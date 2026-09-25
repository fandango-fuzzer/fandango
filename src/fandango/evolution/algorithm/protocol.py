import random
import time
from collections.abc import Generator
from typing import Optional

from fandango.errors import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm.base import GeneticAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.io import FandangoIO
from fandango.io.coverage_filter import PacketCoverageFilter
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.selection.packetselector import PacketSelector
from fandango.io.packet_evolution.io_population_manager import IoPopulationManager
from fandango.io.packet_evolution.mounting_operators import (
    MountingCrossover,
    MountingEvaluator,
    MountingMutation,
)
from fandango.io.packetparser import parse_next_remote_packet
from fandango.io.violation import FandangoRemoteViolation, RemoteViolationType
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER, log_guidance_hint, log_message_transfer


class ProtocolAlgorithm(GeneticAlgorithm):
    def __init__(
        self,
        packet_algorithm: SimpleGeneticAlgorithm,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS,
        remote_response_timeout: float = 15.0,
        max_messages_per_tree: int = 200,
    ):
        self.CLEAR_CONSTRAINT_CACHE_INTERVAL = 100
        self.RANDOM_END_PROBABILITY = 0.5
        self._start_symbol = NonTerminal("<start>")
        self._packet_algorithm = packet_algorithm
        self.grammar = packet_algorithm.grammar
        self._population_manager = IoPopulationManager(
            self.grammar, str(self._start_symbol)
        )
        self._packet_algorithm.population_manager = self._population_manager
        self._packet_algorithm.evaluator = MountingEvaluator(
            self._packet_algorithm.evaluator,
            self._population_manager.packet_mounter,
        )
        self._packet_algorithm.crossover_operator = MountingCrossover(
            self._packet_algorithm.crossover_operator,
            self._population_manager.packet_mounter,
        )
        self._packet_algorithm.mutation_method = MountingMutation(
            self._packet_algorithm.mutation_method,
            self._population_manager.packet_mounter,
        )
        self._protocol_tree: DerivationTree = DerivationTree(self._start_symbol)
        self._coverage_goal = coverage_goal
        self._remote_response_timeout = remote_response_timeout
        self._io_instance: FandangoIO = FandangoIO.instance()
        self._packet_selector: PacketSelector = PacketSelector(
            self.grammar,
            self._io_instance,
            self._protocol_tree,
            self._packet_algorithm.diversity_k,
            max_messages_per_tree=max_messages_per_tree,
        )
        self._packet_selector.set_coverage_goal(self._coverage_goal)
        self._packet_coverage_filter = PacketCoverageFilter(
            self._packet_selector.coverage_tracker
        )
        self.violations: list[tuple[DerivationTree, Exception]] = []
        self.throw_on_violation = False

    @property
    def coverage_goal(self) -> CoverageGoal:
        return self._coverage_goal

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        """Switch the guidance mode, e.g. to CoverageGoal.RANDOM once every
        k-path is covered. Takes effect with the next protocol run."""
        self._coverage_goal = goal
        self._packet_selector.set_coverage_goal(goal)

    def coverage_percent(self) -> Optional[float]:
        """Share of k-paths covered so far, in [0, 1]; None in RANDOM mode,
        which does not track coverage."""
        if self._coverage_goal == CoverageGoal.RANDOM:
            return None
        return self._packet_selector.coverage_percent()

    @property
    def max_messages_per_tree(self) -> int:
        """Messages after which a protocol run is guided to its end."""
        return self._packet_selector.max_messages_per_tree

    @max_messages_per_tree.setter
    def max_messages_per_tree(self, count: int) -> None:
        self._packet_selector.max_messages_per_tree = count

    @property
    def remote_response_timeout(self) -> float:
        return self._remote_response_timeout

    @remote_response_timeout.setter
    def remote_response_timeout(self, seconds: float) -> None:
        self._remote_response_timeout = seconds

    def _is_protocol_run_complete(self) -> bool:
        if not self._packet_selector.is_complete():
            return False
        if len(self._packet_selector.get_next_parties()) == 0:
            return True
        if self._coverage_goal == CoverageGoal.RANDOM:
            return random.random() < self.RANDOM_END_PROBABILITY
        return self._packet_selector.is_guide_to_end()

    def _wait_for_remote_message(self, timeout: float) -> bool:
        wait_start = time.time()
        while not self._io_instance.received_msg():
            if time.time() - wait_start > timeout and timeout >= 0:
                return False
            time.sleep(0.025)
        return True

    def _gen_timeout_violation(self) -> FandangoRemoteViolation:
        external_parties = self._packet_selector.next_external_parties()
        packets_by_party = self._packet_selector.forecasting_result.parties_to_packets
        expected_nonterminals = sorted(
            {
                nonterminal
                for party in external_parties
                for nonterminal in packets_by_party[party].get_non_terminals()
            },
            key=lambda nonterminal: nonterminal.format_as_spec(),
        )
        return FandangoRemoteViolation(
            f"Timed out while waiting for message from remote party. Expected message from party: {', '.join(external_parties)}",
            error_type=RemoteViolationType.TIMEOUT,
            session_tree=self._protocol_tree,
            sender=", ".join(external_parties),
            recipient=None,
            payload_raw="",
            expected_nonterminals=expected_nonterminals,
        )

    def _handle_remote_response(self) -> DerivationTree:
        timeout = self._remote_response_timeout
        for packet in self._packet_selector.next_packets:
            if packet.node.sender == "TimerEvent":
                timeout = -1
        if not self._wait_for_remote_message(timeout):
            raise self._gen_timeout_violation()

        packet_mounter = self._population_manager.packet_mounter
        packet_mounter.reset(self._protocol_tree)
        packet_sender = None
        packet_recipient = None
        packet_tree = None
        expected_nonterminals: list[NonTerminal] = []
        failed_constraints: list[str] = []
        for forecast, packet_tree in parse_next_remote_packet(
            self.grammar,
            self._packet_selector.forecasting_result,
            self._io_instance,
            self._protocol_tree,
        ):
            packet_sender = packet_tree.sender
            packet_recipient = packet_tree.recipient
            packet_tree = packet_tree
            assert packet_sender is not None

            for hookin_option in forecast.paths:
                packet_mounter.attach(packet_tree, hookin_option)
                _solutions, (fitness, failing_trees, _suggestion) = GeneratorWithReturn(
                    self._packet_algorithm.evaluator.evaluate_individual(packet_tree)
                ).collect()
                assert fitness <= 1.0
                if fitness == 1.0:
                    log_message_transfer(
                        packet_sender,
                        packet_recipient,
                        packet_tree,
                        False,
                    )
                    return packet_mounter.mount(packet_tree)
                for failing_tree in failing_trees:
                    constraint = failing_tree.cause.format_as_spec()
                    if constraint not in failed_constraints:
                        failed_constraints.append(constraint)
            if packet_tree.nonterminal not in expected_nonterminals:
                expected_nonterminals.append(packet_tree.nonterminal)
        if packet_tree is not None:
            assert packet_sender is not None
            log_message_transfer(
                packet_sender,
                packet_recipient,
                packet_tree,
                False,
            )
            raise FandangoRemoteViolation(
                "Remote response does not match constraints",
                error_type=RemoteViolationType.CONSTRAINT,
                session_tree=self._protocol_tree,
                sender=packet_sender,
                recipient=packet_recipient,
                payload_raw=packet_tree.to_bytes()
                if packet_tree.contains_bytes()
                else packet_tree.to_string(),
                expected_nonterminals=expected_nonterminals,
                failed_constraints=failed_constraints,
                payload_tree=packet_tree,
            )
        raise FandangoParseError("Remote response does not match constraints")

    def _filter_by_coverage(self, packet: DerivationTree) -> Optional[DerivationTree]:
        with self._population_manager.packet_mounter.mount_context(packet):
            return self._packet_coverage_filter.filter(packet)

    def _generate_packet(self, max_generations: int | None = None) -> DerivationTree:
        if max_generations is None:
            selected_packet_max_generations = 10
            overall_max_generations = max_generations
        else:
            selected_packet_max_generations = int(max_generations / 3)
            overall_max_generations = max_generations - selected_packet_max_generations

        self._packet_algorithm.reset()
        try:
            solutions = [
                next(
                    filter(
                        self._filter_by_coverage,
                        self._population_manager.refill_population(
                            current_population=self._packet_algorithm.population,
                            eval_individual=self._packet_algorithm.evaluator.evaluate_individual,
                            max_nodes=self._packet_algorithm.adaptive_tuner.current_max_nodes,
                            target_population_size=self._packet_algorithm.population_size,
                        ),
                    )
                )
            ]
        except StopIteration:
            solutions = []
        if solutions:
            return solutions[0]

        try:
            return next(
                filter(
                    self._filter_by_coverage,
                    self._packet_algorithm.generate(
                        max_generations=selected_packet_max_generations
                    ),
                )
            )
        except StopIteration:
            pass

        self._packet_coverage_filter.mark_uncovered_k_paths_unreachable()
        if len(self._packet_coverage_filter.hold_back_solutions) != 0:
            return random.choice(list(self._packet_coverage_filter.hold_back_solutions))

        self._population_manager.allow_fallback_packets = True
        try:
            return next(
                self._packet_algorithm.generate(max_generations=overall_max_generations)
            )
        except StopIteration:
            all_allowed_packets = (
                self._population_manager.fuzzable_packets
                + self._population_manager.fallback_packets
            )
            nonterminals_str = " | ".join(
                map(lambda x: str(x.node.symbol), all_allowed_packets)
            )
            raise FandangoFailedError(
                f"Couldn't find solution for any packet: {nonterminals_str}"
            ) from None

    def _is_coverage_complete(self) -> bool:
        return (
            self._coverage_goal != CoverageGoal.RANDOM
            and self._packet_selector.coverage_percent() == 1.0
        )

    def _is_failed_forecast(self) -> bool:
        return (
            len(self._packet_selector.get_next_parties()) == 0
            and not self._packet_selector.is_complete()
        )

    def _clear_constraint_caches(self) -> None:
        self._packet_algorithm.evaluator.clear_constraint_caches()

    def generate(
        self,
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
    ) -> Generator[DerivationTree, None, None]:
        iteration = 0
        while True:
            iteration += 1
            if (
                self.CLEAR_CONSTRAINT_CACHE_INTERVAL > 0
                and iteration % self.CLEAR_CONSTRAINT_CACHE_INTERVAL == 0
            ):
                self._clear_constraint_caches()
            self._packet_selector.compute(self._protocol_tree)
            if self._coverage_goal != CoverageGoal.RANDOM:
                LOGGER.info(
                    f"Current coverage: {self._packet_selector.coverage_percent() * 100:.2f}%"
                )

            if self._is_failed_forecast():
                raise FandangoFailedError("Could not forecast next packet")

            if self._is_protocol_run_complete():
                final_tree = random.choice(
                    list(self._packet_selector.forecasting_result.complete_trees)
                )
                self._packet_selector.add_completed_tree(final_tree)
                self._packet_coverage_filter.add_completed_tree(final_tree)
                yield final_tree
                if self._is_coverage_complete():
                    log_guidance_hint("Full coverage reached, stopping evolution.")
                    return None
                log_guidance_hint("Starting new protocol run.")
                self._io_instance.reset_parties()
                self._protocol_tree = DerivationTree(self._start_symbol, [])
                continue

            if self._should_generate_next_packet():
                self._packet_algorithm.reset()
                self._configure_fuzzable_packets()
                self._packet_coverage_filter.set_current_tree(self._protocol_tree)
                next_history_tree = self._population_manager.packet_mounter.mount(
                    self._generate_packet(max_generations=max_generations)
                )
                if self._io_instance.received_msg():
                    continue
                new_packet = next(next_history_tree.protocol_msgs(reverse=True))
                if (
                    new_packet.recipient is None
                    or not self._io_instance.parties[
                        new_packet.recipient
                    ].is_fuzzer_controlled()
                ):
                    self._io_instance.transmit(
                        new_packet.sender, new_packet.recipient, new_packet.msg
                    )
                    log_message_transfer(
                        new_packet.sender,
                        new_packet.recipient,
                        new_packet.msg,
                        True,
                    )
                self._protocol_tree = next_history_tree
            else:
                try:
                    self._protocol_tree = self._handle_remote_response()
                except (
                    FandangoFailedError,
                    FandangoParseError,
                    FandangoValueError,
                ) as exc:
                    self._packet_selector.abort_run(self._protocol_tree)
                    self._packet_coverage_filter.add_completed_tree(self._protocol_tree)
                    self.violations.append((self._protocol_tree, exc))
                    if self.throw_on_violation:
                        raise exc
                    LOGGER.warning(
                        f"Discarding remote response that could not be handled. "
                        f"Recording violation: {exc}"
                    )
                    if self._is_coverage_complete():
                        log_guidance_hint("Full coverage reached, stopping evolution.")
                        return None
                    log_guidance_hint("Starting new protocol run.")
                    self._io_instance.reset_parties()
                    self._protocol_tree = DerivationTree(self._start_symbol, [])
                    continue
            self._protocol_tree.set_all_read_only(True)

    def _configure_fuzzable_packets(self) -> None:
        self._population_manager.packet_mounter.reset(self._protocol_tree)
        self._clear_constraint_caches()
        self._population_manager.fuzzable_packets = self._packet_selector.next_packets
        self._population_manager.fallback_packets = []
        for sender in self._packet_selector.next_fuzzer_parties():
            self._population_manager.fallback_packets.extend(
                list(
                    self._packet_selector.forecasting_result.parties_to_packets[
                        sender
                    ].nt_to_packet.values()
                )
            )
        self._population_manager.allow_fallback_packets = False

        preferred_symbols: list[str] = [
            str(pkg.node.symbol) for pkg in self._population_manager.fuzzable_packets
        ]
        LOGGER.debug(f"Trying to generate: {', '.join(preferred_symbols)}")

    def _should_generate_next_packet(self) -> bool:
        if len(self._packet_selector.next_packets) == 1:
            for packet in self._packet_selector.next_packets:
                if packet.node.sender == "TimerEvent":
                    return False
        return (
            len(self._packet_selector.next_fuzzer_parties()) != 0
            and not self._io_instance.received_msg()
        )

    def reset(self) -> None:
        self._packet_algorithm.reset()
        self._packet_selector.reset_coverage()
        self._packet_coverage_filter.reset()
        self._protocol_tree = DerivationTree(self._start_symbol)

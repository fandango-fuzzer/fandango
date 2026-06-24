

import random
import time
from collections.abc import Generator
from typing import Optional

from fandango.errors import FandangoFailedError, FandangoParseError
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm.base import GeneticAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.evolution.population import IoPopulationManager
from fandango.io import FandangoIO
from fandango.io.coverage_filter import PacketCoverageFilter
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.io.navigation.packetselector import PacketSelector
from fandango.io.packetparser import parse_next_remote_packet
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER, log_guidance_hint, log_message_transfer


class ProtocolAlgorithm(GeneticAlgorithm):
    def __init__(
        self,
        packet_algorithm: SimpleGeneticAlgorithm,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS,
        remote_response_timeout: int = 15,
    ):
        self._start_symbol = NonTerminal("<start>")
        self._packet_algorithm = packet_algorithm
        self.grammar = packet_algorithm.grammar
        self._population_manager = IoPopulationManager(
            self.grammar, str(self._start_symbol)
        )
        self._packet_algorithm.population_manager = self._population_manager
        self._protocol_tree: DerivationTree = DerivationTree(self._start_symbol)
        self._past_interactions: list[DerivationTree] = []
        self._coverage_goal = coverage_goal
        self._remote_response_timeout = remote_response_timeout
        self._io_instance: FandangoIO = FandangoIO.instance()
        self._packet_selector: PacketSelector = PacketSelector(
            self.grammar,
            self._io_instance,
            self._protocol_tree,
            self._packet_algorithm.diversity_k,
        )
        self._packet_selector.set_coverage_goal(self._coverage_goal)
        self._packet_coverage_filter = PacketCoverageFilter(
            self._packet_algorithm.diversity_k, self.grammar
        )
        self._time_in_measurements = 0
        self.coverage_log_interval = -1
        self.stop_on_full_coverage = True
        self._is_enable_guidance = True
        self.coverage_log: list[tuple[float, dict[NonTerminal, tuple[int, int]]]] = []
        self.coverage_log_overlap: list[
            tuple[float, dict[NonTerminal, tuple[int, int]]]
        ] = []
        self.violations = []
        self.throw_on_violation = False

    def _is_protocol_run_complete(self) -> bool:
        return (
            len(self._packet_selector.get_next_parties()) == 0
            or self._packet_selector.is_guide_to_end()
            or self._coverage_goal == CoverageGoal.SINGLE_DERIVATION
        ) and self._packet_selector.is_complete()

    def _wait_for_remote_message(self, timeout: int) -> bool:
        wait_start = time.time()
        while not self._io_instance.received_msg():
            if time.time() - wait_start > timeout and timeout >= 0:
                return False
            time.sleep(0.025)
        return True

    def _handle_remote_response(self) -> DerivationTree:
        timeout = self._remote_response_timeout
        for packet in self._packet_selector.next_packets:
            if packet.node.sender == "TimerEvent":
                timeout = -1
        if not self._wait_for_remote_message(timeout):
            external_parties = self._packet_selector.next_external_parties()
            raise FandangoFailedError(
                f"Timed out while waiting for message from remote party. Expected message from party: {', '.join(external_parties)}"
            )

        packet_sender = None
        packet_recipient = None
        packet_tree = None
        for forecast, packet_tree in parse_next_remote_packet(
            self.grammar,
            self._packet_selector.forecasting_result,
            self._io_instance,
        ):
            packet_sender = packet_tree.sender
            packet_recipient = packet_tree.recipient
            packet_tree = packet_tree
            assert packet_sender is not None

            for hookin_option in forecast.paths:
                # Deepcopy so that a failed constraint attempt on one NT
                # does not corrupt the shared base tree for the next candidate.
                history_tree = hookin_option.tree.deepcopy(copy_parent=False)
                history_tree.append(hookin_option.path[1:-1], packet_tree)
                _solutions, (fitness, _failing_trees, _suggestion) = (
                    GeneratorWithReturn(
                        self._packet_algorithm.evaluator.evaluate_individual(
                            history_tree
                        )
                    ).collect()
                )
                assert fitness <= 1.0
                if fitness == 1.0:
                    log_message_transfer(
                        packet_sender,
                        packet_recipient,
                        packet_tree,
                        False,
                    )
                    return history_tree
        if packet_tree is not None:
            assert packet_sender is not None
            log_message_transfer(
                packet_sender,
                packet_recipient,
                packet_tree,
                False,
            )
        raise FandangoParseError("Remote response does not match constraints")

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
                        lambda x: self._packet_coverage_filter.filter(x),
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

        if solutions:
            return solutions[0]

        try:
            return next(
                filter(
                    lambda x: self._packet_coverage_filter.filter(x),
                    self._packet_algorithm.generate(
                        max_generations=selected_packet_max_generations
                    ),
                )
            )
        except StopIteration:
            pass

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

    def _is_failed_forecast(self) -> bool:
        return (
            len(self._packet_selector.get_next_parties()) == 0
            and not self._packet_selector.is_complete()
        )

    def generate(
        self,
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
    ) -> Generator[DerivationTree, None, None]:
        iteration = 0
        while True:
            self._packet_selector.compute(self._protocol_tree, self._past_interactions)
            start_measuring = time.time()
            iteration += 1
            if (
                self.coverage_log_interval > 0
                and iteration % self.coverage_log_interval == 0
            ):
                current_cov = (
                    self._packet_selector.coverage_percent(alt_cache=True) * 100
                )
                LOGGER.info(f"Current coverage: {current_cov:.2f}%")
                self.coverage_log.append(
                    (
                        start_measuring - self._time_in_measurements,
                        self._packet_selector._compute_coverage_trees(False),
                    )
                )
                self.coverage_log_overlap.append(
                    (
                        start_measuring - self._time_in_measurements,
                        self._packet_selector._compute_coverage_trees(True),
                    )
                )
            self._time_in_measurements += time.time() - start_measuring

            if self._is_failed_forecast():
                raise FandangoFailedError("Could not forecast next packet")

            if self._is_protocol_run_complete():
                final_tree = random.choice(
                    list(self._packet_selector.forecasting_result.complete_trees)
                )
                self._past_interactions.append(final_tree)
                yield final_tree
                if self._coverage_goal == CoverageGoal.SINGLE_DERIVATION:
                    return None
                if self._packet_selector.coverage_percent() == 1.0:
                    if self.stop_on_full_coverage:
                        log_guidance_hint("Full coverage reached, stopping evolution.")
                        return None
                    self.enable_guidance(False)
                log_guidance_hint("Starting new protocol run.")
                self._io_instance.reset_parties()
                self._protocol_tree = DerivationTree(self._start_symbol, [])
                continue

            if self._should_generate_next_packet():
                self._packet_algorithm.reset()
                self._configure_fuzzable_packets()
                self._packet_coverage_filter.set_existing_derivations(
                    [self._protocol_tree] + self._past_interactions
                )
                next_history_tree = self._generate_packet(
                    max_generations=max_generations
                )
                if self._io_instance.received_msg():
                    continue
                new_packet = next_history_tree.protocol_msgs()[-1]
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
                except (FandangoFailedError, FandangoParseError) as exc:
                    self._past_interactions.append(self._protocol_tree)
                    self.violations.append((self._protocol_tree, exc))
                    if self.throw_on_violation:
                        raise exc
                    LOGGER.warning(
                        f"Discarding remote response that could not be handled. "
                        f"Recording violation and starting a new protocol run: {exc}"
                    )
                    self._io_instance.reset_parties()
                    self._protocol_tree = DerivationTree(self._start_symbol, [])
                    continue
            self._protocol_tree.set_all_read_only(True)

    def _configure_fuzzable_packets(self) -> None:
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
        self._past_interactions.clear()
        self._protocol_tree = DerivationTree(self._start_symbol)

    def enable_guidance(self, value: bool) -> None:
        self._is_enable_guidance = value
        self._packet_coverage_filter.disable_filtering = not value
        self._packet_selector.enable_guidance(value)

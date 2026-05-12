import random
import time
from typing import Generator, Optional

from fandango import FandangoParseError
from fandango.errors import FandangoFailedError
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm import GeneticAlgorithm
from fandango.io import FandangoIO
from fandango.io.coverage_filter import PacketCoverageFilter
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.io.navigation.packetselector import PacketSelector
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER, log_guidance_hint, log_message_transfer


class ProtocolAlgorithm(GeneticAlgorithm):

    def __init__(
        self,
        packet_algorithm: GeneticAlgorithm,
        coverage_goal: CoverageGoal,
        remote_response_timeout: float = 15.0,
    ):
        self._start_symbol = NonTerminal("<start>")
        self._packet_algorithm = packet_algorithm
        self._protocol_tree: DerivationTree = DerivationTree(
            self._start_symbol
        )
        self._past_interactions: list[DerivationTree] = []
        self._coverage_goal = coverage_goal
        self._remote_response_timeout = remote_response_timeout
        self._io_instance: FandangoIO = FandangoIO.instance()
        self._packet_selector: PacketSelector = PacketSelector(
            self.grammar,
            self._io_instance,
            self._protocol_tree,
            self._packet_strategy.diversity_k
        )
        self._packet_selector.set_coverage_goal(self._coverage_goal)
        self._packet_coverage_filter = PacketCoverageFilter(
            self._packet_strategy.diversity_k,
            self.grammar
        )


    def _is_protocol_run_complete(self) -> bool:
        return (
            (
                len(self._packet_selector.get_next_parties()) == 0
                or self._packet_selector.is_guide_to_end()
                or self.coverage_goal == CoverageGoal.SINGLE_DERIVATION
            )
            and self._packet_selector.is_complete()
        )

    def _wait_for_remote_message(self, timeout: float) -> bool:
        wait_start = time.time()
        while not self._io_instance.received_msg():
            if time.time() - wait_start > timeout:
                return False
            time.sleep(0.025)
        return True

    def _handle_remote_response(self) -> DerivationTree:
        if not self._wait_for_remote_message(self.remote_response_timeout):
            external_parties = self._packet_selector.next_external_parties()
            raise FandangoFailedError(
                f"Timed out while waiting for message from remote party. Expected message from party: {', '.join(external_parties)}"
            )
        forecast, packet_tree = parse_next_remote_packet(
            self.grammar,
            self._packet_selector.forecasting_result,
            self._io_instance,
        )
        assert packet_tree is not None
        assert forecast is not None
        packet_sender = packet_tree.sender
        assert packet_sender is not None
        log_message_transfer(
            packet_sender,
            packet_tree.recipient,
            packet_tree,
            False,
        )

        for hookin_option in forecast.paths:
            history_tree = hookin_option.tree
            history_tree.append(hookin_option.path[1:-1], packet_tree)
            _solutions, (fitness, _failing_trees, _suggestion) = GeneratorWithReturn(
                self._packet_strategy.evaluator.evaluate_individual(history_tree)
            ).collect()
            assert fitness <= 1.0
            if fitness == 1.0:
                return history_tree
        raise FandangoParseError("Remote response does not match constraints")


    def _generate_packet(self, max_generations: int | None = None) -> DerivationTree:
        if max_generations is None:
            selected_packet_max_generations = 10
            overall_max_generations = max_generations
        else:
            selected_packet_max_generations = int(max_generations / 3)
            overall_max_generations = max_generations - selected_packet_max_generations

        try:
            solutions = [
                next(
                    filter(
                        lambda x: self._packet_coverage_filter.filter(x),
                        self._population_manager.refill_population(
                            current_population=self._packet_strategy.population,
                            eval_individual=self._packet_strategy.evaluator.evaluate_individual,
                            max_nodes=self._packet_strategy.adaptive_tuner.current_max_nodes,
                            target_population_size=self._packet_strategy.population_size,
                        )
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
                    self._packet_strategy.generate(
                        max_generations=selected_packet_max_generations
                    )
                )
            )
        except StopIteration:
            pass

        if len(self._packet_coverage_filter.hold_back_solutions) != 0:
            return random.choice(list(self._packet_coverage_filter.hold_back_solutions))

        self._population_manager.allow_fallback_packets = True
        try:
            return next(
                filter(
                    lambda x: self._packet_coverage_filter.filter(x),
                    self._packet_strategy.generate(
                        max_generations=overall_max_generations
                    )
                )
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
            )


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
        while True:
            self._packet_selector.compute(self._protocol_tree, self._past_interactions)
            LOGGER.info(
                f"Current coverage: {self._packet_selector.coverage_percent() * 100:.2f}%"
            )

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
                    log_guidance_hint("Full coverage reached, stopping evolution.")
                    return None
                log_guidance_hint("Starting new protocol run.")
                self._io_instance.reset_parties()
                self._protocol_tree = DerivationTree(self._start_symbol, [])
                continue

            if self._should_fuzz_next_packet():
                self._packet_strategy.reset()
                self._configure_fuzzable_packets()
                self._packet_coverage_filter.set_existing_derivations(
                    [self._protocol_tree] + self._past_interactions
                )
                next_history_tree = self._generate_packet(max_generations=max_generations)
                if self._io_instance.received_msg():
                    return None
                new_packet = next_history_tree.protocol_msgs()[-1]
                if (
                        new_packet.recipient is None
                        or not self._io_instance.parties[new_packet.recipient].is_fuzzer_controlled()
                ):
                    self._io_instance.transmit(new_packet.sender, new_packet.recipient, new_packet.msg)
                    log_message_transfer(
                        new_packet.sender,
                        new_packet.recipient,
                        new_packet.msg,
                        True,
                    )
                if next_history_tree is None:
                    continue
                protocol_tree = next_history_tree
            else:
                protocol_tree = self._handle_remote_response()
            protocol_tree.set_all_read_only(True)
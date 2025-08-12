from typing import Optional

from fandango.io import FandangoIO
from fandango.language.tree import DerivationTree
from fandango.io.navigation.packetforecaster import (
    ForcastingPacket,
    PacketForecaster,
    ForecastingResult,
)
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language import Grammar
from fandango.language.symbols import NonTerminal
from fandango.logger import log_guidance_hint


class PacketSelector:
    def __init__(
        self, grammar: Grammar, io_instance: FandangoIO, history_tree: DerivationTree
    ):
        self.grammar = grammar
        self.io_instance = io_instance
        self.navigator = PacketNavigator(grammar, NonTerminal("<start>"))
        self.forecaster = PacketForecaster(self.grammar)
        self.parst_derivations: set[DerivationTree] = set()
        self.history_tree = None
        self._forecasting_result = None
        self._next_packets = None
        self._coverage_scores = None
        self._guide_to_end = False
        self.compute(history_tree, self.parst_derivations)

    def _compute_message_coverage_score(
        self, k: int, show_external: bool = False
    ) -> list[tuple[tuple[str, Optional[str], NonTerminal], float]]:
        """
        Computes the coverage score for each NonTerminal in the given DerivationTrees.
        The score is the ratio of the number of trees containing the NonTerminal to the total number of trees.

        :param trees: List of DerivationTrees to analyze.
        :param k: The k-path length for coverage computation.
        :return: Dictionary mapping NonTerminals to their coverage scores.
        """
        fuzzer_parties = set(
            map(lambda x: x.party_name, self.io_instance.get_fuzzer_parties())
        )
        trees = list(self.parst_derivations)
        trees.append(self.history_tree)
        messages: list[DerivationTree] = []
        for tree in trees:
            if show_external:
                messages.extend(map(lambda x: x.msg, tree.protocol_msgs()))
            else:
                messages.extend(
                    filter(
                        lambda y: y.sender in fuzzer_parties,
                        map(lambda x: x.msg, tree.protocol_msgs()),
                    )
                )
        messages_by_nt = {}
        for msg in messages:
            messages_by_nt.setdefault(
                (msg.sender, msg.recipient, msg.symbol), []
            ).append(msg)
        nt_coverage = {}
        for sender, recipient, non_terminal in self.grammar.get_protocol_messages():
            if not (show_external or (sender in fuzzer_parties)):
                continue
            if (sender, recipient, non_terminal) not in messages_by_nt:
                nt_coverage[(sender, recipient, non_terminal)] = 0.0
                continue
            nt_coverage[(sender, recipient, non_terminal)] = (
                self.grammar.compute_kpath_coverage(
                    messages_by_nt[(sender, recipient, non_terminal)], k, non_terminal
                )
            )
        nt_coverage = list(
            sorted(nt_coverage.items(), key=lambda x: (x[1], x[0][2].name()))
        )
        return nt_coverage

    def _get_guide_to_end_packet(self) -> Optional[ForcastingPacket]:
        path = self.navigator.astar_search_end(self.history_tree)
        if len(path) > 0:
            sender, receiver, next_nt = path[0]
            if (
                sender in self.next_fuzzer_parties()
                and next_nt in self.forecasting_result[sender].nt_to_packet
            ):
                return self.forecasting_result[sender].nt_to_packet[next_nt]
        return None

    def compute(
        self, history_tree: DerivationTree, parst_derivations: set[DerivationTree]
    ):
        self.history_tree = history_tree
        self.parst_derivations = parst_derivations
        self._forecasting_result = None
        self._coverage_scores = None
        self._next_packets = None

    @property
    def forecasting_result(self) -> ForecastingResult:
        if self._forecasting_result is None:
            self._forecasting_result = self.forecaster.predict(self.history_tree)
        return self._forecasting_result

    @property
    def coverage_scores(
        self,
    ) -> list[tuple[tuple[str, Optional[str], NonTerminal], float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_message_coverage_score(2)
        return self._coverage_scores

    @property
    def next_packets(self) -> list[ForcastingPacket]:
        if self._next_packets is None:
            self._next_packets = self._select_next_packet()
        return self._next_packets

    def is_guide_to_end(self) -> bool:
        return self._guide_to_end

    def is_complete(self) -> bool:
        assert self.forecasting_result is not None
        return len(self.forecasting_result.complete_trees) != 0

    def next_fuzzer_parties(self) -> list[str]:
        assert self.forecasting_result is not None
        return list(
            filter(
                lambda x: self.io_instance.parties[x].is_fuzzer_controlled(),
                self.forecasting_result.get_msg_parties(),
            )
        )

    def next_external_parties(self) -> list[str]:
        assert self.forecasting_result is not None
        return list(
            filter(
                lambda x: not self.io_instance.parties[x].is_fuzzer_controlled(),
                self.forecasting_result.get_msg_parties(),
            )
        )

    def get_next_parties(self) -> list[str]:
        return list(self.forecasting_result.get_msg_parties())

    def _select_next_packet(self):
        fuzzable_packets = []
        if len(self.next_fuzzer_parties()) == 0:
            return fuzzable_packets
        self._guide_to_end = False
        max_messages_per_tree = 50
        if len(self.history_tree.protocol_msgs()) > max_messages_per_tree:
            log_guidance_hint(
                f"Current tree contains more then {max_messages_per_tree} messages. Guiding to end of tree."
            )
            self._guide_to_end = True
            fuzzable_packets.append(self._get_guide_to_end_packet())
            return fuzzable_packets
        # Select next packet to send by computing guiding generator to underexplored areas of the grammar
        all_derivations = list(self.parst_derivations)
        all_derivations.append(self.history_tree)
        if len(self.coverage_scores) > 0 and self.coverage_scores[0][1] == 1.0:
            log_guidance_hint("Full coverage reached. Guiding to end of tree.")
            self._guide_to_end = True
            fuzzable_packets.append(self._get_guide_to_end_packet())
            return fuzzable_packets

        for (sender, recipient, target_nt), coverage_score in self.coverage_scores:
            path = self.navigator.astar_tree(tree=self.history_tree, symbol=target_nt)
            if path is None:
                # We can't find a path to this non-terminal. That means we can't reach it without starting a new tree.
                # So we try to finish this tree ASAP by selecting the non-terminal with the lowest distance to completion.
                log_guidance_hint(
                    f"No path found for target {target_nt} with score {coverage_score}. Guiding to end of tree."
                )
                self._guide_to_end = True
                fuzzable_packets.append(self._get_guide_to_end_packet())
                break
            else:
                log_guidance_hint(
                    f"Guiding to target {target_nt} with score {coverage_score}"
                )
                sender, receiver, next_nt = path[0]
                if (
                    sender in self.next_fuzzer_parties()
                    and next_nt in self.forecasting_result[sender].nt_to_packet
                ):
                    fuzzable_packets.append(
                        self.forecasting_result[sender].nt_to_packet[next_nt]
                    )
                    break
        if len(fuzzable_packets) == 0:
            fuzzable_packets.append(self._get_guide_to_end_packet())
        return fuzzable_packets

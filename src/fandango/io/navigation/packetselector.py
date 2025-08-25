from typing import Optional

from fandango.io import FandangoIO
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.grammarreducer import GrammarReducer
from fandango.io.navigation.powerschedule import PowerSchedule
from fandango.language.tree import DerivationTree
from fandango.io.navigation.packetforecaster import (
    ForecastingPacket,
    PacketForecaster,
    ForecastingResult,
)
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language import Grammar
from fandango.language.symbols import NonTerminal
from fandango.logger import log_guidance_hint


class PacketSelector:
    def __init__(
        self,
        grammar: Grammar,
        io_instance: FandangoIO,
        history_tree: DerivationTree,
        diversity_k: int,
    ):
        self.start_symbol = NonTerminal("<start>")
        self.grammar = grammar
        reduced_grammar = GrammarReducer(self.grammar.grammar_settings).process(self.grammar.rules, self.start_symbol)
        self.coverage_symbols = list(reduced_grammar.keys())
        self.coverage_symbols.extend(map(lambda x: x[2], self.grammar.get_protocol_messages(self.start_symbol)))
        self.coverage_symbols = list(filter(lambda x: x in self.grammar.rules, self.coverage_symbols))
        self.power_schedule = PowerSchedule()
        self.io_instance = io_instance
        self.navigator = PacketNavigator(grammar, self.start_symbol)
        self.forecaster = PacketForecaster(self.grammar)
        self.diversity_k = diversity_k
        self.parst_derivations: set[DerivationTree] = set()
        self.history_tree = None
        self._forecasting_result = None
        self._next_packets = None
        self._old_packet_selections = []
        self._old_coverage_scores = []
        self._coverage_scores = None
        self._guide_to_end = False
        self._current_guide_target = None
        self._current_guide_path = None
        self.compute(history_tree, self.parst_derivations)

    def _group_messages_by_nt(self, trees: list[DerivationTree]):
        messages: list[DerivationTree] = []
        for tree in trees:
            for subtree in tree.flatten():
                if subtree.symbol in self.coverage_symbols:
                    messages.append(subtree)
        messages_by_nt = {}
        for msg in messages:
            messages_by_nt.setdefault(msg.symbol, []).append(msg)
        return messages_by_nt


    def _compute_coverage_score(
        self, k: int
    ) -> list[tuple[NonTerminal, float]]:
        """
        Computes the coverage score for each NonTerminal in the given DerivationTrees.
        The score is the ratio of the number of trees containing the NonTerminal to the total number of trees.

        :param trees: List of DerivationTrees to analyze.
        :param k: The k-path length for coverage computation.
        :return: Dictionary mapping NonTerminals to their coverage scores.
        """
        trees = list(self.parst_derivations)
        trees.append(self.history_tree)
        messages_by_nt = self._group_messages_by_nt(trees)
        nt_coverage = {}
        for symbol in self.coverage_symbols:
            if symbol not in messages_by_nt:
                nt_coverage[symbol] = 0.0
                continue
            nt_coverage[symbol] = (
                self.grammar.compute_kpath_coverage(
                    messages_by_nt[symbol], k, symbol
                )
            )
        nt_coverage = list(
            sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name()))
        )
        return nt_coverage

    def _get_guide_to_end_packet(self) -> list[ForecastingPacket]:
        path = self.navigator.astar_search_end(self.history_tree)
        if len(path) > 0:
            next_packet = next(filter(lambda x: isinstance(x, PacketNonTerminal), path), None)
            if next_packet is None:
                return []
            assert isinstance(next_packet, PacketNonTerminal)
            if (
                next_packet.sender in self.next_fuzzer_parties()
                and next_packet.symbol in self.forecasting_result[next_packet.sender].nt_to_packet
            ):
                return [self.forecasting_result[next_packet.sender].nt_to_packet[next_packet.symbol]]
        return []

    def compute(
        self, history_tree: DerivationTree, parst_derivations: set[DerivationTree]
    ):
        self.history_tree = history_tree
        self.parst_derivations = parst_derivations
        if self._coverage_scores is not None:
            self._old_coverage_scores.append(self._coverage_scores)
        if self._next_packets is not None:
            for packet in self._next_packets:
                node = packet.node
                self._old_packet_selections.append(
                    (node.sender, node.recipient, node.symbol)
                )
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
    ) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_score(
                self.diversity_k
            )
        return self._coverage_scores

    @property
    def next_packets(self) -> list[ForecastingPacket]:
        if self._next_packets is None:
            self._next_packets = self._select_next_packet()
        return self._next_packets

    def is_guide_to_end(self) -> bool:
        if self._next_packets is None:
            self._next_packets = self._select_next_packet()
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

    def get_fuzzer_packets(self):
        assert self.forecasting_result is not None
        return [
            packet
            for sender in self.next_fuzzer_parties()
            for packet in self.forecasting_result.parties_to_packets[sender].nt_to_packet.values()
        ]

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
        max_messages_per_tree = 100
        if len(self.history_tree.protocol_msgs()) > max_messages_per_tree:
            log_guidance_hint(
                f"Current tree contains more then {max_messages_per_tree} messages. Guiding to end of tree."
            )
            self._guide_to_end = True
            fuzzable_packets.extend(self._get_guide_to_end_packet())
            return fuzzable_packets
        # Select next packet to send by computing guiding generator to underexplored areas of the grammar
        all_derivations = list(self.parst_derivations)
        all_derivations.append(self.history_tree)
        if len(self.coverage_scores) > 0 and self.coverage_scores[0][1] == 1.0:
            log_guidance_hint("Full coverage reached. Guiding to end of tree.")
            self._guide_to_end = True
            fuzzable_packets.extend(self._get_guide_to_end_packet())
            return fuzzable_packets

        for target_nt, coverage_score in self.coverage_scores:
            messages = self.history_tree.protocol_msgs()
            if len(messages) > 0:
                last_message = messages[-1]
                if target_nt in last_message.get_state_nt():
                    fuzzable_packets.extend(self.get_fuzzer_packets_w_coverage(target_nt, all_derivations))
                    if len(fuzzable_packets) > 0:
                        return fuzzable_packets
                    fuzzable_packets.extend(self.get_fuzzer_packets())
                    return fuzzable_packets
            path = self.navigator.astar_tree(tree=self.history_tree, symbol=target_nt)
            log_guidance_hint(
                f"Guiding to target {target_nt} with score {coverage_score}"
            )
            self._guide_to_end = any(filter(lambda p: p is None, path))

            next_packet = next((x for x in path if isinstance(x, PacketNonTerminal)), None)
            if next_packet is None:
                # If no packet needs to be sent to reach the target, we are in a state that contains the target state that we want to reach.
                # We send a packet that adds the target state nonterminal as part of its hookin path.
                for sender in self.next_fuzzer_parties():
                    fuzzable_packets.extend(self.find_packets_with_sender_path_symbol(sender, target_nt))
                if len(fuzzable_packets) == 0:
                    fuzzable_packets.extend(self.get_fuzzer_packets())
                return fuzzable_packets

            if (
                    next_packet.sender in self.next_fuzzer_parties()
                    and next_packet.symbol in self.forecasting_result[next_packet.sender].nt_to_packet
            ):
                fuzzable_packets.extend(self.find_packets_with_sender_path_symbol(next_packet.sender, target_nt, next_packet.symbol))
                if len(fuzzable_packets) == 0:
                    fuzzable_packets.append(
                        self.forecasting_result[next_packet.sender].nt_to_packet[next_packet.symbol]
                    )
                break
        if len(fuzzable_packets) == 0:
            fuzzable_packets.extend(self._get_guide_to_end_packet())
        return fuzzable_packets


    def find_packets_with_sender_path_symbol(self, sender: str, path_symbol: NonTerminal, packet_symbol: Optional[NonTerminal] = None) -> list[ForecastingPacket]:
        packets = []
        if sender in self.next_fuzzer_parties():
            for packet in self.forecasting_result[sender].nt_to_packet.values():
                if packet_symbol is not None and packet.node.symbol != packet_symbol:
                    continue
                append_packet = ForecastingPacket(packet.node)
                for hookin_path in packet.paths:
                    if any(filter(lambda s: s[0] == path_symbol and s[1], hookin_path.path)):
                        append_packet.paths.add(hookin_path)
                if len(append_packet.paths) != 0:
                    packets.append(append_packet)
        return packets

    def get_fuzzer_packets_w_coverage(self, target_nt, all_derivations) -> list[ForecastingPacket]:
        def contains(sub, full):
            n, m = len(sub), len(full)
            if n == 0:
                return True
            for i in range(m - n + 1):
                if full[i:i + n] == sub:
                    return True
            return False
        by_nt = self._group_messages_by_nt(all_derivations)
        if target_nt not in by_nt:
            missing_paths = self.grammar.find_missing_k_paths([], self.diversity_k, target_nt)
        else:
            missing_paths = self.grammar.find_missing_k_paths(by_nt[target_nt], self.diversity_k, target_nt)
        packets = []
        assert self.forecasting_result is not None
        for packet in self.get_fuzzer_packets():
            append_packet = ForecastingPacket(packet.node)
            for path in packet.paths:
                symbol_path = tuple(map(lambda x: x[0], path.path))
                symbol_path = (*symbol_path, packet.node.symbol)

                truncated_paths = []
                for missing_path in missing_paths:
                    if packet.node.symbol in missing_path:
                        truncated_paths.append(missing_path[:(missing_path.index(packet.node.symbol)+1)])
                    else:
                        truncated_paths.append(missing_path)
                if any(filter(lambda x: contains(x, symbol_path), truncated_paths)):
                    append_packet.paths.add(path)
            if len(append_packet.paths) != 0:
                packets.append(append_packet)
        return packets
import random
from typing import Optional

from fandango.io import FandangoIO
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.grammarreducer import GrammarReducer
from fandango.io.navigation.powerschedule import PowerSchedule
from fandango.io.rule_completion_tester import RuleCompletionTester
from fandango.language.tree import DerivationTree
from fandango.io.navigation.packetforecaster import (
    ForecastingPacket,
    PacketForecaster,
    ForecastingResult,
)
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal, Symbol
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
        self._completion_tester = RuleCompletionTester(self.grammar)
        self.coverage_symbols = self._get_subgrammar_symbols(self.start_symbol)
        self.power_schedules: dict[Symbol, PowerSchedule] = dict()
        self.io_instance = io_instance
        self.navigator = PacketNavigator(grammar, self.start_symbol)
        self.forecaster = PacketForecaster(self.grammar)
        self.diversity_k = diversity_k
        self.parst_derivations: list[DerivationTree] = []
        self.prev_past_derivations_len = 0
        self.history_tree = None
        self._forecasting_result = None
        self._next_packets = None
        self._coverage_scores = None
        self._guide_to_end = False
        self._guide_target = None
        self._guide_path = None
        self._navigator_states: list[NonTerminal] = []
        self._current_k_path = None
        self._current_covered_k_paths = set()
        self.compute(history_tree, self.parst_derivations)

    def _get_subgrammar_symbols(self, starting_symbol: NonTerminal):
        reduced_grammar = GrammarReducer(self.grammar.grammar_settings).process(self.grammar.rules, starting_symbol)
        symbols = set(reduced_grammar.keys())
        symbols.update(map(lambda x: x[2], self.grammar.get_protocol_messages(starting_symbol)))
        symbols = set(filter(lambda x: x in self.grammar.rules, symbols))
        return symbols

    def _group_messages_by_nt(self, trees: list[DerivationTree], non_terminals: Optional[set[NonTerminal]] = None):
        if non_terminals is None:
            non_terminals = self.coverage_symbols
        messages: list[DerivationTree] = []
        for tree in trees:
            for subtree in tree.flatten():
                if subtree.symbol in non_terminals:
                    messages.append(subtree)
        messages_by_nt = {}
        for msg in messages:
            messages_by_nt.setdefault(msg.symbol, []).append(msg)
        return messages_by_nt

    @staticmethod
    def _tuple_contains(sub: tuple, full: tuple) -> bool:
        n, m = len(sub), len(full)
        if n == 0:
            return True
        for i in range(m - n + 1):
            if full[i:i + n] == sub:
                return True
        return False


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
        messages_by_nt = self._group_messages_by_nt(self._all_derivation_trees())
        nt_coverage = {}
        for symbol in self.coverage_symbols:
            if symbol not in messages_by_nt:
                nt_coverage[symbol] = 0.0
                continue
            nt_coverage[symbol] = (
                self.grammar.compute_kpath_coverage(
                    messages_by_nt[symbol], k, symbol, False
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
        self, history_tree: DerivationTree, parst_derivations: list[DerivationTree]
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

    def _all_derivation_trees(self):
        all_derivation_trees = list(self.parst_derivations)
        all_derivation_trees.append(self.history_tree)
        return all_derivation_trees

    def _uncovered_paths(self):
        return self.grammar.get_uncovered_k_paths(self._all_derivation_trees(), self.diversity_k, self.start_symbol)

    def _select_next_target_4(self, grammar_starting_symbol: Optional[NonTerminal] = None) -> NonTerminal:
        uncovered_paths = self._uncovered_paths()
        self._hookin_states = []
        for list_idx, path in enumerate(list(uncovered_paths)):
            remaining_path = path
            for path_idx, symbol in enumerate(path[::-1]):
                if symbol in self.coverage_symbols:
                    break
                last_idx = len(path) - path_idx - 1
                remaining_path = remaining_path[:last_idx]
            uncovered_paths[list_idx] = remaining_path
        uncovered_paths = list(filter(lambda x: len(x) > 0, uncovered_paths))
        if len(uncovered_paths) == 0:
            message_nts = self.grammar.get_protocol_messages(self.start_symbol)
            message_coverage = filter(lambda x: x[0] in message_nts, self.coverage_scores)
            message_coverage = list(map(lambda y: y[0], filter(lambda x: x[1] < 1.0, message_coverage)))
            self._navigator_states.clear()
            self._hookin_states.clear()
            self._current_k_path = None
            return message_coverage[0]
        selected_path = random.choice(uncovered_paths)
        if len(selected_path) > 1:
            self._navigator_states = list(selected_path[:-1])
            self._hookin_states = list(self._navigator_states)
        else:
            self._navigator_states.clear()
            self._hookin_states.clear()
        self._current_k_path = selected_path
        return selected_path[-1]

    def _is_tree_contains_paths(self, paths: set[tuple[Symbol, ...]], tree: DerivationTree) -> bool:
        covered_paths = list(self.grammar._extract_k_paths_from_tree(tree, self.diversity_k))
        for list_idx, path in enumerate(list(covered_paths)):
            remaining_path = path
            for path_idx, symbol in enumerate(path[::-1]):
                if symbol in self.coverage_symbols:
                    break
                last_idx = len(path) - path_idx - 1
                remaining_path = remaining_path[:last_idx]
            covered_paths[list_idx] = remaining_path
        covered_paths = list(filter(lambda x: len(x) > 0, covered_paths))
        return len(paths.difference(covered_paths)) == 0


    def _is_can_enter_target_state(self) -> bool:
        for packet in self.get_fuzzer_packets():
            for path in packet.paths:
                is_new_states = list(map(lambda x: x[1], path.path))
                if True not in is_new_states:
                    continue
                first_new_idx = is_new_states.index(True)
                states = list(map(lambda x: x[0], path.path))
                from_scan_idx = first_new_idx - len(self._navigator_states)
                if from_scan_idx < 0:
                    continue
                scan_states = states[from_scan_idx:]
                if PacketSelector._tuple_contains(tuple(self._navigator_states + [self._guide_target]), tuple(scan_states)):
                    return True
        return False

    def _remember_messages(self):
        self._prev_session_msgs = list(map(lambda x: x.msg, self.history_tree.protocol_msgs()))

    def _new_msgs(self, is_new_tree: bool) -> list[DerivationTree]:
        prev_msgs = []
        if is_new_tree:
            prev_msgs = list(map(lambda x: x.msg, self.parst_derivations[-1].protocol_msgs()))
        current_session_msgs = list(map(lambda x: x.msg, self.history_tree.protocol_msgs()))
        all_current_msgs = prev_msgs + current_session_msgs
        new_msgs = []
        for prev, new in zip(self._prev_session_msgs, all_current_msgs):
            if prev != new:
                new_msgs.extend(current_session_msgs)
                return new_msgs
        if len(all_current_msgs) > len(self._prev_session_msgs):
            return all_current_msgs[len(self._prev_session_msgs):]
        return new_msgs

    def _get_next_packet(self):
        return next((x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None)

    def _select_next_packet(self):
        #print(f"LOWEST AT {self.coverage_scores[0][1]} PERCENT ({self.coverage_scores[0][0]})")
        #print(f"START  AT {dict(self.coverage_scores)[NonTerminal("<start>")]} PERCENT")
        #return self.get_fuzzer_packets()

        if len(self.next_fuzzer_parties()) == 0:
            return []

        is_new_tree = len(self.parst_derivations) > self.prev_past_derivations_len
        if is_new_tree:
            self._navigator_states.clear()
            self._current_covered_k_paths.clear()
        self.prev_past_derivations_len = len(self.parst_derivations)
        fuzzable_packets = []
        all_derivations = list(self.parst_derivations)
        all_derivations.append(self.history_tree)


        self._guide_to_end = False
        max_messages_per_tree = 200

        if len(self.history_tree.protocol_msgs()) > max_messages_per_tree:
            log_guidance_hint(
                f"Current tree contains more then {max_messages_per_tree} messages. Guiding to end of tree."
            )
            self._guide_to_end = True
            fuzzable_packets.extend(self._get_guide_to_end_packet())
            return fuzzable_packets

        if len(self.coverage_scores) > 0 and self.coverage_scores[0][1] == 1.0:
            log_guidance_hint("Full coverage reached. Guiding to end of tree.")
            self._guide_to_end = True
            fuzzable_packets.extend(self._get_guide_to_end_packet())
            return fuzzable_packets

        if self._guide_path is None:
            left_path = False
        else:
            left_path = False
            for msg in self._new_msgs(is_new_tree):
                old_next_packet = self._get_next_packet()
                if old_next_packet is None or old_next_packet.symbol != msg.symbol:
                    left_path = True
                    break

                path_to_remove = self._guide_path[:self._guide_path.index(old_next_packet) + 1]
                for symbol in path_to_remove:
                    if len(self._navigator_states) > 0 and symbol == self._navigator_states[0]:
                        self._navigator_states.pop(0)
                self._guide_path = self._guide_path[self._guide_path.index(old_next_packet) + 1:]
            left_path = left_path and not self._is_can_enter_target_state()
            if len(self._guide_path) == 0 and self._current_k_path is not None:
                should_covered_paths = self._current_covered_k_paths.union([self._current_k_path])
                if self._is_tree_contains_paths(should_covered_paths, self.history_tree):
                    self._current_covered_k_paths.add(self._current_k_path)

        if self._guide_target is None or len(self._guide_path) == 0 or left_path:
            self._guide_target = self._select_next_target_4()
            self._guide_path = self.navigator.astar_tree(tree=self.history_tree, destination_symbols=self._navigator_states + [self._guide_target], included_k_paths=self._current_covered_k_paths)
            log_guidance_hint(
                f"Guiding to target {self._guide_target} with score {dict(self.coverage_scores)[self._guide_target]}"
            )

        print(f"LOWEST AT {self.coverage_scores[0][1]} PERCENT ({self.coverage_scores[0][0]})")
        print(f"START  AT {dict(self.coverage_scores)[NonTerminal("<start>")]} PERCENT")

        is_next_symbol_state = next((x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None) is None
        while self._is_can_enter_target_state() and is_next_symbol_state:
            self._guide_target = self._select_next_target_4(self._guide_target)
            self._guide_path = self.navigator.astar_tree(tree=self.history_tree, destination_symbols=self._navigator_states + [self._guide_target], included_k_paths=self._current_covered_k_paths)
            is_next_symbol_state = next((x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None) is None

        self._guide_to_end = any(filter(lambda p: p is None, self._guide_path))
        next_packet = next((x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None)

        if next_packet is None:
            # If no packet needs to be sent to reach the target, we are in a state that contains the target state that we want to reach.
            # We send a packet that adds the target state nonterminal as part of its hookin path.
            fuzzable_packets.extend(self.find_packets())

        elif next_packet.sender in self.next_fuzzer_parties():
            fuzzable_packets.extend(
                self.find_packets(sender=next_packet.sender, packet_symbol=next_packet.symbol))

        if len(fuzzable_packets) == 0:
            fuzzable_packets.extend(self._get_guide_to_end_packet())
        self._remember_messages()
        return fuzzable_packets

    def find_packets(self, *, sender: Optional[str] = None, prev_states: Optional[list[Symbol]] = None, hookin_states: Optional[list[Symbol]] = None, packet_symbol: Optional[NonTerminal] = None) -> list[ForecastingPacket]:
        packets = []
        if prev_states is None:
            prev_states = []
        if hookin_states is None:
            hookin_states = tuple()
        else:
            hookin_states = tuple(hookin_states)

        for current_sender in self.next_fuzzer_parties():
            if sender is not None and current_sender != sender:
                continue
            for packet in self.forecasting_result[current_sender].nt_to_packet.values():
                if packet_symbol is not None and packet.node.symbol != packet_symbol:
                    continue
                append_packet = ForecastingPacket(packet.node)
                for hookin_path in packet.paths:
                    if not self._is_tree_contains_paths(self._current_covered_k_paths, hookin_path.tree):
                        continue
                    match_prev_state = True
                    curr_hookin_path_idx = 0
                    hookin_path_states = tuple(map(lambda y: y[0], hookin_path.path))
                    for state in prev_states:
                        if state not in hookin_path_states[curr_hookin_path_idx:]:
                            match_prev_state = False
                            break
                        curr_hookin_path_idx = hookin_path_states[curr_hookin_path_idx:].index(state)
                    if not match_prev_state:
                        continue
                    packet_hookin_states = tuple(map(lambda y: y[0], filter(lambda x: x[1], hookin_path.path)))
                    if not PacketSelector._tuple_contains(hookin_states, packet_hookin_states):
                        continue
                    append_packet.paths.add(hookin_path)
                if len(append_packet.paths) != 0:
                    packets.append(append_packet)
        return packets
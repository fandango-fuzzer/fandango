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
        self.parst_derivations: set[DerivationTree] = set()
        self.prev_past_derivations_len = 0
        self.history_tree = None
        self._forecasting_result = None
        self._next_packets = None
        self._coverage_scores = None
        self._guide_to_end = False
        self._guide_target = None
        self._guide_path = None
        self._guide_states: list[Symbol] = []
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

    def _compute_coverage_score_perspective(self) -> list[tuple[NonTerminal, float]]:
        messages_by_nt = self._group_messages_by_nt(self._all_derivation_trees())
        controlflow_trees = list(map(lambda x: x[0], self.navigator.get_controlflow_tree(self.history_tree)))
        rule_completion_tester = RuleCompletionTester(self.grammar)


        nt_coverage = {}
        for cov_symbol in self.coverage_symbols:
            if cov_symbol not in messages_by_nt:
                nt_coverage[cov_symbol] = 0.0
                continue
            all_paths = self.grammar._generate_all_k_paths(self.diversity_k, cov_symbol, True)
            for path in list(all_paths):
                if cov_symbol not in path:
                    continue
                idx = path.index(cov_symbol)
                if idx == 0:
                    continue
                existing_prefix = path[:idx]
                any_match = len(controlflow_trees) == 0
                for tree in controlflow_trees:
                    first_symbol = existing_prefix[0]
                    reachable = self.navigator.check_reachability_w_controlflow(tree=tree, symbol=first_symbol)
                    if reachable:
                        any_match = True
                        break
                    symbol_trees = self.history_tree.find_all_nodes(first_symbol, exclude_read_only=False)
                    any_incomplete = False
                    for symbol_tree in symbol_trees:
                        if not rule_completion_tester.check_complete(symbol_tree):
                            inner_symbol_trees = {symbol_tree}
                            for inner_symbol in existing_prefix[1:]:
                                new_inner_symbol_trees = set()
                                for inner_symbol_tree in inner_symbol_trees:
                                    new_inner_symbol_trees.update(inner_symbol_tree.find_all_nodes(inner_symbol, exclude_read_only=False))
                                inner_symbol_trees = new_inner_symbol_trees
                                for inner_symbol_tree in set(inner_symbol_trees):
                                    if rule_completion_tester.check_complete(inner_symbol_tree):
                                        inner_symbol_trees.remove(inner_symbol_tree)
                            if len(inner_symbol_trees) > 0:
                                any_incomplete = True
                                break
                    if any_incomplete:
                        any_match = True
                        break
                    if any_match:
                        break
                if not any_match:
                    all_paths.remove(path)

            covered_k_paths = set()
            for tree in messages_by_nt[cov_symbol]:
                covered_k_paths.update(self.grammar._extract_k_paths_from_tree(tree, self.diversity_k, True))
            covered_k_paths = covered_k_paths.intersection(all_paths)

            if not all_paths:
                nt_coverage[cov_symbol] = 1.0
            else:
                nt_coverage[cov_symbol] = len(covered_k_paths) / len(all_paths)
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


    def _select_next_target_2(self, grammar_starting_symbol: Optional[NonTerminal] = None):
        def shorten_tuples(list1, list2):
            results = []
            for tup in list1:
                longest = 0
                for ref in list2:
                    if tup[:len(ref)] == ref and len(ref) > longest:
                        longest = len(ref)
                results.append((tup[longest:], longest))
            return results

        def is_prefix(a: tuple, b: tuple) -> bool:
            return len(a) <= len(b) and b[:len(a)] == a

        current_guide_states = tuple(self._guide_states)
        uncovered_paths = self._uncovered_paths()
        uncovered_state_paths = []

        # Remove or truncate all parts that are not part of the state model
        for path in uncovered_paths:
            added = False
            for idx, symbol in enumerate(path):
                if symbol not in self.coverage_symbols and idx != 0:
                    uncovered_state_paths.append(path[:idx])
                    added = True
                    break
            if not added:
                uncovered_state_paths.append(path)

        relevant_packets = []
        packets_with_coverage = list()
        # check of each packet, if it can directly cover any uncovered paths
        for party in self.get_next_parties():
            for packet in self.forecasting_result.parties_to_packets[party].nt_to_packet.values():
                append_packet = ForecastingPacket(packet.node)
                packet_covered_paths = set()
                for path in packet.paths:
                    new_path = tuple(map(lambda y: y[0], filter(lambda x: x[1], path.path)))
                    existing_path = tuple(map(lambda y: y[0], filter(lambda x: not x[1], path.path)))
                    # only packets that expand the current search area are taken into account
                    if not is_prefix(current_guide_states, new_path):
                        continue
                    append_packet.paths.add(path)
                    full_path = existing_path + new_path + (packet.node.symbol,)
                    new_covered_paths = set(filter(lambda x: PacketSelector._tuple_contains(x, full_path), uncovered_paths))
                    if len(new_covered_paths) == 0:
                        continue
                    append_packet.paths.add(path)
                    packet_covered_paths.update(new_covered_paths)
                if len(append_packet.paths) == 0:
                    continue
                packet_covered_paths = len(packet_covered_paths)
                packet_covered_paths += len(self.grammar.get_uncovered_k_paths(self._all_derivation_trees(), self.diversity_k, packet.node.symbol))
                packets_with_coverage.append((append_packet, packet_covered_paths))



        direct_reach_paths = set()
        reachable_path_distribution = dict()
        for packet in relevant_packets:
            for path in packet.paths:
                cover = tuple(map(lambda y: y[0], filter(lambda x: x[1], path.path)))
                cover = cover + (packet.node.symbol,)
                direct_reach_paths.add((packet, cover))
        for uncovered_path, covered_len in shortened_paths:
            prefix = next(filter(lambda x: is_prefix(x[1], uncovered_path), direct_reach_paths), None)
            if prefix is not None:
                if prefix[1] not in reachable_path_distribution:
                    reachable_path_distribution[prefix[1]] = {'score': 0, 'node': prefix[0]}
                reachable_path_distribution[prefix[1]]['score'] += 1 + covered_len

        by_next_path_node = dict()
        for path, covered_len in shortened_paths:
            if len(path) == 0:
                continue
            next_node = path[0]
            if next_node not in self.coverage_symbols:
                continue
            if next_node not in by_next_path_node:
                by_next_path_node[next_node] = 0
            by_next_path_node[next_node] += 1 + covered_len

        if grammar_starting_symbol not in self.power_schedules:
            self.power_schedules[grammar_starting_symbol] = PowerSchedule()
        ps = self.power_schedules[grammar_starting_symbol]
        if grammar_starting_symbol is None:
            self._guide_states = []
        else:
            self._guide_states.append(grammar_starting_symbol)
        ps.assign_energy_new(by_next_path_node, reachable_path_distribution)
        new_target = ps.choose()
        ps.add_past_target(new_target)
        return new_target


    def _select_next_target(self, grammar_starting_symbol: Optional[NonTerminal] = None) -> NonTerminal:
        if grammar_starting_symbol not in self.power_schedules:
            self.power_schedules[grammar_starting_symbol] = PowerSchedule()
        ps = self.power_schedules[grammar_starting_symbol]
        if grammar_starting_symbol is None:
            self._guide_states = []
            grammar_starting_symbol = self.start_symbol
        else:
            self._guide_states.append(grammar_starting_symbol)
        grammar_nonterminals = self._get_subgrammar_symbols(grammar_starting_symbol)
        grammar_nonterminals.remove(grammar_starting_symbol)
        coverage_scores = self._compute_coverage_score_perspective()
        coverage_scores = list(filter(lambda x: x[0] in grammar_nonterminals, coverage_scores))
        ps.assign_energy(dict(coverage_scores))
        new_target = ps.choose()
        ps.add_past_target(new_target)
        return new_target

    def _is_appended_target_state(self, tree: DerivationTree) -> bool:
        messages = tree.protocol_msgs()
        if len(messages) > 0:
            last_message = messages[-1]
            return self._guide_target in last_message.get_state_nt()
        return False

    def _is_can_enter_target_state(self) -> bool:
        for packet in self.get_fuzzer_packets():
            for path in packet.paths:
                if PacketSelector._tuple_contains(tuple(self._guide_states + [self._guide_target]), tuple(map(lambda y: y[0], filter(lambda x: x[1], path.path)))):
                    return True
        return False

    def _select_next_packet(self):
        #print(f"LOWEST AT {self.coverage_scores[0][1]} PERCENT ({self.coverage_scores[0][0]})")
        #print(f"START  AT {dict(self.coverage_scores)[NonTerminal("<start>")]} PERCENT")
        #return self.get_fuzzer_packets()
        is_new_tree = len(self.parst_derivations) > self.prev_past_derivations_len
        if is_new_tree:
            self._guide_states.clear()
        self.prev_past_derivations_len = len(self.parst_derivations)
        fuzzable_packets = []
        all_derivations = list(self.parst_derivations)
        all_derivations.append(self.history_tree)

        if len(self.next_fuzzer_parties()) == 0:
            return fuzzable_packets
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
            current_guide_path = self.navigator.astar_tree(tree=self.history_tree, symbol=self._guide_target)
            left_path = not (len(current_guide_path) <= len(self._guide_path) and PacketSelector._tuple_contains(tuple(current_guide_path), tuple(self._guide_path)))
            # any(filter(lambda x: isinstance(x, PacketNonTerminal), self._guide_path)) and
            left_path = left_path and not self._is_can_enter_target_state()
            self._guide_path = current_guide_path

        if self._guide_target is None or left_path:
            self._guide_target = self._select_next_target()
            self._guide_path = self.navigator.astar_tree(tree=self.history_tree, symbol=self._guide_target)
            log_guidance_hint(
                f"Guiding to target {self._guide_target} with score {dict(self.coverage_scores)[self._guide_target]}"
            )

        print(f"LOWEST AT {self.coverage_scores[0][1]} PERCENT ({self.coverage_scores[0][0]})")
        print(f"START  AT {dict(self.coverage_scores)[NonTerminal("<start>")]} PERCENT")

        while self._is_can_enter_target_state() or self._is_appended_target_state(self.history_tree):
            self._guide_target = self._select_next_target(self._guide_target)
            self._guide_path = self.navigator.astar_tree(tree=self.history_tree, symbol=self._guide_target)

        self._guide_to_end = any(filter(lambda p: p is None, self._guide_path))
        next_packet = next((x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None)
        if next_packet is not None:
            packet_idx = self._guide_path.index(next_packet)
            hookin_states = self._guide_path[:packet_idx]
        else:
            hookin_states = self._guide_path

        if next_packet is None:
            # If no packet needs to be sent to reach the target, we are in a state that contains the target state that we want to reach.
            # We send a packet that adds the target state nonterminal as part of its hookin path.
            fuzzable_packets.extend(self.find_packets(prev_states=self._guide_states, hookin_states=hookin_states, packet_symbol=None))

        elif next_packet.sender in self.next_fuzzer_parties():
            fuzzable_packets.extend(
                self.find_packets(sender=next_packet.sender, prev_states=self._guide_states, hookin_states=hookin_states, packet_symbol=next_packet.symbol))

        if len(fuzzable_packets) == 0:
            fuzzable_packets.extend(self._get_guide_to_end_packet())
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
                    match_prev_state = True
                    curr_hookin_path_idx = 0
                    for state in prev_states:
                        if state not in hookin_path.path[curr_hookin_path_idx:]:
                            match_prev_state = False
                            break
                        curr_hookin_path_idx = hookin_path.path[curr_hookin_path_idx].index(state)
                    if not match_prev_state:
                        continue
                    packet_hookin_states = tuple(map(lambda y: y[0], filter(lambda x: x[1], hookin_path.path)))
                    if not PacketSelector._tuple_contains(hookin_states, packet_hookin_states):
                        continue
                    append_packet.paths.add(hookin_path)
                if len(append_packet.paths) != 0:
                    packets.append(append_packet)
        return packets
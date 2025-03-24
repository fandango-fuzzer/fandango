from typing import List, Set

from fandango.language.grammar import Grammar, NodeVisitor, NonTerminalNode, TerminalNode, ParseState, Column, Node, \
    Concatenation, Alternative, Repetition, Option, Plus, Star, CharSet
from fandango.language.symbol import Terminal, NonTerminal
from fandango.language.tree import DerivationTree


class PacketForecaster:
    class ForcastingResult:
        pass

    class GrammarReducer(NodeVisitor):

        def __init__(self):
            self._reduced = dict()

        def process(self, grammar: Grammar):
            self._reduced = dict()
            self.seen_keys = set()
            self.seen_keys.add(NonTerminal("<start>"))
            self.processed_keys = set()
            diff_keys = self.seen_keys - self.processed_keys
            while len(diff_keys) != 0:
                key = diff_keys.pop()
                self._reduced[key] = self.visit(grammar.rules[key])
                self.processed_keys.add(key)
            return self._reduced

        def default_result(self):
            return []

        def aggregate_results(self, aggregate, result):
            aggregate.append(result)
            return aggregate

        def visitConcatenation(self, node: Concatenation):
            return Concatenation(self.visitChildren(node))

        def visitTerminalNode(self, node: TerminalNode):
            return TerminalNode(node.symbol)

        def visitAlternative(self, node: Alternative):
            return Alternative(self.visitChildren(node))

        def visitRepetition(self, node: Repetition):
            return Repetition(self.visit(node), node.expr_data_min, node.expr_data_max)

        def visitOption(self, node: Option):
            return Option(self.visit(node))

        def visitPlus(self, node: Plus):
            return Plus(self.visit(node), node.expr_data_max)

        def visitStar(self, node: Star):
            return Star(self.visit(node), node.expr_data_max)

        def visitCharSet(self, node: CharSet):
            return CharSet(node.chars)

        def visitNonTerminalNode(self, node: NonTerminalNode):
            if node.role is None or node.recipient is None:
                self.seen_keys.add(node.symbol)
                return node

            symbol = NonTerminal("<_packet_" + node.symbol.symbol[1:])
            node = NonTerminalNode(symbol, node.role, node.recipient)
            self._reduced[symbol] = TerminalNode(Terminal(node.symbol.symbol))
            self.seen_keys.add(symbol)
            self.processed_keys.add(symbol)
            return node

    class Parser(Grammar.Parser):

        def __init__(self, grammar: Grammar):
            super().__init__(grammar)
            self.detailed_tree = None

        def construct_incomplete_tree(
            self, state: ParseState, table: List[Set[ParseState] | Column]
        ) -> DerivationTree:
            pass


    def __init__(self, grammar: Grammar):
        g_globals, g_locals = grammar.get_python_env()
        reduced = PacketForecaster.GrammarReducer().process(grammar)
        self.grammar = Grammar(reduced, grammar.fuzzing_mode, g_locals, g_globals)
        self._parser = PacketForecaster.Parser(self.grammar)

    def predict(self, tree: DerivationTree):
        history_nts = ""
        for r_msg in tree.find_role_msgs():
            history_nts += str(r_msg.msg.symbol)
        self._parser.detailed_tree = tree
        tree, table = self._parser.parse(history_nts, NonTerminal("<start>"),
                           Grammar.Parser.ParsingMode.INCOMPLETE,
                           False, True)


        for state in table[len(history_nts)].states:
            if state.dot_params is None:
                continue
            for param in state.dot_params:
                key, val = param
                if key == "role":
                    paths = self._find_paths(state, table, [[state.dot]])
                    break
            # Everything that comes after the second *start* is garbage
            if state.nonterminal == NonTerminal("<start>") and state.dot is None:
                break

    def _find_paths(self, state, table, path):
        if state.nonterminal == NonTerminal("<*start*>"):
            return [path]

        options = table[state.position].dot_map.get(state.nonterminal)
        result = []
        for option in options:
            result.extend(self._find_paths(option, table, [state.nonterminal, *path]))
        return result


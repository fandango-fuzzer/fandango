from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.io.navigation.grammarreducer import GrammarReducer
from fandango.io.navigation.packetiterativeparser import PacketIterativeParser
from fandango.language import Grammar, NonTerminal, DerivationTree, Terminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode


class PacketNavigator(GrammarNavigator):

    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal = NonTerminal("<start>")
    ):
        reduced_rules = GrammarReducer(grammar.grammar_settings).process(
            grammar.rules, start_symbol
        )
        super().__init__(
            Grammar(
                grammar_settings=grammar.grammar_settings,
                rules=reduced_rules,
                fuzzing_mode=grammar.fuzzing_mode,
                local_variables=grammar._local_variables,
                global_variables=grammar._global_variables,
            ),
            start_symbol,
        )
        self._parser = PacketIterativeParser(reduced_rules)
        self.set_message_cost(1)

    def astar_tree(self, tree: DerivationTree, goal_symbol: NonTerminal):
        history_nts = ""
        for r_msg in tree.protocol_msgs():
            assert isinstance(r_msg.msg.symbol, NonTerminal)
            history_nts += r_msg.msg.symbol.name()
        self._parser.detailed_tree = tree
        goal_symbol = Terminal(goal_symbol.name())

        self._parser.new_parse(NonTerminal("<start>"), ParsingMode.INCOMPLETE)
        paths = []
        if history_nts == "":
            path = super().astar_tree(DerivationTree(NonTerminal("<start>")), goal_symbol)
            if path is not None:
                paths.append(path)
        for suggested_tree in self._parser.consume(history_nts):
            for orig_r_msg, r_msg in zip(
                tree.protocol_msgs(), suggested_tree.protocol_msgs()
            ):
                assert isinstance(r_msg.msg.symbol, NonTerminal)
                assert isinstance(orig_r_msg.msg.symbol, NonTerminal)
                if (
                    r_msg.msg.symbol.name()[9:] == orig_r_msg.msg.symbol.name()[1:]
                    and r_msg.sender == orig_r_msg.sender
                    and r_msg.recipient == orig_r_msg.recipient
                ):
                    pass  # Todo set children for computed length repetitions
                else:
                    break
            else:
                path = super().astar_tree(suggested_tree, goal_symbol)
                if path is None:
                    continue
                paths.append(path)
        for i, path in enumerate(paths):
            path = list(filter(lambda n: isinstance(n.node, NonTerminalNode), path))
            path = list(filter(lambda n: n.node.sender is not None, path))
            path = list(
                map(
                    lambda n: (n.node.sender, n.node.recipient, NonTerminal(f"<{str(n.node.symbol.value())[9:]}")),
                    path,
                )
            )
            paths[i] = path

        paths.sort(key=lambda path: len(path))
        if len(paths) == 0:
            return None
        return paths[0]

from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols.non_terminal import NonTerminal


class MessageNestingDetector(NodeVisitor):
    def __init__(self, grammar: "Grammar"):
        self.grammar = grammar
        self.seen_nt: set[NonTerminal] = set()
        self.current_path: list[NonTerminal] = []

    def fail_on_nested_packet(self, start_symbol: NonTerminal):
        self.current_path.append(start_symbol)
        self.visit(self.grammar[start_symbol])
        self.current_path.pop()

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol not in self.seen_nt:
            self.seen_nt.add(node.symbol)
        elif node.sender is not None and node.symbol in self.current_path:
            str_path = [str(p) for p in self.current_path]
            raise RuntimeError(
                f"Found illegal packet-definitions within packet-definition of non_terminal {node.symbol}! DerivationPath: "
                + " -> ".join(str_path)
            )
        else:
            return

        if node.sender is not None:
            parties = self.grammar[node.symbol].msg_parties(include_recipients=False)
            if len(parties) != 0:
                raise RuntimeError(
                    f"Found illegal packet-definitions within packet-definition of non_terminal {node.symbol}: "
                    + ", ".join(parties)
                )
            return
        self.current_path.append(node.symbol)
        self.visit(self.grammar[node.symbol])
        self.current_path.pop()

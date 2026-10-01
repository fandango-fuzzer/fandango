from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols.non_terminal import NonTerminal


class RuleRecursionTester:

    def __init__(self, rules: dict[NonTerminal, Node]):
        self._references = {
            symbol: self.referenced_symbols(body) for symbol, body in rules.items()
        }
        self._derivable_by_symbol: dict[NonTerminal, set[NonTerminal]] = {}

    @staticmethod
    def referenced_symbols(body: Node) -> set[NonTerminal]:
        """All symbols in a rule body."""
        referenced = set()
        pending = [body]
        while pending:
            node = pending.pop()
            if isinstance(node, NonTerminalNode):
                referenced.add(node.symbol)
            else:
                pending.extend(node.children())
        return referenced

    def is_recursive_call(self, calling_symbol: NonTerminal, called_symbol: NonTerminal) -> bool:
        """True if the reference from calling_symbol to called_symbol is a recursive call."""
        derivable = self._derivable_by_symbol.get(called_symbol)
        if derivable is None:
            derivable = set()
            pending = [called_symbol]
            while pending:
                for symbol in self._references.get(pending.pop(), ()):
                    if symbol not in derivable:
                        derivable.add(symbol)
                        pending.append(symbol)
            self._derivable_by_symbol[called_symbol] = derivable
        return calling_symbol in derivable

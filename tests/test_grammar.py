import random
import unittest
from typing import Dict, Tuple, Union, List

from fandango.language.grammar import NodeVisitor, TerminalNode, NonTerminalNode, Concatenation, Alternative, CharSet, \
    Option, Plus, Star, Repetition, Node
from fandango.language.parse import parse
from fandango.language.symbol import Terminal, NonTerminal


class Disambiguator(NodeVisitor):
    def __init__(self):
        self.path_manifestations = {}

    def visit(self, node: Node) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return super().visit(node)

    def visitAlternative(self, node: Alternative) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        child_endpoints = {}
        for child in node.children():
            endpoints: Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]] = self.visit(child)
            for children in endpoints:
                # prepend the alternative to all paths
                if not children in child_endpoints:
                    child_endpoints[children] = []
                # join observed paths (these are impossible to disambiguate)
                child_endpoints[children].extend((node,) + path for path in endpoints[children])

        return child_endpoints


    def visitConcatenation(self, node: Concatenation) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        child_endpoints = {(): []}
        for child in node.children():
            next_endpoints = {}
            endpoints: Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]] = self.visit(child)
            for children in endpoints:
                for existing in child_endpoints:
                    concatenation = existing + children
                    if not concatenation in next_endpoints:
                        next_endpoints[concatenation] = []
                    next_endpoints[concatenation].extend(child_endpoints[existing])
                    next_endpoints[concatenation].extend(endpoints[children])
            child_endpoints = next_endpoints

        return {children: [(node,) + path for path in child_endpoints[children]] for children in child_endpoints}


    def visitRepetition(self, node: Repetition) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        # repetitions are alternatives over concatenations
        implicit_alternative = Alternative(
            [Concatenation([node.node] * r) for r in range(node.min, node.max)]
        )
        return self.visit(implicit_alternative)

    def visitStar(self, node: Star) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitOption(self, node: Option) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        implicit_alternative = Alternative(
            [Concatenation([]), Concatenation([node.node])]
        )
        return self.visit(implicit_alternative)

    def visitNonTerminalNode(self, node: NonTerminalNode) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitTerminalNode(self, node: TerminalNode) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitCharSet(self, node: CharSet) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(Terminal(c),): [(node, TerminalNode(Terminal(c)))] for c in node.chars}


class ConstraintTest(unittest.TestCase):
    GRAMMAR = """
<start> ::= <ab>;
<ab> ::= 
      "a" <ab> 
    | <ab> "b"
    | ""
    ;
"""

    def test_generate_k_paths(self):
        grammar = parse(self.GRAMMAR)[0]

        kpaths = grammar._generate_all_k_paths(3)
        print(len(kpaths))

        for path in grammar._generate_all_k_paths(3):
            print(tuple(path))

    def test_derivation_k_paths(self):
        grammar = parse(self.GRAMMAR)[0]

        random.seed(0)
        tree = grammar.fuzz()
        print([t.symbol for t in tree.flatten()])

    def test_parse(self):
        grammar = parse(self.GRAMMAR)[0]
        tree = grammar.parse("aabb")

        work = [(None, tree)]
        visited = []
        while work:
            entry = work.pop(0)
            visited.append(entry)
            parent, entry = entry
            work.extend((len(visited) - 1, child) for child in entry.children)

        by_idx = {}
        for idx, (parent, entry) in enumerate(visited):
            if entry.children:
                by_idx[idx] = []
            if parent is not None:
                if not parent in by_idx:
                    by_idx[parent] = []
                by_idx[parent].append(idx)

        # visited now represents the level traversal w/ child order and parent backref
        print(by_idx)

        disambiguator = Disambiguator()

        path_segments = []
        for (parent, entry) in visited:
            if len(entry.children) != 0:
                path_segments.append(disambiguator.visit(grammar.rules[entry.symbol])[tuple(c.symbol for c in entry.children)])
            else:
                path_segments.append(None)

        for ((parent, entry), segment) in zip(visited, path_segments):
            print(parent, entry.symbol, entry.children, segment)

from copy import deepcopy
from typing import Optional
from collections.abc import Generator

from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.grammar.nodes.node import Node
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class Parser:
    def __init__(self, grammar_rules: dict[NonTerminal, Node]):
        self._iter_parser = IterativeParser(grammar_rules)
        self._cache: dict[
            tuple[
                str | bytes,
                NonTerminal,
                ParsingMode,
                Optional[DerivationTree],
            ],
            list[DerivationTree],
        ] = {}

    def _parse_forest(
        self,
        word: str | bytes,
        start: str | NonTerminal = "<start>",
        *,
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        starter_bit=-1,
    ):
        """
        Parse a forest of input trees from `word`.
        `start` is the start symbol (default: `<start>`).
        if `allow_incomplete` is True, the function will return trees even if the input ends prematurely.
        """
        self._iter_parser.new_parse(start, mode, hookin_parent, starter_bit)
        yield from self._iter_parser.consume(word)

    def parse_forest(
        self,
        word: str | bytes | int | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        include_controlflow: bool = False,
    ) -> Generator[DerivationTree, None, None]:
        """
        Yield multiple parse alternatives, using a cache.
        """
        starter_bit = -1
        if isinstance(word, DerivationTree):
            if word.contains_bits():
                starter_bit = (word.count_terminals() - 1) % 8
            if word.should_be_serialized_to_bytes():
                bit_string = word.to_bits()
                word = int(bit_string, 2).to_bytes(
                    (len(bit_string) + 7) // 8, byteorder="big"
                )
            else:
                word = word.to_string()
        if isinstance(word, int):
            word = str(word)
        assert isinstance(word, (str, bytes)), type(word)

        if isinstance(start, str):
            start = NonTerminal(start)

        cache_key = (word, start, mode, hookin_parent)
        forest: list[DerivationTree]
        if cache_key in self._cache:
            forest = self._cache[cache_key]
            for tree in forest:
                tree = deepcopy(tree)
                if not include_controlflow:
                    collapsed = self.collapse(tree)
                    if collapsed is not None:
                        yield collapsed
            return

        for tree in self._parse_forest(
            word,
            start,
            mode=mode,
            hookin_parent=hookin_parent,
            starter_bit=starter_bit,
        ):
            tree = self._iter_parser.to_derivation_tree(tree)
            if cache_key in self._cache:
                self._cache[cache_key].append(tree)
            else:
                self._cache[cache_key] = [tree]
            if include_controlflow:
                yield tree
            else:
                collapsed = self.collapse(tree)
                if collapsed is not None:
                    yield collapsed

    def parse_multiple(
        self,
        word: str | bytes | int | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        include_controlflow: bool = False,
    ) -> Generator[DerivationTree, None, None]:
        """
        Yield multiple parse alternatives,
        even for incomplete inputs
        """
        return self.parse_forest(
            word,
            start,
            mode=mode,
            hookin_parent=hookin_parent,
            include_controlflow=include_controlflow,
        )

    def parse(
        self,
        word: str | bytes | int | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        include_controlflow: bool = False,
    ) -> Optional[DerivationTree]:
        """
        Return the first parse alternative,
        or `None` if no parse is possible
        """
        tree_gen = self.parse_multiple(
            word,
            start=start,
            mode=mode,
            hookin_parent=hookin_parent,
            include_controlflow=include_controlflow,
        )
        return next(tree_gen, None)

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._iter_parser.collapse(tree)

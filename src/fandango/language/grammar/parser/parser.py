import gc
import os
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from copy import deepcopy
from typing import Optional

from cachetools import LRUCache

from fandango.language.grammar import ParsingMode
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.grammar.parser.rust_iterative_parser import RustIterativeParser
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.utils import cache_size


@contextmanager
def _gc_paused() -> Iterator[None]:
    """
    Pause the cyclic garbage collector for the duration of the block.
    """
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        yield
    finally:
        if was_enabled:
            gc.enable()


#: Parser backends: the Python Earley parser, or its Rust port.
PARSER_BACKENDS: dict[str, type[IterativeParser] | type[RustIterativeParser]] = {
    "python": IterativeParser,
    "rust": RustIterativeParser,
}


def default_parser_backend() -> str:
    """The backend `Parser` uses by default; set with `FANDANGO_PARSER`."""
    return os.environ.get("FANDANGO_PARSER", "python")


class Parser:
    def __init__(
        self,
        grammar_rules: dict[NonTerminal, Node],
        backend: Optional[str] = None,
    ):
        self._grammar_rules = grammar_rules
        self.backend = backend or default_parser_backend()
        if self.backend not in PARSER_BACKENDS:
            raise ValueError(
                f"Unknown parser backend {self.backend!r}; "
                f"choose one of {sorted(PARSER_BACKENDS)}"
            )
        self._iter_parser_class = PARSER_BACKENDS[self.backend]
        self._iter_parser = self._iter_parser_class(grammar_rules)
        self._iter_parsers_by_start: dict[
            NonTerminal, IterativeParser | RustIterativeParser
        ] = {}
        self._cache: LRUCache[
            tuple[
                str | bytes,
                NonTerminal,
                ParsingMode,
                int,
            ],
            DerivationTree,
        ] = LRUCache(maxsize=cache_size())

    def _parse_forest(
        self,
        word: str | bytes,
        start: str | NonTerminal = "<start>",
        *,
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        starter_bit: int = -1,
    ) -> Generator[DerivationTree, None, None]:
        """
        Parse a forest of input trees from `word`.
        `start` is the start symbol (default: `<start>`).
        In `ParsingMode.INCOMPLETE`, trees are yielded even if the input ends prematurely.
        """
        self._iter_parser.new_parse(start, mode, hookin_parent, starter_bit)
        self._iter_parser.consume(word)
        for tree, _is_complete in self._iter_parser.tree_at(
            self._iter_parser.consumed_length(),
            incomplete=mode == ParsingMode.INCOMPLETE,
        ):
            yield tree

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
                word = int(bit_string, 2).to_bytes((len(bit_string) + 7) // 8)
            else:
                word = word.to_string()
        if isinstance(word, int):
            word = str(word)
        assert isinstance(word, (str, bytes)), type(word)

        if isinstance(start, str):
            start = NonTerminal(start)

        cache_key = (word, start, mode, hash(hookin_parent))
        last_yielded_tree = self._cache.get(cache_key)
        if last_yielded_tree is not None:
            with _gc_paused():
                tree = deepcopy(last_yielded_tree)
                result = tree if include_controlflow else self.collapse(tree)
            if result is not None:
                yield result

        trees = self._parse_forest(
            word,
            start,
            mode=mode,
            hookin_parent=hookin_parent,
            starter_bit=starter_bit,
        )
        while True:
            with _gc_paused():
                parsed = next(trees, None)
                if parsed is None:
                    break
                if last_yielded_tree is not None and hash(parsed) == hash(
                    last_yielded_tree
                ):
                    continue
                result = (
                    deepcopy(parsed) if include_controlflow else self.collapse(parsed)
                )
            if result is not None:
                self._cache[cache_key] = parsed
                yield result

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

    def iterative_parser(
        self, start: NonTerminal
    ) -> IterativeParser | RustIterativeParser:
        if start not in self._iter_parsers_by_start:
            self._iter_parsers_by_start[start] = self._iter_parser_class(
                self._grammar_rules
            )
        return self._iter_parsers_by_start[start]

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._iter_parser.collapse(tree)

import re

from copy import deepcopy
from typing import IO, Optional


from fandango.language.parse.io import init_io
from fandango.language.parse.slice_parties import slice_parties

from fandango.errors import FandangoValueError
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.language.grammar import FuzzingMode, closest_match
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.symbol_finder import SymbolFinder
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.parse.parse_spec import parse_content
from fandango.language.search import (
    AnnotatedSearch,
    DescendantAttributeSearch,
    ItemSearch,
)
from fandango.language.stdlib import stdlib
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree_value import TreeValueType
from fandango.logger import LOGGER

# Save the standard library grammar and constraints
STDLIB_GRAMMAR: Optional[Grammar] = None
STDLIB_CONSTRAINTS: Optional[list[Constraint | SoftValue]] = None


def parse(
    fan_files: str | IO[str] | list[str | IO[str]],
    constraints: Optional[list[str]] = None,
    *,
    use_cache: bool = True,
    use_stdlib: bool = True,
    check: bool = True,
    lazy: bool = False,
    given_grammars: list[Grammar] = [],
    start_symbol: Optional[str] = None,
    includes: Optional[list[str]] = [],
    parties: Optional[list[str]] = None,
    max_repetitions: int = 5,
) -> tuple[Optional[Grammar], list[Constraint | SoftValue]]:
    """
    Parse .fan content, handling multiple files, standard library, and includes.
    :param fan_files: One (open) .fan file, one string, or a list of these
    :param constraints: List of constraints (as strings); default: []
    :param use_cache: If True (default), cache parsing results
    :param use_stdlib: If True (default), use the standard library
    :param check: If True (default), the constraints are checked for consistency
    :param lazy: If True, the constraints are evaluated lazily
    :param given_grammars: Grammars to use in addition to the standard library
    :param start_symbol: The grammar start symbol (default: "<start>")
    :param includes: A list of directories to search for include files; default: []
    :param parties: If given, list of parties to consider in the grammar
    :param max_repetitions: The maximal number of repetitions
    :return: A tuple of the grammar and constraints
    """

    if not isinstance(fan_files, list):
        fan_files = [fan_files]

    if not fan_files and not constraints:
        return None, []

    if constraints is None:
        constraints = []

    if includes is None:
        includes = []

    if start_symbol is None:
        start_symbol = "<start>"

    global STDLIB_SYMBOLS, STDLIB_GRAMMAR, STDLIB_CONSTRAINTS
    if use_stdlib and STDLIB_GRAMMAR is None:
        LOGGER.debug("Reading standard library")
        stdlib_spec = parse_content(
            stdlib,
            filename="<stdlib>",
            use_cache=use_cache,
            max_repetitions=max_repetitions,
        )
        STDLIB_GRAMMAR = stdlib_spec.grammar
        STDLIB_CONSTRAINTS = stdlib_spec.constraints

    used_symbols = set()
    if use_stdlib:
        assert STDLIB_GRAMMAR is not None
        for symbol in STDLIB_GRAMMAR.rules.keys():
            # Do not complain about unused symbols in the standard library
            used_symbols.add(symbol.name())

    grammars = []
    parsed_constraints: list[Constraint | SoftValue] = []
    if use_stdlib:
        assert STDLIB_GRAMMAR is not None
        assert STDLIB_CONSTRAINTS is not None
        try:
            grammars = [deepcopy(STDLIB_GRAMMAR)]
        except TypeError:
            # This can happen if we invoke parse() from a notebook
            grammars = [STDLIB_GRAMMAR]
        parsed_constraints = STDLIB_CONSTRAINTS.copy()

    grammars += given_grammars

    LOGGER.debug("Reading files")

    mode = FuzzingMode.COMPLETE

    for fan_file in fan_files:
        if isinstance(fan_file, str):
            fan_contents = fan_file
            name = "<string>"
        else:
            fan_contents = fan_file.read()
            name = fan_file.name
        LOGGER.debug(f"Reading {name}")
        new_spec = parse_content(
            fan_contents,
            filename=name,
            use_cache=use_cache,
            lazy=lazy,
            max_repetitions=max_repetitions,
            used_symbols=used_symbols,
        )
        parsed_constraints += new_spec.constraints
        new_grammar = new_spec.grammar
        assert new_grammar is not None
        if new_grammar.fuzzing_mode == FuzzingMode.IO:
            mode = FuzzingMode.IO

        grammars.append(new_grammar)

    LOGGER.debug(f"Processing {len(grammars)} grammars")
    grammar = grammars[0]
    LOGGER.debug(f"Grammar #1: {[key.name() for key in grammar.rules.keys()]}")
    n = 2
    for g in grammars[1:]:
        LOGGER.debug(f"Grammar #{n}: {[key.name() for key in g.rules.keys()]}")

        for symbol in g.rules.keys():
            if symbol in grammar.rules:
                LOGGER.info(f"Redefining {symbol.name()}")

        grammar.update(g, prime=False)
        n += 1

    LOGGER.debug(f"Final grammar: {[key.name() for key in grammar.rules.keys()]}")

    grammar.fuzzing_mode = mode
    LOGGER.debug(f"Grammar fuzzing mode: {grammar.fuzzing_mode}")

    LOGGER.debug("Processing constraints")
    for constraint in constraints or []:
        LOGGER.debug(f"Constraint {constraint}")
        first_token = constraint.split()[0]
        if any(
            first_token.startswith(kw) for kw in ["where", "minimizing", "maximizing"]
        ):
            new_spec = parse_content(
                constraint, filename=constraint, use_cache=use_cache, lazy=lazy
            )
        else:
            new_spec = parse_content(
                "where " + constraint,
                filename=constraint,
                use_cache=use_cache,
                lazy=lazy,
            )
        parsed_constraints += new_spec.constraints

    if check:
        LOGGER.debug("Checking and finalizing content")
        if grammar and len(grammar.rules) > 0:
            check_grammar_consistency(
                grammar, given_used_symbols=used_symbols, start_symbol=start_symbol
            )

        if grammar and parsed_constraints:
            check_constraints_existence(grammar, parsed_constraints)

    global_env, local_env = grammar.get_spec_env()

    if not parties and grammar.fuzzing_mode == FuzzingMode.IO:
        init_io(global_env, local_env, grammar, start_symbol)

    # We invoke this at the very end, now that all data is there
    grammar.update(grammar, prime=check)

    if parties:
        slice_parties(grammar, set(parties), ignore_receivers=True)

    LOGGER.debug("All contents parsed")
    return grammar, parsed_constraints


### Consistency Checks


def check_grammar_consistency(
    grammar: Grammar,
    *,
    given_used_symbols: set[str] = set(),
    start_symbol: str = "<start>",
) -> None:
    check_grammar_definitions(
        grammar, given_used_symbols=given_used_symbols, start_symbol=start_symbol
    )
    check_grammar_types(grammar, start_symbol=start_symbol)


def check_grammar_definitions(
    grammar: Grammar,
    *,
    given_used_symbols: set[str] = set(),
    start_symbol: str = "<start>",
) -> None:
    if not grammar:
        return

    LOGGER.debug("Checking grammar")

    used_symbols: set[str] = set()
    undefined_symbols: set[str] = set()
    defined_symbols: set[str] = set()

    defined_symbols.update(map(lambda x: x.name(), grammar.rules.keys()))

    if start_symbol not in defined_symbols:
        if start_symbol == "<start>":
            raise FandangoValueError(
                f"Start symbol {start_symbol!s} not defined in grammar"
            )
        closest = closest_match(start_symbol, defined_symbols)
        raise FandangoValueError(
            f"Start symbol {start_symbol!r} not defined in grammar. Did you mean {closest!r}?"
        )

    def collect_used_symbols(node: Node) -> None:
        if node.is_nonterminal:
            used_symbols.add(node.symbol.name())  # type: ignore[attr-defined] # We're checking types manually
        elif (
            node.node_type == NodeType.REPETITION
            or node.node_type == NodeType.STAR
            or node.node_type == NodeType.PLUS
            or node.node_type == NodeType.OPTION
        ):
            collect_used_symbols(node.node)  # type: ignore[attr-defined] # We're checking types manually

        for child in node.children():
            collect_used_symbols(child)

    for tree in grammar.rules.values():
        collect_used_symbols(tree)

    for symbol in used_symbols:
        if symbol not in defined_symbols:
            undefined_symbols.add(symbol)

    for symbol in defined_symbols:
        if (
            symbol not in used_symbols
            and symbol not in given_used_symbols
            and symbol != start_symbol
            and symbol != "<start>"  # Allow <start> to be defined but not used
        ):
            LOGGER.warning(f"Symbol {symbol!s} defined, but not used")

    if undefined_symbols:
        first_undefined_symbol = undefined_symbols.pop()
        error = FandangoValueError(
            f"Undefined symbol {first_undefined_symbol!s} in grammar"
        )
        if undefined_symbols:
            if getattr(Exception, "add_note", None):
                # Python 3.11+ has add_note() method
                error.add_note(
                    f"Other undefined symbols: {', '.join(undefined_symbols)}"
                )
        raise error


def check_grammar_types(
    grammar: Optional[Grammar], *, start_symbol: str = "<start>"
) -> None:
    if grammar is None:
        return

    LOGGER.debug("Checking types")

    symbol_types: dict[Symbol, tuple[Optional[str], int, int, int]] = {}

    def compatible(tp1: str, tp2: str) -> bool:
        if tp1 in ["int", "bytes"] and tp2 in ["int", "bytes"]:
            return True
        return tp1 == tp2

    def get_type(tree: Node, rule_symbol: str) -> tuple[Optional[str], int, int, int]:
        # LOGGER.debug(f"Checking type of {tree!s} in {rule_symbol!s} ({tree.node_type!s})")
        nonlocal symbol_types, grammar

        tp: Optional[str]
        if isinstance(tree, TerminalNode):
            tp = type(tree.symbol).__name__
            # LOGGER.debug(f"Type of {tree.symbol.symbol!r} is {tp!r}")
            bits = 1 if tree.symbol.is_type(TreeValueType.TRAILING_BITS_ONLY) else 0
            return tp, bits, bits, 0

        elif (
            isinstance(tree, Repetition)
            or isinstance(tree, Star)
            or isinstance(tree, Plus)
            or isinstance(tree, Option)
        ):
            tp, min_bits, max_bits, step = get_type(tree.node, rule_symbol)
            # if min_bits % 8 != 0 and tree.min == 0:
            #     raise FandangoValueError(f"{rule_symbol!s}: Bits cannot be optional")

            rep_min = tree.min
            rep_max = tree.max

            step = min(min_bits, max_bits)
            return tp, rep_min * min_bits, rep_max * max_bits, step

        elif isinstance(tree, NonTerminalNode):
            if tree.symbol in symbol_types:
                return symbol_types[tree.symbol]

            symbol_types[tree.symbol] = (None, 0, 0, 0)
            assert grammar is not None
            symbol_tree = grammar.rules[tree.symbol]
            tp, min_bits, max_bits, step = get_type(symbol_tree, tree.symbol.name())
            symbol_types[tree.symbol] = tp, min_bits, max_bits, step
            # LOGGER.debug(f"Type of {tree.symbol!s} is {tp!r} with {min_bits}..{max_bits} bits")
            return tp, min_bits, max_bits, step

        elif (
            tree.node_type == NodeType.CONCATENATION
            or tree.node_type == NodeType.ALTERNATIVE
        ):
            common_tp = None
            tp_child = None
            first = True
            min_bits = 0
            max_bits = 0
            step = 0
            for child in tree.children():
                tp, min_child_bits, max_child_bits, child_step = get_type(
                    child, rule_symbol
                )
                if first:
                    min_bits = min_child_bits
                    max_bits = max_child_bits
                    step = child_step
                    first = False
                elif tree.node_type == NodeType.CONCATENATION:
                    min_bits += min_child_bits
                    max_bits += max_child_bits
                    step += child_step
                else:  # NodeType.ALTERNATIVE
                    min_bits = min(min_bits, min_child_bits)
                    max_bits = max(max_bits, max_child_bits)
                    step += min(step, child_step)
                if tp is None:
                    continue
                if common_tp is None:
                    common_tp = tp
                    tp_child = child
                    continue
                if not compatible(tp, common_tp):
                    if tree.node_type == NodeType.CONCATENATION:
                        LOGGER.warning(
                            f"{rule_symbol!s}: Concatenating {common_tp!r} ({tp_child!s}) and {tp!r} ({child!s})"
                        )
                    else:
                        LOGGER.warning(
                            f"{rule_symbol!s}: Type can be {common_tp!r} ({tp_child!s}) or {tp!r} ({child!s})"
                        )
                    common_tp = tp

            # LOGGER.debug(f"Type of {rule_symbol!s} is {common_tp!r} with {min_bits}..{max_bits} bits")
            return common_tp, min_bits, max_bits, step

        raise FandangoValueError("Unknown node type")

    start_tree = grammar.rules[NonTerminal(start_symbol)]
    _, min_start_bits, max_start_bits, start_step = get_type(start_tree, start_symbol)
    if start_step > 0 and any(
        bits % 8 != 0 for bits in range(min_start_bits, max_start_bits + 1, start_step)
    ):
        if min_start_bits != max_start_bits:
            LOGGER.warning(
                f"{start_symbol!s}: Number of bits ({min_start_bits}..{max_start_bits}) may not be a multiple of eight"
            )
        else:
            LOGGER.warning(
                f"{start_symbol!s}: Number of bits ({min_start_bits}) is not a multiple of eight"
            )


def check_constraints_existence(
    grammar: Grammar, constraints: list[Constraint | SoftValue]
) -> None:
    LOGGER.debug("Checking constraints")

    indirect_child: dict[str, dict[str, Optional[bool]]] = {
        k.name(): {l.name(): None for l in grammar.rules.keys()}  # noqa: E741
        for k in grammar.rules.keys()
    }

    defined_symbols = []
    for symbol in grammar.rules.keys():
        defined_symbols.append(symbol.name())

    grammar_symbols = grammar.rules.keys()
    grammar_matches = re.findall(
        r"<([^>]*)>", "".join(k.format_as_spec() for k in grammar_symbols)
    )
    # LOGGER.debug(f"All used symbols: {grammar_matches}")

    for constraint in constraints:
        constraint_symbols = constraint.get_symbols()

        for value in constraint_symbols:
            # LOGGER.debug(f"Constraint {constraint}: Checking {value}")

            constraint_matches = re.findall(
                r"<([^>]*)>", value.format_as_spec()
            )  # was <(.*?)>

            missing = [
                match for match in constraint_matches if match not in grammar_matches
            ]

            if missing:
                first_missing_symbol = missing[0]
                closest = closest_match(first_missing_symbol, defined_symbols)

            if len(missing) > 1:
                missing_symbols = ", ".join(
                    ["<" + str(symbol) + ">" for symbol in missing]
                )
                error = FandangoValueError(
                    f"{constraint}: undefined symbols {missing_symbols}. Did you mean {closest!r}?"
                )
                raise error

            if len(missing) == 1:
                missing_symbol = missing[0]
                error = FandangoValueError(
                    f"{constraint}: undefined symbol <{missing_symbol!r}>. Did you mean {closest!r}?"
                )
                raise error

            for i in range(len(constraint_matches) - 1):
                parent = constraint_matches[i]
                symbol = constraint_matches[i + 1]
                # This handles <parent>[...].<symbol> as <parent>..<symbol>.
                # We could also interpret the actual [...] contents here,
                # but slices and chains could make this hard -- AZ
                recurse = (
                    isinstance(value, DescendantAttributeSearch)
                    or isinstance(value, ItemSearch)
                    or (
                        isinstance(value, AnnotatedSearch)
                        and (
                            isinstance(value.inner, DescendantAttributeSearch)
                            or isinstance(value.inner, ItemSearch)
                        )
                    )
                )
                if not check_constraints_existence_children(
                    grammar, parent, symbol, recurse, indirect_child
                ):
                    msg = f"{constraint.format_as_spec()}: <{parent!s}> has no child <{symbol!s}>"
                    raise FandangoValueError(msg)


def check_constraints_existence_children(
    grammar: Grammar,
    parent: str,
    symbol: str,
    recurse: bool,
    indirect_child: dict[str, dict[str, Optional[bool]]],
) -> Optional[bool]:
    # LOGGER.debug(f"Checking if <{symbol}> is a child of <{parent}>")

    if indirect_child[f"<{parent}>"][f"<{symbol}>"] is not None:
        return indirect_child[f"<{parent}>"][f"<{symbol}>"]

    grammar_symbols = grammar.rules[NonTerminal(f"<{parent}>")]

    # Original code; fails on <a> "b" <c> -- AZ
    # grammar_matches = re.findall(r'(?<!")<([^>]*)>(?!".*)',
    #                              str(grammar_symbols))
    #
    # Simpler version; may overfit (e.g. matches <...> in strings),
    # but that should not hurt us -- AZ
    finder = SymbolFinder()
    finder.visit(grammar_symbols)
    non_terminals = [nt.symbol.name()[1:-1] for nt in finder.nonTerminalNodes]

    if symbol in non_terminals:
        indirect_child[f"<{parent}>"][f"<{symbol}>"] = True
        return True

    is_child = False
    for match in non_terminals:
        if recurse or match.startswith("_"):
            is_child = (
                is_child
                or check_constraints_existence_children(
                    grammar, match, symbol, recurse, indirect_child
                )
                is True
            )
    indirect_child[f"<{parent}>"][f"<{symbol}>"] = is_child
    return is_child

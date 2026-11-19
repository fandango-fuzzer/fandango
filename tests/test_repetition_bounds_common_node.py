from fandango.constraints.repetition_bounds import _get_first_common_node
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.symbols.terminal import Terminal
from fandango.language.tree import DerivationTree


def tree(name: str, *children: DerivationTree) -> DerivationTree:
    return DerivationTree(NonTerminal(f"<{name}>"), list(children))


def leaf(text: str) -> DerivationTree:
    return DerivationTree(Terminal(text))


def test_common_node_of_two_nodes_in_one_tree() -> None:
    a, b = tree("a", leaf("1")), tree("b", leaf("2"))
    inner = tree("inner", a, b)
    root = tree("start", tree("x", leaf("0")), inner)
    assert _get_first_common_node(a, b) is inner
    assert _get_first_common_node(a, root.children[0]) is root


def test_common_node_inside_the_source_of_a_generator() -> None:
    """Both nodes are below a tree that a generator was called with. The way to
    them leads through `sources`, not through `children`, at one step."""
    count, body = tree("count", leaf("2")), tree("body", leaf("ab"))
    view = tree("view", tree("pad", leaf("-")), tree("pair", count, body))
    generated = tree("generated", leaf("zz"))
    generated.sources = [view]
    tree("start", tree("head", leaf("h")), generated)

    assert _get_first_common_node(count, body) is view.children[1]
    assert _get_first_common_node(view.children[0], body) is view

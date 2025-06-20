# wildcard import required for usage in spec files
from fandango.io import *  # noqa: F403
from fandango.language.symbol import NonTerminal


# Importing '*' here, because all functions, and classes existing in the io file, need to be available within spec files


def is_int(x):
    if isinstance(x, DerivationTree):
        return x.is_int()
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True


def is_float(x):
    if isinstance(x, DerivationTree):
        return x.is_float()
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def is_num(x):
    if isinstance(x, DerivationTree):
        return x.is_num()
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def is_complex(x):
    if isinstance(x, DerivationTree):
        return x.is_complex()
    try:
        complex(x)
    except ValueError:
        return False
    else:
        return True


def is_before(
    tree: DerivationTree, before_tree: DerivationTree, after_tree: DerivationTree
):
    """
    Check if the tree is before the before_tree and after the after_tree.
    """
    before_index = tree.get_index(before_tree)
    after_index = tree.get_index(after_tree)
    if before_index < 0 or after_index < 0:
        return False
    return before_index < after_index


def is_after(
    tree: DerivationTree, after_tree: DerivationTree, before_tree: DerivationTree
):
    """
    Check if the tree is after the after_tree and before the before_tree.
    """
    return is_before(tree, before_tree, after_tree)


def get_index_within(
    tree: DerivationTree, scope: DerivationTree, index_counter_symbols: list[str]
) -> int:
    idx = 0
    index_counter_nts = [NonTerminal(symbol) for symbol in index_counter_symbols]
    for val in scope.flatten():
        if val == tree:
            return idx
        if val.symbol in index_counter_nts:
            idx += 1
    return -1

from fandango.language.tree import DerivationTree

actual_int = int
actual_float = float
actual_complex = complex


def int(x, *args, **kwargs):
    if isinstance(x, DerivationTree):
        return x.to_int(*args, **kwargs)
    return actual_int(x, *args, **kwargs)


def float(x):
    if isinstance(x, DerivationTree):
        return x.to_float()
    return actual_float(x)


def complex(x, *args, **kwargs):
    if isinstance(x, DerivationTree):
        return x.to_complex(*args, **kwargs)
    return complex(x, *args, **kwargs)


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

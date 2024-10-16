from fandango.language.tree import DerivationTree

actual_int = int
actual_float = float
actual_complex = complex


def int(x):
    if isinstance(x, DerivationTree):
        return x.to_int()
    return actual_int(x)


def float(x):
    if isinstance(x, DerivationTree):
        return x.to_float()
    return actual_float(x)


def complex(x):
    if isinstance(x, DerivationTree):
        return x.to_complex()
    return complex(x)


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

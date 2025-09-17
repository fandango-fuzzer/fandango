import pytest
from fandango.errors import FandangoConversionError
from fandango.language.symbols.terminal import Terminal
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import (
    DIRECT_ACCESS_METHODS_BASE_TO_FIRST_ARG_TYPE,
    DIRECT_ACCESS_METHODS_BASE_TO_UNDERLYING_TYPE,
    TreeValue,
    trailing_bits_to_int,
)
from fandango.language.tree_value import TreeValue, TreeValueType, trailing_bits_to_int


A_BITS = [int(bit) for bit in f"{ord('a'):08b}"]
ONE_BITS = [int(bit) for bit in f"{ord('1'):08b}"]


def test_trailing_bits_to_int():
    assert trailing_bits_to_int([]) == 0
    assert trailing_bits_to_int([0]) == 0
    assert trailing_bits_to_int([1]) == 1
    assert trailing_bits_to_int([0, 1]) == 1
    assert trailing_bits_to_int([1, 0]) == 2
    assert trailing_bits_to_int([1, 1]) == 3
    assert trailing_bits_to_int([1] + [0] * 16) == 65536


@pytest.mark.parametrize(
    "value", ["Hello, World!", "", "💃", b"", b"Hello, World!", 0, 1]
)
def test_tree_value_create(value):
    type_ = type(value)
    tree_value = TreeValue(value)
    assert type_(tree_value) == value


def test_empty_convertors():
    tree_value = TreeValue.empty()
    assert str(tree_value) == ""
    assert bytes(tree_value) == b""
    assert int(tree_value) == 0
    assert tree_value.to_bits() == ""


def test_append_to_empty():
    tree_value = TreeValue.empty()
    tree_value = tree_value.append(TreeValue(1))
    with pytest.raises(ValueError):
        str(tree_value)
    with pytest.raises(ValueError):
        bytes(tree_value)
    assert int(tree_value) == 1
    assert tree_value.to_bits() == "1"

    tree_value = TreeValue.empty()
    tree_value = tree_value.append(TreeValue("a"))
    assert str(tree_value) == "a"
    assert bytes(tree_value) == b"a"
    with pytest.raises(ValueError):
        assert int(tree_value) == 1


def test_append_with_empty():
    tree_value = TreeValue(1)
    tree_value = tree_value.append(TreeValue.empty())
    with pytest.raises(ValueError):
        str(tree_value)
    with pytest.raises(ValueError):
        bytes(tree_value)
    assert int(tree_value) == 1
    assert tree_value.to_bits() == "1"

    tree_value = TreeValue("a")
    tree_value = tree_value.append(TreeValue.empty())
    assert str(tree_value) == "a"
    assert bytes(tree_value) == b"a"
    with pytest.raises(ValueError):
        int(tree_value)


def test_append_empty_with_empty():
    tree_value = TreeValue.empty()
    tree_value = tree_value.append(TreeValue.empty())
    assert str(tree_value) == ""
    assert bytes(tree_value) == b""
    assert int(tree_value) == 0
    assert tree_value.to_bits() == ""


def test_tree_value_cross_conversion_from_int():
    # simple case
    tree_value = TreeValue(1)
    assert tree_value.trailing_bits == (1,)
    assert int(tree_value) == 1

    with pytest.raises(ValueError):
        str(tree_value)
    with pytest.raises(ValueError):
        bytes(tree_value)

    # reducing
    tree_value = TreeValue(b"")
    for bit in ONE_BITS:
        tree_value = tree_value.append(TreeValue(int(bit)))  # push 8 bits, or one byte
    assert int(tree_value) == 1
    assert str(tree_value) == "1"
    assert bytes(tree_value) == b"1"


def test_tree_value_cross_conversion_from_str():
    tree_value = TreeValue("Hello, World!")
    with pytest.raises(ValueError):
        int(tree_value)
    assert str(tree_value) == "Hello, World!"
    assert bytes(tree_value) == b"Hello, World!"


def test_tree_value_cross_conversion_from_bytes():
    tree_value = TreeValue(b"Hello, World!")
    with pytest.raises(FandangoConversionError):
        int(tree_value)
    assert str(tree_value) == "Hello, World!"
    assert bytes(tree_value) == b"Hello, World!"

    tree_value = TreeValue(b"123")
    assert int(tree_value) == 123
    assert str(tree_value) == "123"
    assert bytes(tree_value) == b"123"


def test_tree_value_trailing_bits():
    # from string
    tree_value = TreeValue("Hello, World!")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))

    assert str(tree_value) == "Hello, World!a"

    tree_value = TreeValue("Hello, World!")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))
    assert bytes(tree_value) == b"Hello, World!a"

    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))
    assert str(tree_value) == "Hello, World!a"

    tree_value = TreeValue(b"Hello, World!")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))
    assert bytes(tree_value) == b"Hello, World!a"


def test_tree_value_incomplete_trailing_bits():
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue(1))
    with pytest.raises(FandangoConversionError):
        int(tree_value)
    with pytest.raises(FandangoConversionError):
        str(tree_value)
    with pytest.raises(FandangoConversionError):
        bytes(tree_value)


def test_tree_value_combine_with_str():
    # from string
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue("a"))
    assert str(tree_value) == "Hello, World!a"
    assert tree_value.is_type(TreeValueType.STRING)

    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    tree_value = tree_value.append(TreeValue("a"))
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(TreeValueType.BYTES)

    # from int
    tree_value = TreeValue(1)
    with pytest.raises(FandangoConversionError):
        tree_value.append(TreeValue("a"))


def test_tree_value_combine_with_bytes():
    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    tree_value = tree_value.append(TreeValue(b"a"))
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(TreeValueType.BYTES)

    # from string
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue(b"a"))
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(TreeValueType.BYTES)

    # from int
    tree_value = TreeValue(1)
    with pytest.raises(FandangoConversionError):
        tree_value.append(TreeValue(b"a"))


def test_tree_value_combine_with_int():
    # from string
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue(A_BITS[0]))
    with pytest.raises(ValueError):
        str(tree_value)

    for i in range(1, len(A_BITS)):  # add more bits to be reducible to a byte
        tree_value = tree_value.append(TreeValue(A_BITS[i]))
    assert str(tree_value) == "Hello, World!a"
    for bit in A_BITS:  # add more bits to be reducible to a byte
        tree_value = tree_value.append(TreeValue(bit))
    assert bytes(tree_value) == b"Hello, World!aa"
    assert tree_value.is_type(TreeValueType.BYTES)

    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    tree_value = tree_value.append(TreeValue(A_BITS[0]))
    with pytest.raises(ValueError):
        bytes(tree_value)

    for i in range(1, len(A_BITS)):  # add more bits to be reducible to a byte
        tree_value = tree_value.append(TreeValue(A_BITS[i]))
    assert str(tree_value) == "Hello, World!a"
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))
    assert bytes(tree_value) == b"Hello, World!aa"
    assert tree_value.is_type(TreeValueType.BYTES)

    # from int
    tree_value = TreeValue(1)
    tree_value = tree_value.append(TreeValue(1))
    assert int(tree_value) == 3
    assert tree_value.is_type(TreeValueType.TRAILING_BITS_ONLY)


def test_tree_value_to_bits():
    tree_value_str = TreeValue("a")
    assert tree_value_str.to_bits() == f"{ord('a'):08b}"

    tree_value_bytes = TreeValue(b"a")
    assert tree_value_bytes.to_bits() == f"{ord('a'):08b}"

    tree_value_int = TreeValue(1)
    assert tree_value_int.to_bits() == "1"

    tree_value_str = tree_value_str.append(TreeValue(1))
    assert tree_value_str.to_bits() == f"{ord('a'):08b}1"

    tree_value_bytes = tree_value_bytes.append(TreeValue(1))
    assert tree_value_bytes.to_bits() == f"{ord('a'):08b}1"

    tree_value_int = tree_value_int.append(TreeValue(1))
    assert tree_value_int.to_bits() == "11"


def test_direct_access_simple():
    tree_value = TreeValue(1)
    assert -1 == -tree_value  # type: ignore[operator]
    tree = DerivationTree(Terminal(1))
    assert -1 == -tree  # type: ignore[operator]


UNDERLYING_TYPE_NO_ARGS = [
    "__abs__",
    "__ceil__",
    "__float__",
    "__floor__",
    "__index__",
    "__invert__",
    "__neg__",
    "__pos__",
    "__round__",
    "__trunc__",
    "as_integer_ratio",
    "bit_count",
    "bit_length",
    "capitalize",
    "casefold",
    "conjugate",
    "expandtabs",
    "hex",
    "isalnum",
    "isalpha",
    "isascii",
    "isdecimal",
    "isdigit",
    "isidentifier",
    "islower",
    "isnumeric",
    "isprintable",
    "isspace",
    "istitle",
    "isupper",
    "lower",
    "lstrip",
    "split",
    "strip",
    "rsplit",
    "rstrip",
    "splitlines",
    "swapcase",
    "title",
    "upper",
]


@pytest.mark.parametrize("method", UNDERLYING_TYPE_NO_ARGS)
def test_to_underlying_type_no_arg(method):
    def check_method(obj, method):
        if 1 < ((method in dir(1)) + (method in dir("1")) + (method in dir(b"1"))):
            with pytest.warns(DeprecationWarning):
                assert not callable(getattr(obj, method)())
        else:
            assert not callable(getattr(obj, method)())

    run = 0
    if method in dir(1):
        assert not callable(getattr(1, method)())
        check_method(DerivationTree(Terminal(1)), method)
        check_method(TreeValue(1), method)
        run += 1
    if method in dir("1"):
        assert not callable(getattr("1", method)())
        check_method(DerivationTree(Terminal("1")), method)
        check_method(TreeValue("1"), method)
        run += 1
    if method in dir(b"1"):
        assert not callable(getattr(b"1", method)())
        check_method(DerivationTree(Terminal(b"1")), method)
        check_method(TreeValue(b"1"), method)
        run += 1
    assert (
        run > 0
    ), f"{method} not found in dirs of 1, {set(dir(1) + dir('1') + dir(b'1'))}"


UNDERLYING_TYPE_INT_ARG = [
    "__mul__",
    "__pow__",
    "__rmul__",
    "__rpow__",
    "center",
    "ljust",
    "rjust",
    "zfill",
]


@pytest.mark.parametrize("method", UNDERLYING_TYPE_INT_ARG)
def test_to_underlying_type_int_arg(method):
    left: tuple[int | str | bytes, ...] = (1, "1", b"1")
    right: tuple[int | str | bytes, ...] = (1, 1, 1)
    if "__r" in method:
        left, right = right, left

    def check_method(obj, method, *args):
        if 1 < ((method in dir(1)) + (method in dir("1")) + (method in dir(b"1"))):
            with pytest.warns(DeprecationWarning):
                assert not callable(getattr(obj, method)(*args))
        else:
            assert not callable(getattr(obj, method)(*args))

    run = 0
    if method in dir(1):
        assert not callable(getattr(left[0], method)(right[0]))
        check_method(DerivationTree(Terminal(left[0])), method, right[0])
        check_method(TreeValue(left[0]), method, right[0])
        run += 1
    if method in dir("1"):
        assert not callable(getattr(left[1], method)(right[1]))
        check_method(DerivationTree(Terminal(left[1])), method, right[1])
        check_method(TreeValue(left[1]), method, right[1])
        run += 1
    if method in dir(b"1"):
        assert not callable(getattr(left[2], method)(right[2]))
        check_method(DerivationTree(Terminal(left[2])), method, right[2])
        check_method(TreeValue(left[2]), method, right[2])
        run += 1
    assert (
        run > 0
    ), f"{method} not found in dirs of 1, {set(dir(1) + dir('1') + dir(b'1'))}"


MODS = [
    "__mod__",
    "__rmod__",
]


@pytest.mark.parametrize("method", MODS)
def test_to_underlying_type_mod(method):
    run = 0
    left = (1, "%s", b"%s")
    right = (1, "1", b"1")
    if "r" in method:
        left, right = right, left

    if method in dir(1):
        assert not callable(getattr(left[0], method)(right[0]))
        assert not callable(
            getattr(DerivationTree(Terminal(left[0])), method)(right[0])
        )
        assert not callable(getattr(TreeValue(left[0]), method)(right[0]))
        run += 1
    if method in dir("1"):
        assert not callable(getattr(left[1], method)(right[1]))
        assert not callable(
            getattr(DerivationTree(Terminal(left[1])), method)(right[1])
        )
        assert not callable(getattr(TreeValue(left[1]), method)(right[1]))
        run += 1
    if method in dir(b"1"):
        assert not callable(getattr(left[2], method)(right[2]))
        assert not callable(
            getattr(DerivationTree(Terminal(left[2])), method)(right[2])
        )
        assert not callable(getattr(TreeValue(left[2]), method)(right[2]))
        run += 1
    assert (
        run > 0
    ), f"{method} not found in dirs of 1, {set(dir(1) + dir('1') + dir(b'1'))}"


FORMATS = [
    "format",
]


@pytest.mark.parametrize("method", FORMATS)
def test_to_underlying_type_format(method):
    def check_method(obj, method, *args, **kwargs):
        if 1 < ((method in dir(1)) + (method in dir("1")) + (method in dir(b"1"))):
            with pytest.warns(DeprecationWarning):
                assert not callable(getattr(obj, method)(*args, **kwargs))
        else:
            assert not callable(getattr(obj, method)(*args, **kwargs))

    run = 0
    if method in dir(1):
        assert not callable(getattr(1, method)())
        check_method(DerivationTree(Terminal(1)), method)
        check_method(TreeValue(1), method)
        run += 1
    if method in dir("1"):
        assert not callable(getattr("{}", method)("1"))
        check_method(DerivationTree(Terminal("{}")), method, "1")
        check_method(TreeValue("{}"), method, "1")
        run += 1
    if method in dir(b"1"):
        assert not callable(getattr(b"{}", method)(b"1"))
        check_method(DerivationTree(Terminal(b"{}")), method, b"1")
        check_method(TreeValue(b"{}"), method, b"1")
        run += 1

    assert (
        run > 0
    ), f"{method} not found in dirs of 1, {set(dir(1) + dir('1') + dir(b'1'))}"


FORMAT_MAP = [
    "format_map",
]


@pytest.mark.parametrize("method", FORMAT_MAP)
def test_to_underlying_type_format_map(method):
    def check_method(obj, method, *args, **kwargs):
        if 1 < ((method in dir(1)) + (method in dir("1")) + (method in dir(b"1"))):
            with pytest.warns(DeprecationWarning):
                assert not callable(getattr(obj, method)(*args, **kwargs))
        else:
            assert not callable(getattr(obj, method)(*args, **kwargs))

    run = 0
    if method in dir(1):
        assert not callable(getattr(1, method)({1: 1}))
        check_method(DerivationTree(Terminal(1)), method, {1: 1})
        check_method(TreeValue(1), method, {1: 1})
        run += 1
    if method in dir("1"):
        assert not callable(getattr("1", method)({"1": "1"}))
        check_method(DerivationTree(Terminal("1")), method, {"1": "1"})
        check_method(TreeValue("1"), method, {"1": "1"})
        run += 1
    if method in dir(b"1"):
        assert not callable(getattr(b"1", method)({b"1": b"1"}))
        check_method(DerivationTree(Terminal(b"1")), method, {b"1": b"1"})
        check_method(TreeValue(b"1"), method, {b"1": b"1"})


FIRST_ARG = [
    "__add__",
    "__and__",
    "__contains__",
    "__divmod__",
    "__floordiv__",
    "__ge__",
    "__gt__",
    "__le__",
    "__lshift__",
    "__lt__",
    "__or__",
    "__radd__",
    "__rand__",
    "__rdivmod__",
    "__rfloordiv__",
    "__rlshift__",
    "__ror__",
    "__rrshift__",
    "__rshift__",
    "__rsub__",
    "__rtruediv__",
    "__rxor__",
    "__sub__",
    "__truediv__",
    "__xor__",
    "count",
    "endswith",
    "find",
    "index",
    "partition",
    "removeprefix",
    "removesuffix",
    "rfind",
    "rindex",
    "rpartition",
    "startswith",
]


@pytest.mark.parametrize("method", FIRST_ARG)
def test_to_first_arg(method):
    run = 0
    if method in dir(1):
        assert not callable(getattr(1, method)(1))
        assert not callable(getattr(DerivationTree(Terminal(1)), method)(1))
        assert not callable(getattr(TreeValue(1), method)(1))
        run += 1
    if method in dir("1"):
        assert not callable(getattr("1", method)("1"))
        assert not callable(getattr(DerivationTree(Terminal("1")), method)("1"))
        assert not callable(getattr(TreeValue("1"), method)("1"))
        run += 1
    if method in dir(b"1"):
        assert not callable(getattr(b"1", method)(b"1"))
        assert not callable(getattr(DerivationTree(Terminal(b"1")), method)(b"1"))
        assert not callable(getattr(TreeValue(b"1"), method)(b"1"))
        run += 1
    assert (
        run > 0
    ), f"{method} not found in dirs of 1, {set(dir(1) + dir('1') + dir(b'1'))}"


def test_check_all_direct_methods_tested():
    in_tests = (
        FIRST_ARG
        + UNDERLYING_TYPE_NO_ARGS
        + UNDERLYING_TYPE_INT_ARG
        + MODS
        + FORMATS
        + FORMAT_MAP
    )
    implemented = (
        DIRECT_ACCESS_METHODS_BASE_TO_FIRST_ARG_TYPE
        + DIRECT_ACCESS_METHODS_BASE_TO_UNDERLYING_TYPE
    )
    assert sorted(in_tests) == sorted(implemented)


@pytest.mark.parametrize(
    "base_value",
    [TreeValue("Hello, World!"), DerivationTree(Terminal("Hello, World!"))],
)
def test_tree_value_direct_access_non_base_type(base_value):
    assert base_value.startswith("Hello")
    with pytest.warns(DeprecationWarning):
        assert base_value.startswith(TreeValue("Hello"))
    with pytest.warns(DeprecationWarning):
        assert base_value.startswith(DerivationTree(Terminal("Hello")))

    with pytest.raises(Exception):
        base_value.startswith(1.0)  # float is illegal base type

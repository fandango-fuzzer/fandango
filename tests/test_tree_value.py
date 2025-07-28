import pytest
from fandango.language.tree_value import TreeValue, trailing_bits_to_int


A_BITS = [int(bit) for bit in f"{ord('a'):08b}"]


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


def test_tree_value_cross_conversion_from_int():
    # simple case
    tree_value = TreeValue(1)
    assert int(tree_value) == 1

    with pytest.raises(ValueError):
        str(tree_value)
    with pytest.raises(ValueError):
        bytes(tree_value)

    # reducing
    tree_value = TreeValue(b"")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(int(bit)))  # push 8 bits, or one byte
    assert int(tree_value) == ord("a")
    assert str(tree_value) == "a"
    assert bytes(tree_value) == b"a"


def test_tree_value_cross_conversion_from_str():
    tree_value = TreeValue("Hello, World!")
    with pytest.raises(ValueError):
        int(tree_value)
    assert str(tree_value) == "Hello, World!"
    assert bytes(tree_value) == b"Hello, World!"


def test_tree_value_cross_conversion_from_bytes():
    tree_value = TreeValue(b"Hello, World!")
    assert int(tree_value) == int.from_bytes(b"Hello, World!")
    assert str(tree_value) == "Hello, World!"
    assert bytes(tree_value) == b"Hello, World!"


def test_tree_value_trailing_bits():
    # from string
    tree_value = TreeValue("Hello, World!")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))

    assert str(tree_value) == "Hello, World!a"
    assert bytes(tree_value) == b"Hello, World!a"

    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    for bit in A_BITS:
        tree_value = tree_value.append(TreeValue(bit))
    assert str(tree_value) == "Hello, World!a"
    assert bytes(tree_value) == b"Hello, World!a"


def test_tree_value_incomplete_trailing_bits():
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue(1))
    with pytest.raises(ValueError):
        int(tree_value)
    with pytest.raises(ValueError):
        str(tree_value)
    with pytest.raises(ValueError):
        bytes(tree_value)


def test_tree_value_combine_with_str():
    # from string
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue("a"))
    assert str(tree_value) == "Hello, World!a"
    assert tree_value.is_type(str)

    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    tree_value = tree_value.append(TreeValue("a"))
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(bytes)

    # from int
    tree_value = TreeValue(1)
    with pytest.raises(ValueError):
        tree_value = tree_value.append(TreeValue("a"))


def test_tree_value_combine_with_bytes():
    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    tree_value = tree_value.append(TreeValue(b"a"))
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(bytes)

    # from string
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue(b"a"))
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(bytes)

    # from int
    tree_value = TreeValue(1)
    with pytest.raises(ValueError):
        tree_value = tree_value.append(TreeValue(b"a"))


def test_tree_value_combine_with_int():
    # from string
    tree_value = TreeValue("Hello, World!")
    tree_value = tree_value.append(TreeValue(A_BITS[0]))
    with pytest.raises(ValueError):
        str(tree_value)

    for i in range(1, len(A_BITS)):  # add more bits to be reducible to a byte
        tree_value = tree_value.append(TreeValue(A_BITS[i]))
    assert str(tree_value) == "Hello, World!a"
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(bytes)

    # from bytes
    tree_value = TreeValue(b"Hello, World!")
    tree_value = tree_value.append(TreeValue(A_BITS[0]))
    with pytest.raises(ValueError):
        bytes(tree_value)

    for i in range(1, len(A_BITS)):  # add more bits to be reducible to a byte
        tree_value = tree_value.append(TreeValue(A_BITS[i]))
    assert str(tree_value) == "Hello, World!a"
    assert bytes(tree_value) == b"Hello, World!a"
    assert tree_value.is_type(bytes)

    # from int
    tree_value = TreeValue(1)
    tree_value = tree_value.append(TreeValue(1))
    assert int(tree_value) == 3
    assert tree_value.is_type(type(None))


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

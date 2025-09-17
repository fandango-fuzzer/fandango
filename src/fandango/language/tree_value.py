from __future__ import annotations
from types import NoneType
from typing import Any, Optional
import warnings
import enum

from fandango.errors import FandangoConversionError, FandangoValueError

STRING_TO_BYTES_ENCODING = "utf-8"  # according to the docs
BYTES_TO_STRING_ENCODING = "latin-1"  # according to the docs


class TreeValueType(enum.Enum):
    STRING = "string"
    BYTES = "bytes"
    TRAILING_BITS_ONLY = "trailing_bits"
    EMPTY = "empty"


def trailing_bits_to_int(trailing_bits: list[int]) -> int:
    """
    Convert a list of trailing bits to an integer.

    The bits are assumed to be in big endian order and are not checked for validity (assumed to be 0 or 1)
    """
    return sum(bit << i for i, bit in enumerate(reversed(trailing_bits)))


def _str_to_bytes(value: str, encoding: str) -> bytes:
    """
    Convert a string to bytes.

    :param value: The string to convert.
    :param encoding: The encoding to use when converting the string to bytes.
    :throws FandangoConversionError: If the string cannot be converted to bytes.
    :return: A bytes object.
    """
    try:
        return value.encode(encoding=encoding)
    except UnicodeEncodeError as e:
        raise FandangoConversionError(
            f"string to bytes conversion failed, string: {value}, encoding: {encoding}, error: {e}"
        )


def _bytes_to_str(value: bytes, encoding: str) -> str:
    """
    Convert bytes to a string.

    :param value: The bytes to convert.
    :param encoding: The encoding to use when converting the bytes to a string.
    :throws FandangoConversionError: If the bytes cannot be converted to a string.
    :return: A string.
    """
    try:
        return value.decode(encoding=encoding)
    except UnicodeDecodeError as e:
        raise FandangoConversionError(
            f"bytes to string conversion failed, bytes: {value!r}, encoding: {encoding}, error: {e}"
        )


def _get_exclusive_base_type_method_is_implemented_for(name: str) -> Optional[type]:
    """
    If the method, whose name is passed, is implemented on only one of int, str, bytes, return that type.
    If the method is implemented on more than one type, return None.
    If the method is not implemented on any type, raise an error.
    """
    is_in_int = name in dir(1)
    is_in_str = name in dir("1")
    is_in_bytes = name in dir(b"1")
    match is_in_int + is_in_str + is_in_bytes:
        case 0:
            raise FandangoValueError(
                f"Method {name} is not implemented on any underlying type"
            )
        case 1:
            return int if is_in_int else str if is_in_str else bytes
        case _:
            return None


def _attach_to_first_arg(
    function_names: list[str],
):
    """
    Decorator to add methods to a class, where self is transformed to either
    (a) the only base type it is implemented on,
    (b) the type of the first argument,
    (c) the type of the only keyword argument.

    If the first argument is a DerivationTree or TreeValue, it is converted to the underlying type. This is deprecated.
    """

    def make_method(name):
        def method(self, *args, **kwargs):
            base_type = _get_exclusive_base_type_method_is_implemented_for(name)
            if base_type is None:
                message = (
                    "Using a {} arg to pass as a {} arg "
                    f"to {name} is deprecated "
                    "because there is no automated way of knowing which type to transform the underlying type to. "
                    "Use `str` or `bytes` to explicitly convert to the desired type first."
                )

                if len(args) == 0:
                    assert (
                        len(kwargs) == 1
                    ), f"Method {name} must have at least one unnamed argument or exactly one named argument"
                    k, v = list(kwargs.items())[0]
                    # cannot import DerivationTree because of circular import
                    if v.__class__.__name__ == "DerivationTree":
                        v = v.value()._inner_value(
                            message.format("DerivationTree", "keyword")
                        )
                    elif isinstance(v, TreeValue):
                        v = v._inner_value(message.format("TreeValue", "keyword"))
                    base_type = type(v)
                    kwargs = {k: v}
                else:
                    first_arg = args[0]
                    # cannot import DerivationTree because of circular import
                    if first_arg.__class__.__name__ == "DerivationTree":
                        first_arg = first_arg.value()._inner_value(
                            message.format("DerivationTree", "first")
                        )
                    elif isinstance(first_arg, TreeValue):
                        first_arg = first_arg._inner_value(
                            message.format("TreeValue", "first")
                        )
                    base_type = type(first_arg)
                    args = (first_arg,) + args[1:]

            assert base_type in [
                str,
                bytes,
                int,
            ], f"Cannot determine the type the base should be converted to based on argument of type {base_type.__name__}"

            base = base_type(self)
            return getattr(base, name)(*args, **kwargs)

        return method

    def decorator(cls):
        for name in function_names:
            # Check if the method is actually implemented on the class itself, not inherited
            if name in cls.__dict__:
                warnings.warn(
                    f"Method {name} already exists on {cls.__name__}, skipping",
                    Warning,
                )
            else:
                setattr(cls, name, make_method(name))
        return cls

    return decorator


def _attach_to_underlying(
    function_names: list[str],
):
    """
    Decorator to add methods to a class, where self is transformed to either (a) the only base type it is implemented on or (b) the underlying type and then the method is called on that.

    (b) is deprecated.
    """

    def make_method(name):
        def method(self: TreeValue, *args, **kwargs):
            base_type = _get_exclusive_base_type_method_is_implemented_for(name)
            if base_type is not None:
                base = base_type(self)
            else:
                message = (
                    f"Using {name} on DerivationTree or TreeValue objects is deprecated "
                    "because there is no automated way of knowing which type to transform the underlying type to. "
                    "Use `str` or `bytes` to explicitly convert to the desired type first."
                )
                base = self._inner_value(message)
            return getattr(base, name)(*args, **kwargs)

        return method

    def decorator(cls):
        for name in function_names:
            # Check if the method is actually implemented on the class itself, not inherited
            if name in cls.__dict__:
                warnings.warn(
                    f"Method {name} already exists on {cls.__name__}, skipping",
                    Warning,
                )
            else:
                setattr(cls, name, make_method(name))
        return cls

    return decorator


# not implemented on purpose:
# __bool__
# __buffer__
# __bytes__
# __delattr__
# __dir__
# __doc__
# __eq__
# __format__
# __getattribute__
# __getitem__
# __getnewargs__
# __getstate__
# __hash__
# __init__
# __init_subclass__
# __int__
# __iter__
# __len__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# decode
# denominator
# encode
# fromhex
# from_bytes
# imag
# numerator
# maketrans
# join
# real
# replace
# translate
# to_bytes

DIRECT_ACCESS_METHODS_BASE_TO_FIRST_ARG_TYPE = [
    "__add__",
    "__contains__",
    "__divmod__",
    "__floordiv__",
    "__ge__",
    "__gt__",
    "__le__",
    "__lshift__",
    "__lt__",
    "__mod__",
    "__radd__",
    "__rand__",
    "__rdivmod__",
    "__rfloordiv__",
    "__rlshift__",
    "__rmod__",
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

DIRECT_ACCESS_METHODS_BASE_TO_UNDERLYING_TYPE = [
    "__and__",
    "__abs__",
    "__ceil__",
    "__float__",
    "__floor__",
    "__index__",
    "__invert__",
    "__mul__",
    "__neg__",
    "__or__",
    "__pos__",
    "__pow__",
    "__rmul__",
    "__round__",
    "__ror__",
    "__rpow__",
    "__trunc__",
    "as_integer_ratio",
    "bit_count",
    "bit_length",
    "capitalize",
    "casefold",
    "center",
    "conjugate",
    "expandtabs",
    "format",
    "format_map",
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
    "ljust",
    "split",
    "strip",
    "rjust",
    "rsplit",
    "rstrip",
    "splitlines",
    "swapcase",
    "title",
    "upper",
    "zfill",
]


@_attach_to_first_arg(DIRECT_ACCESS_METHODS_BASE_TO_FIRST_ARG_TYPE)
@_attach_to_underlying(DIRECT_ACCESS_METHODS_BASE_TO_UNDERLYING_TYPE)
class TreeValue:
    def __init__(
        self,
        value: str | bytes | int | None,
        *,
        trailing_bits: list[int] = [],
        allow_empty: bool = False,
    ):
        self._value: str | bytes | None
        assert all(
            bit & 1 == bit for bit in trailing_bits
        ), "trailing bits must be 0 or 1, got " + str(trailing_bits)

        if isinstance(value, int):
            assert (
                value & 1 == value
            ), "ints are used for bit values, and must thus be 0 or 1"
            assert trailing_bits == [], "trailing bits are not supported for int values"
            trailing_bits = [value]
            value = None

        if value is None:
            assert (
                allow_empty or len(trailing_bits) > 0
            ), "None values must have trailing bits"

        self._value = value
        self._trailing_bits = trailing_bits

    def _reduce_trailing_bits(self, str_to_bytes_encoding: str) -> None:
        """
        Reduce the trailing bits into the value.

        :raises FandangoConversionError: If the trailing bits don't sum up to a perfect number of bytes.
        """
        if not self._trailing_bits:
            return

        if len(self._trailing_bits) % 8 != 0:
            raise FandangoConversionError(
                "Trailing bits are not a multiple of 8, currently have "
                f"{len(self._trailing_bits)} bits"
            )

        num = trailing_bits_to_int(self._trailing_bits)
        bytes_ = num.to_bytes(len(self._trailing_bits) // 8)
        self._trailing_bits = []
        if isinstance(self._value, str):
            self._value = (
                _str_to_bytes(self._value, encoding=str_to_bytes_encoding) + bytes_
            )
        elif isinstance(self._value, bytes):
            self._value = self._value + bytes_
        elif self._value is None:
            self._value = bytes_
        else:
            raise FandangoValueError(
                f"Invalid value type: {type(self._value)}, {self._trailing_bits}. This should not happen, please report this as a bug"
            )

    @property
    def type_(self) -> TreeValueType:
        if self._value is None:
            if self._trailing_bits:
                return TreeValueType.TRAILING_BITS_ONLY
            else:
                return TreeValueType.EMPTY
        elif isinstance(self._value, str):
            if self._trailing_bits:
                # Trailing bits are reduced to bytes
                return TreeValueType.BYTES
            else:
                return TreeValueType.STRING
        elif isinstance(self._value, bytes):
            return TreeValueType.BYTES
        else:
            raise ValueError(f"Invalid value type: {type(self._value)}")

    def is_type(self, type_: TreeValueType) -> bool:
        return self.type_ == type_

    def count_bytes(self) -> int:
        """
        Count the number of bytes in the TreeValue.

        :throws FandangoConversionError: If the value cannot be converted to bytes.
        :return: The number of bytes in the TreeValue.
        """
        return len(self.to_bytes())

    def append(
        self,
        other: TreeValue,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
    ) -> TreeValue:
        """
        Create a new TreeValue by appending another value to this value.

        :param other: The value to append..
        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :throws FandangoConversionError: If one of the values has to be converted and the conversion fails.
        :return: A new TreeValue.
        """

        if self.is_type(TreeValueType.EMPTY):
            return TreeValue(
                other._value, trailing_bits=other._trailing_bits, allow_empty=True
            )

        if other._value is None:
            trailing_bits = self._trailing_bits + other._trailing_bits
            return TreeValue(self._value, trailing_bits=trailing_bits)

        # flush bits, will set self._value
        self._reduce_trailing_bits(str_to_bytes_encoding=str_to_bytes_encoding)

        if isinstance(self._value, str):
            if isinstance(other._value, str):
                return TreeValue(
                    self._value + other._value,
                    trailing_bits=other._trailing_bits,
                )
            elif isinstance(other._value, bytes):
                return TreeValue(
                    _str_to_bytes(self._value, encoding=str_to_bytes_encoding)
                    + other._value,
                    trailing_bits=other._trailing_bits,
                )

        elif isinstance(self._value, bytes):
            if isinstance(other._value, str):
                return TreeValue(
                    self._value
                    + _str_to_bytes(other._value, encoding=str_to_bytes_encoding),
                    trailing_bits=other._trailing_bits,
                )
            elif isinstance(other._value, bytes):
                return TreeValue(
                    self._value + other._value,
                    trailing_bits=other._trailing_bits,
                )
        raise FandangoValueError(
            f"Cannot compute {self._value!r} + {other._value!r}. This should not happen, please report this as a bug"
        )

    def can_compare_with(self, right: object) -> bool:
        if isinstance(right, TreeValue):
            return self.is_type(right.type_)

        return (
            (isinstance(right, int) and self.is_type(TreeValueType.TRAILING_BITS_ONLY))
            or (isinstance(right, str) and self.is_type(TreeValueType.STRING))
            or (isinstance(right, bytes) and self.is_type(TreeValueType.BYTES))
        )

    def to_string(
        self,
        bytes_to_str_encoding: str = BYTES_TO_STRING_ENCODING,
    ) -> str:
        """
        Convert the TreeValue to a string.

        :param bytes_to_str_encoding: The encoding to use when converting bytes to strings.
        :throws FandangoConversionError: If the value cannot be converted to a string.
        :return: A string.
        """
        if self.is_type(TreeValueType.EMPTY):
            return ""

        # encoding with the same encoding in both direction
        self._reduce_trailing_bits(str_to_bytes_encoding=bytes_to_str_encoding)
        if isinstance(self._value, str):
            return self._value
        if isinstance(self._value, bytes):
            return _bytes_to_str(self._value, encoding=bytes_to_str_encoding)
        raise FandangoValueError(
            f"Invalid value type: {type(self._value)}, {self._trailing_bits}. This should not happen, please report this as a bug"
        )

    def to_bytes(
        self,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
    ) -> bytes:
        """
        Convert the TreeValue to bytes.

        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :throws FandangoConversionError: If the value cannot be converted to bytes.
        :return: A bytes object.
        """
        if self.is_type(TreeValueType.EMPTY):
            return b""

        self._reduce_trailing_bits(str_to_bytes_encoding=str_to_bytes_encoding)
        if isinstance(self._value, bytes):
            return self._value
        elif isinstance(self._value, str):
            return _str_to_bytes(self._value, encoding=str_to_bytes_encoding)
        raise FandangoValueError(
            f"Invalid value type: {type(self._value)}, {self._trailing_bits}. This should not happen, please report this as a bug"
        )

    def to_bits(
        self,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
    ) -> str:
        """
        Convert the TreeValue to a string of 0s and 1s representing bits.

        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :throws FandangoConversionError: If the value cannot be converted to bits.
        :return: A string of bits.
        """
        if self._value is None:
            value = ""
        elif isinstance(self._value, bytes):
            value = "".join(f"{byte_:08b}" for byte_ in self._value)
        elif isinstance(self._value, str):
            value = "".join(
                f"{byte_:08b}"
                for byte_ in _str_to_bytes(self._value, encoding=str_to_bytes_encoding)
            )
        else:
            raise FandangoValueError(
                f"Invalid value type: {type(self._value)}. This should not happen, please report this as a bug"
            )

        trailing_bits = "".join(str(bit) for bit in self._trailing_bits)

        return value + trailing_bits

    def to_int(
        self,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
        bytes_to_str_encoding: str = BYTES_TO_STRING_ENCODING,
    ) -> int:
        """
        Convert the TreeValue to an integer.

        Strings are converted to ints using int(), bytes are converted to strings using the given encoding and then to ints using int().

        If bits were ever included, the underlying data structure is bytes.

        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :throws FandangoConversionError: If the value cannot be converted to an integer.
        :return: An integer.
        """
        if self._value is None:  # only trailing bits
            return trailing_bits_to_int(self._trailing_bits)
        else:
            self._reduce_trailing_bits(str_to_bytes_encoding=str_to_bytes_encoding)
            if isinstance(self._value, str):
                return int(self._value)
            elif isinstance(self._value, bytes):
                try:
                    return int(
                        self.to_string(bytes_to_str_encoding=bytes_to_str_encoding)
                    )
                except ValueError as e:
                    raise FandangoConversionError(
                        f"int conversion failed, value: {self._value!r}, encoding: {bytes_to_str_encoding}, error: {e}"
                    )
            else:
                raise FandangoValueError(
                    f"Invalid value type: {type(self._value)}, {self._trailing_bits}. This should not happen, please report this as a bug"
                )

    @property
    def trailing_bits(self) -> Optional[tuple[int, ...]]:
        """
        Return the trailing bits as a tuple of 0s and 1s. MSB first. None if this is not only trailing bits.

        :return: A tuple of integers, or None if this is not only trailing bits.
        """
        if self._value is None:
            return tuple(self._trailing_bits)
        else:
            return None

    def __str__(self) -> str:
        return self.to_string()

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def __int__(self) -> int:
        return self.to_int()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TreeValue):
            return (
                self._value == other._value
                and self._trailing_bits == other._trailing_bits
            )
        # attempt to coerce type of self to the same as other
        # works (at least) for int, str, bytes
        if isinstance(other, int):
            return self.to_int() == other
        elif isinstance(other, str):
            return self.to_string() == other
        elif isinstance(other, bytes):
            return self.to_bytes() == other
        else:
            raise TypeError(
                f"Cannot compare TreeValue of type {type(self)} with {type(other)}"
            )

    def __hash__(self) -> int:
        return hash((self._value, tuple(self._trailing_bits)))

    def __repr__(self) -> str:
        if self._trailing_bits:
            return f"{self._value!r} + bits: {''.join(str(bit) for bit in self._trailing_bits)}"
        else:
            return repr(self._value)

    def __deepcopy__(self, memo: dict[int, Any]) -> TreeValue:
        return TreeValue(
            self._value, trailing_bits=self._trailing_bits, allow_empty=True
        )

    def _inner_value(self, warn_message: str) -> str | bytes | int:
        """
        Don't you dare using this outside this class! This is a dirty, dirty hack to support the legacy interface.
        """

        warnings.warn(warn_message, DeprecationWarning, stacklevel=2)

        match self.type_:
            case TreeValueType.STRING:
                return str(self)
            case TreeValueType.BYTES:
                return bytes(self)
            case TreeValueType.TRAILING_BITS_ONLY:
                return int(self)
            case TreeValueType.EMPTY:
                return ""
            case _:
                raise FandangoValueError(
                    f"Invalid value type: {type(self)}. This should not happen, please report this as a bug"
                )

    @classmethod
    def empty(cls) -> TreeValue:
        return TreeValue(None, trailing_bits=[], allow_empty=True)

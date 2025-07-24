from __future__ import annotations
from types import NoneType
from typing import Any, Optional
import warnings

from fandango.errors import FandangoConversionError, FandangoValueError

STRING_TO_BYTES_ENCODING = "utf-8"  # according to the docs
BYTES_TO_STRING_ENCODING = "latin-1"  # according to the docs


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


# Shared argument unwrapping for operator and attribute delegation


def _unwrap_for_operator(arg):
    # Can't import DerivationTree directly due to circular import, so check by name
    if type(arg).__name__ == "TreeValue":
        # Inline the logic from to_inner_value
        if arg.is_type(str):
            return str(arg)
        elif arg.is_type(bytes):
            return bytes(arg)
        elif arg.is_type(NoneType):
            return int(arg)
        else:
            return arg._value
    elif type(arg).__name__ == "DerivationTree":
        return _unwrap_for_operator(arg.value())
    return arg


def delegate_dunders(to_method, dunder_names):
    """
    Decorator to add dunder methods to a class, delegating to the result of `to_method(self)`.
    """

    def make_method(name):
        def method(self, *args, **kwargs):
            warnings.warn(
                f"Using {name} on {type(self).__name__} is deprecated.",
                DeprecationWarning,
                stacklevel=2,
            )
            new_args = tuple(_unwrap_for_operator(arg) for arg in args)
            new_kwargs = {k: _unwrap_for_operator(v) for k, v in kwargs.items()}
            # For TreeValue, use self directly, not self.to_inner_value()
            if type(self).__name__ == "TreeValue":
                left = _unwrap_for_operator(self)
            else:
                left = getattr(self, to_method)()

            return getattr(left, name)(*new_args, **new_kwargs)

        return method

    def decorator(cls):
        for name in dunder_names:
            setattr(cls, name, make_method(name))
        return cls

    return decorator


DUNDER_METHODS = [
    "__add__",
    "__radd__",
    "__sub__",
    "__mul__",
    "__truediv__",
    "__floordiv__",
    "__mod__",
    "__pow__",
    "__and__",
    "__or__",
    "__xor__",
    "__lt__",
    "__le__",
    "__gt__",
    "__ge__",
    "__contains__",
]


# delegate_dunders and DUNDER_METHODS are now the canonical implementation for operator delegation.
@delegate_dunders("to_inner_value", DUNDER_METHODS)
class TreeValue:
    def __init__(
        self,
        value: str | bytes | int | None,
        *,
        trailing_bits: list[int] = [],
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
            assert len(trailing_bits) > 0, "None values must have trailing bits"

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
    def type_(self) -> type:
        return type(self._value)

    def is_type(self, type_: type) -> bool:
        return isinstance(self._value, type_)

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
            return self.can_compare_with(right._value)

        return (
            (isinstance(right, int) and self._value is None)
            or (isinstance(right, str) and self.is_type(str))
            or (isinstance(right, bytes) and self.is_type(bytes))
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
        return TreeValue(self._value, trailing_bits=self._trailing_bits)

    def __getattr__(self, name: str) -> Any:
        # Check if the attribute exists on the instance
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass

        warnings.warn(
            f"Using functions on the underlying types of DerivationTree and TreeValue types is deprecated.  Use the `str` or `bytes` to explicitly convert to the desired type first. TreeValue has no attribute {name}",
            DeprecationWarning,
        )

        def wrapper(*args, **kwargs):
            errors: list[tuple[str, Any]] = []

            unwrapped_args = tuple(_unwrap_for_operator(arg) for arg in args)
            unwrapped_kwargs = {
                key: _unwrap_for_operator(value) for key, value in kwargs.items()
            }

            for blank in ("", b"", 0):
                if hasattr(blank, name):
                    try:
                        converted = type(blank)(self)
                        attr = getattr(converted, name)
                        res = attr(*unwrapped_args, **unwrapped_kwargs)
                        return res
                    except Exception as e:
                        errors.append((type(blank).__name__, e))

            stringified_errors = "\n".join(f"{k}: {e}" for k, e in errors)
            stringified_args = ", ".join(
                f"{arg!r}(type: {type(arg).__name__})" for arg in args
            )
            stringified_kwargs = ", ".join(
                f"{k!r}={v!r}(type: {type(v).__name__})" for k, v in kwargs.items()
            )
            stringified_unwrapped_args = ", ".join(
                f"{arg!r}(type: {type(arg).__name__})" for arg in unwrapped_args
            )
            stringified_unwrapped_kwargs = ", ".join(
                f"{k!r}={v!r}(type: {type(v).__name__})"
                for k, v in unwrapped_kwargs.items()
            )

            raise AttributeError(
                f"TreeValue has no attribute {name} or all application attempts failed, "
                "possibly because the function call threw an exception, "
                f"errors during application attempts: {stringified_errors},\n"
                f"args: {stringified_args},\n"
                f"kwargs: {stringified_kwargs},\n"
                f"unwrapped_args: {stringified_unwrapped_args},\n"
                f"unwrapped_kwargs: {stringified_unwrapped_kwargs}"
            )

        return wrapper

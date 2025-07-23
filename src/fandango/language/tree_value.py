from __future__ import annotations
import enum

from fandango.errors import FandangoValueError


STRING_TO_BYTES_ENCODING = "utf-8"  # according to the docs
BYTES_TO_STRING_ENCODING = "latin-1"  # according to the docs


def trailing_bits_to_int(trailing_bits: list[int]) -> int:
    """
    Convert a list of trailing bits to an integer.

    The bits are assumed to be in big endian order and are not checked for validity (assumed to be 0 or 1)
    """
    return sum(bit << i for i, bit in enumerate(reversed(trailing_bits)))


class TreeValueType(enum.Enum):
    STRING = "string"
    BYTES = "bytes"
    TRAILING_BITS_ONLY = "trailing_bits"
    EMPTY = "empty"


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

        :raises ValueError: If the trailing bits don't sum up to a perfect number of bytes.
        """
        if not self._trailing_bits:
            return

        if len(self._trailing_bits) % 8 != 0:
            raise ValueError(
                "Trailing bits are not a multiple of 8, currently have "
                f"{len(self._trailing_bits)} bits"
            )

        num = trailing_bits_to_int(self._trailing_bits)
        bytes_ = num.to_bytes(len(self._trailing_bits) // 8)
        self._trailing_bits = []
        if isinstance(self._value, str):
            self._value = self._value.encode(encoding=str_to_bytes_encoding) + bytes_
        elif isinstance(self._value, bytes):
            self._value = self._value + bytes_
        elif self._value is None:
            self._value = bytes_
        else:
            raise ValueError(f"Invalid value type: {type(self._value)}")

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
                    self._value.encode(str_to_bytes_encoding) + other._value,
                    trailing_bits=other._trailing_bits,
                )

        elif isinstance(self._value, bytes):
            if isinstance(other._value, str):
                return TreeValue(
                    self._value + other._value.encode(str_to_bytes_encoding),
                    trailing_bits=other._trailing_bits,
                )
            elif isinstance(other._value, bytes):
                return TreeValue(
                    self._value + other._value,
                    trailing_bits=other._trailing_bits,
                )
        raise FandangoValueError(
            f"Cannot compute {self._value!r} + {other._value!r}, should not happen"
        )

    def can_compare_with(self, right: object) -> bool:
        if isinstance(right, TreeValue):
            return True

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
        :return: A string.
        """
        # encoding with the same encoding in both direction
        self._reduce_trailing_bits(str_to_bytes_encoding=bytes_to_str_encoding)
        if isinstance(self._value, str):
            return self._value
        if isinstance(self._value, bytes):
            return self._value.decode(encoding=bytes_to_str_encoding)
        raise ValueError(f"Invalid value type: {type(self._value)}")

    def to_bytes(
        self,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
    ) -> bytes:
        """
        Convert the TreeValue to bytes.

        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :return: A bytes object.
        """
        self._reduce_trailing_bits(str_to_bytes_encoding=str_to_bytes_encoding)
        if isinstance(self._value, bytes):
            return self._value
        elif isinstance(self._value, str):
            return self._value.encode(encoding=str_to_bytes_encoding)
        raise ValueError(f"Invalid value type: {type(self._value)}")

    def to_bits(
        self,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
    ) -> str:
        """
        Convert the TreeValue to a string of 0s and 1s representing bits.

        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :return: A string of bits.
        """
        if self._value is None:
            value = ""
        elif isinstance(self._value, bytes):
            value = "".join(f"{byte_:08b}" for byte_ in self._value)
        elif isinstance(self._value, str):
            value = "".join(
                f"{byte_:08b}"
                for byte_ in self._value.encode(encoding=str_to_bytes_encoding)
            )
        else:
            raise ValueError(f"Invalid value type: {type(self._value)}")

        trailing_bits = "".join(str(bit) for bit in self._trailing_bits)

        return value + trailing_bits

    def to_int(
        self,
        str_to_bytes_encoding: str = STRING_TO_BYTES_ENCODING,
    ) -> int:
        """
        Convert the TreeValue to an integer.

        Strings are converted to ints using int(), bytes are converted to ints using int.from_bytes().

        If bits were ever included, the underlying data structure is bytes.

        :param str_to_bytes_encoding: The encoding to use when converting strings to bytes.
        :return: An integer.
        """
        if self._value is None:  # only trailing bits
            return trailing_bits_to_int(self._trailing_bits)
        else:
            self._reduce_trailing_bits(str_to_bytes_encoding=str_to_bytes_encoding)
            if isinstance(self._value, str):
                return int(self._value)
            elif isinstance(self._value, bytes):
                return int.from_bytes(self._value)
            else:
                raise ValueError(f"Invalid value type: {type(self._value)}")

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

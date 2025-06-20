import random
import struct
from abc import ABC, abstractmethod
from enum import Enum, auto

from fandango import DerivationTree

# Magic Values taken from LibAFL
ARITH_MAX = 35
MAX_SIZE = 1048576

# Interesting values from LibAFL
INTERESTING_VALUES = {
    1: [-128, -1, 0, 1, 16, 32, 64, 100, 127],
    2: [
        -128,
        -1,
        0,
        1,
        16,
        32,
        64,
        100,
        127,
        -32768,
        -129,
        128,
        255,
        256,
        512,
        1000,
        1024,
        4096,
        32767,
    ],
    4: [
        -128,
        -1,
        0,
        1,
        16,
        32,
        64,
        100,
        127,
        -32768,
        -129,
        128,
        255,
        256,
        512,
        1000,
        1024,
        4096,
        32767,
        -2147483648,
        -100663046,
        -32769,
        32768,
        65535,
        65536,
        100663045,
        2147483647,
    ],
}


def _wrapping_add(a: int, b: int, byte_size: int = 1) -> int:
    return (a + b) % (256**byte_size)


def _wrapping_sub(a: int, b: int, byte_size: int = 1) -> int:
    return (a - b) % (256**byte_size)


def _get_random_index(input: bytearray) -> int:
    """
    Returns a random index in the input_.

    :param input: The input_ to get the index from.
    :return: A random index in the input_, always valid as an index for the input_.
    """
    return random.randint(0, len(input) - 1)


def _get_random_range_of_length(input: bytearray, length: int) -> tuple[int, int]:
    """
    Returns a random range of the given length in the input_.

    :param input: The input_ to get the range from.
    :param length: The length of the range to get.
    :return: A tuple of the start (inclusive) and end (exclusive) of the range.
    """

    if length == 0:
        raise ValueError("Length cannot be 0")
    if length > len(input):
        raise ValueError("Length is greater than the input_ size")
    start = random.randint(0, len(input) - length)
    end = start + length
    return start, end


def _get_random_range_with_max_length(
    input: bytearray, max_length: int
) -> tuple[int, int]:
    """
    Returns a random range of a length between 1 and the max length in the input_.

    :param input: The input_ to get the range from.
    :param max_length: The maximum length of the range to get.
    :return: A tuple of the start (inclusive) and end (exclusive) of the range.
    """
    if max_length > len(input):
        raise ValueError("Max length is greater than the input_ size")
    length = random.randint(1, max_length)
    return _get_random_range_of_length(input, length)


class ByteLevelMutationOperator(ABC):
    """Base class for all mutation operators that perform byte-level mutations on input_ data."""

    @abstractmethod
    def mutate(
        self,
        input: bytearray,
    ) -> bool:
        """
        Abstract method to perform byte-level mutation.

        :param input: The input_ to mutate.
        :return: True if the input_ was mutated, False otherwise.
        """
        pass


class BitFlipMutation(ByteLevelMutationOperator):
    """Flips a random bit in a random byte of the input_."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        offset = _get_random_index(input)
        input[offset] ^= 1 << random.randint(0, 7)
        return True


class ByteFlipMutation(ByteLevelMutationOperator):
    """Flips all bits in a random byte of the input_."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        offset = _get_random_index(input)
        input[offset] ^= 0xFF
        return True


class ByteIncMutation(ByteLevelMutationOperator):
    """Increments a random byte in the input_ by 1."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        offset = _get_random_index(input)
        input[offset] = _wrapping_add(input[offset], 1)
        return True


class ByteDecMutation(ByteLevelMutationOperator):
    """Decrements a random byte in the input_ by 1."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        offset = _get_random_index(input)
        input[offset] = _wrapping_sub(input[offset], 1)
        return True


class ByteNegMutation(ByteLevelMutationOperator):
    """Negates a random byte in the input_."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        offset = _get_random_index(input)
        value = _wrapping_add(input[offset] ^ 0xFF, 1)
        if value == input[offset]:
            return False
        input[offset] = value
        return True


class ByteRandMutation(ByteLevelMutationOperator):
    """Replaces a random byte in the input_ with a random value."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        offset = _get_random_index(input)
        new_val = random.randint(0, 255)
        if new_val == input[offset]:
            return False
        input[offset] = new_val
        return True


class ArithmeticOperation(Enum):
    """Enum for arithmetic operations used in mutations."""

    ADD = auto()
    SUB = auto()


def _get_format_string(num_bytes: int, little_endian: bool) -> str:
    if num_bytes == 1:
        format_string_size = "B"
    elif num_bytes == 2:
        format_string_size = "H"
    elif num_bytes == 4:
        format_string_size = "I"
    elif num_bytes == 8:
        format_string_size = "Q"
    else:
        raise ValueError(f"Unsupported number of bytes: {num_bytes}")

    format_string_endianness = "<" if little_endian else ">"
    return format_string_endianness + format_string_size


class MultiByteArithmeticMutation(ByteLevelMutationOperator):
    """Performs an addition or subtraction on a random (multi-byte) value in the input_, in either little or big endian."""

    def __init__(
        self, num_bytes: int, operation: ArithmeticOperation, little_endian: bool
    ):
        self.num_bytes = num_bytes
        self.operation = operation
        self.little_endian = little_endian
        self.format_string = _get_format_string(num_bytes, little_endian)
        match operation:
            case ArithmeticOperation.ADD:
                self.operation_function = _wrapping_add
            case ArithmeticOperation.SUB:
                self.operation_function = _wrapping_sub

    def mutate(self, input: bytearray) -> bool:
        if len(input) < self.num_bytes:
            return False

        offset, end = _get_random_range_of_length(input, self.num_bytes)
        val = struct.unpack(self.format_string, input[offset:end])[0]
        new_val = self.operation_function(
            val, random.randint(2, ARITH_MAX + 1), byte_size=self.num_bytes
        )
        # ensure a positive value for packing
        new_val = new_val % 256**self.num_bytes
        if new_val == val:
            return False
        struct.pack_into(self.format_string, input, offset, new_val)
        return True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(num_bytes={self.num_bytes}, "
            f"operation={self.operation}, "
            f"little_endian={self.little_endian})"
        )


class MultiByteInterestingMutation(ByteLevelMutationOperator):
    """Replaces a random (multi-byte) value in the input_ with a potentially interesting value."""

    def __init__(self, num_bytes: int):
        self.num_bytes = num_bytes
        self.format_string = _get_format_string(num_bytes, False)

    def mutate(self, input: bytearray) -> bool:
        if len(input) < self.num_bytes:
            return False

        start, end = _get_random_range_of_length(input, self.num_bytes)
        replacement_value = (
            random.choice(INTERESTING_VALUES[self.num_bytes]) % 256**self.num_bytes
        )
        if struct.unpack(self.format_string, input[start:end])[0] == replacement_value:
            return False
        struct.pack_into(self.format_string, input, start, replacement_value)
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(num_bytes={self.num_bytes})"


class BytesDeleteMutation(ByteLevelMutationOperator):
    """Deletes random bytes from the input_."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) < 2:
            return False

        num_bytes = random.randint(1, len(input) - 1)
        offset, end = _get_random_range_of_length(input, num_bytes)
        del input[offset:end]
        return True


class BytesExpandMutation(ByteLevelMutationOperator):
    """Extends the input_ by a subslice of itself."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size >= MAX_SIZE or size == 0:
            return False

        # Don't let input_ grow beyond MAX_SIZE
        max_value = min(16, size, MAX_SIZE - size)
        if max_value <= 0:
            return False
        amount = random.randint(1, max_value)

        start, end = _get_random_range_of_length(input, amount)
        input.extend(input[start:end])
        return True


class BytesInsertMutation(ByteLevelMutationOperator):
    """Inserts a slice consisting of a random value from the input_ into a random position in the input_."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size >= MAX_SIZE or size == 0:
            return False

        value = random.choice(input)

        amount = random.randint(1, 16)
        if size + amount > MAX_SIZE:
            if MAX_SIZE > size:
                amount = MAX_SIZE - size
            else:
                return False

        offset = _get_random_index(input)
        input[offset:offset] = [value] * amount
        return True


class BytesRandInsertMutation(ByteLevelMutationOperator):
    """Inserts a slice consisting of a random value into a random position in the input_."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size >= MAX_SIZE or size == 0:
            return False

        value = random.randint(0, 255)

        amount = random.randint(1, 16)
        if size + amount > MAX_SIZE:
            if MAX_SIZE > size:
                amount = MAX_SIZE - size
            else:
                return False

        offset = _get_random_index(input)
        input[offset:offset] = [value] * amount
        return True


class BytesSetMutation(ByteLevelMutationOperator):
    """Sets a random range in the input_ to a random value from the input_."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size == 0:
            return False

        value = random.choice(input)
        start, end = _get_random_range_with_max_length(input, min(size, 16))
        new_val = bytearray([value] * (end - start))
        if input[start:end] == new_val:
            return False
        input[start:end] = new_val
        return True


class BytesRandSetMutation(ByteLevelMutationOperator):
    """Sets a random range in the input_ to a random value."""

    def mutate(self, input: bytearray) -> bool:
        if len(input) == 0:
            return False

        value = random.randint(0, 255)
        start, end = _get_random_range_with_max_length(input, len(input))
        new_val = bytearray([value] * (end - start))
        if input[start:end] == new_val:
            return False
        input[start:end] = new_val
        return True


class BytesCopyMutation(ByteLevelMutationOperator):
    """Copies a random range in the input_ to a random position in the input_."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size < 2:
            return False

        target_start = _get_random_index(input)
        source_start, source_end = _get_random_range_with_max_length(
            input, size - target_start
        )
        target_end = target_start + source_end - source_start

        if input[target_start:target_end] == input[source_start:source_end]:
            return False
        input[target_start:target_end] = input[source_start:source_end]
        return True


class BytesInsertCopyMutation(ByteLevelMutationOperator):
    """Inserts a copy of a random range in the input_ into a random position in the input_."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size < 2 or size >= MAX_SIZE:
            return False

        target_start, _ = _get_random_range_of_length(input, 2)
        max_insert_len = random.randint(
            1, min(16, size - target_start, MAX_SIZE - size)
        )
        source_start, _ = _get_random_range_of_length(input, max_insert_len)
        temp_buf = input[source_start : source_start + max_insert_len]
        input[target_start + max_insert_len : size + max_insert_len] = input[
            target_start:size
        ]
        input[target_start : target_start + max_insert_len] = temp_buf
        return True


class BytesSwapMutation(ByteLevelMutationOperator):
    """Swaps a random range in the input_ with a random range in the input_."""

    def mutate(self, input: bytearray) -> bool:
        size = len(input)
        if size < 2:
            return False
        first_start, first_end = _get_random_range_with_max_length(input, len(input))
        if first_start > 0 and random.choice([True, False]):
            # second range comes before first
            second_start, second_end = _get_random_range_with_max_length(
                bytearray(input[:first_start]), first_start
            )

            input_copy = input[second_start:first_end]

            second_temp = input[second_start:second_end]
            middle_temp = input[second_end:first_start]
            first_temp = input[first_start:first_end]

            input[second_start : second_start + len(first_temp)] = first_temp
            input[
                second_start
                + len(first_temp) : second_start
                + len(first_temp)
                + len(middle_temp)
            ] = middle_temp
            input[first_end - len(second_temp) : first_end] = second_temp

            if input[second_start:first_end] == input_copy:
                return False
        elif first_end < size - 1:
            # second range comes after first
            second_start, second_end = _get_random_range_with_max_length(
                bytearray(input[first_end:]), size - first_end
            )
            second_start, second_end = second_start + first_end, second_end + first_end

            input_copy = input[first_start:second_end]

            first_temp = input[first_start:first_end]
            middle_temp = input[first_end:second_start]
            second_temp = input[second_start:second_end]

            input[first_start : first_start + len(second_temp)] = second_temp
            input[
                first_start
                + len(second_temp) : first_start
                + len(second_temp)
                + len(middle_temp)
            ] = middle_temp
            input[second_end - len(first_temp) : second_end] = first_temp

            if input[first_start:second_end] == input_copy:
                return False
        else:
            return False

        return True


def havoc_mutations() -> tuple[ByteLevelMutationOperator, ...]:
    return (
        BitFlipMutation(),
        ByteFlipMutation(),
        ByteIncMutation(),
        ByteDecMutation(),
        ByteNegMutation(),
        ByteRandMutation(),
        MultiByteArithmeticMutation(1, ArithmeticOperation.ADD, False),
        MultiByteArithmeticMutation(1, ArithmeticOperation.SUB, False),
        # for 1 byte, little endian and big endian are the same
        MultiByteArithmeticMutation(2, ArithmeticOperation.ADD, False),
        MultiByteArithmeticMutation(2, ArithmeticOperation.SUB, False),
        MultiByteArithmeticMutation(2, ArithmeticOperation.ADD, True),
        MultiByteArithmeticMutation(2, ArithmeticOperation.SUB, True),
        MultiByteArithmeticMutation(4, ArithmeticOperation.ADD, False),
        MultiByteArithmeticMutation(4, ArithmeticOperation.SUB, False),
        MultiByteArithmeticMutation(4, ArithmeticOperation.ADD, True),
        MultiByteArithmeticMutation(4, ArithmeticOperation.SUB, True),
        MultiByteArithmeticMutation(8, ArithmeticOperation.ADD, False),
        MultiByteArithmeticMutation(8, ArithmeticOperation.SUB, False),
        MultiByteArithmeticMutation(8, ArithmeticOperation.ADD, True),
        MultiByteArithmeticMutation(8, ArithmeticOperation.SUB, True),
        MultiByteInterestingMutation(1),
        MultiByteInterestingMutation(2),
        MultiByteInterestingMutation(4),
        BytesDeleteMutation(),
        BytesExpandMutation(),
        BytesInsertMutation(),
        BytesRandInsertMutation(),
        BytesSetMutation(),
        BytesRandSetMutation(),
        BytesCopyMutation(),
        BytesInsertCopyMutation(),
        BytesSwapMutation(),
    )


def havoc_mutate(
    input_: DerivationTree,
    mutations: (
        list[ByteLevelMutationOperator] | tuple[ByteLevelMutationOperator, ...]
    ) = havoc_mutations(),
    max_stack_pow=7,
    nop_probability=0,
) -> bytes:
    """
    Mutates the input using the given mutations, defaulting to a .

    :param input_: The input to mutate.
    :param mutations: The mutations to use.
    :param max_stack_pow: The maximum power of 2 for the stack size.
    :return: The mutated input.
    """
    if random.random() < nop_probability:
        return input_.to_bytes()

    inp = bytearray(input_.to_bytes())
    for _ in range(1 << random.randint(0, max_stack_pow)):
        mutation = random.choice(mutations)
        mutation.mutate(inp)
    fixed = bytes(inp)
    return fixed

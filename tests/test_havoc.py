#!/usr/bin/env pytest

from collections import Counter
import pytest

from fandango.evolution import havoc

ITERS = 100000
INPUT_SIZE = 100


def adjacent_diff(input_: bytearray) -> list[int]:
    return [input_[i] - input_[i - 1] for i in range(1, len(input_))]


def test_wrapping_add():
    from fandango.evolution.havoc import _wrapping_add

    assert _wrapping_add(1, 1) == 2
    assert _wrapping_add(256 - 1, 1) == 0
    assert _wrapping_add(256**2 - 1, 1, byte_size=2) == 0
    assert _wrapping_add(256**4 - 1, 1, byte_size=4) == 0


def test_wrapping_sub():
    from fandango.evolution.havoc import _wrapping_sub

    assert _wrapping_sub(1, 1) == 0
    assert _wrapping_sub(0, 1) == 256 - 1
    assert _wrapping_sub(0, 1, byte_size=2) == 256**2 - 1
    assert _wrapping_sub(0, 1, byte_size=4) == 256**4 - 1


def test_get_random_index():
    from fandango.evolution.havoc import _get_random_index

    input = bytearray([0] * INPUT_SIZE)
    for _ in range(ITERS):
        index = _get_random_index(input)
        assert index < INPUT_SIZE
        assert index >= 0
        assert input[index] == 0


def test_get_random_range_of_length():
    from fandango.evolution.havoc import _get_random_range_of_length

    # testing edge cases of length values
    with pytest.raises(ValueError):
        _get_random_range_of_length(bytearray([0] * INPUT_SIZE), 0)
    with pytest.raises(ValueError):
        _get_random_range_of_length(bytearray([0] * INPUT_SIZE), INPUT_SIZE + 1)

    # testing edge cases of input_ size
    with pytest.raises(ValueError):
        _get_random_range_of_length(bytearray([]), 1)

    input = bytearray([0] * INPUT_SIZE)
    for _ in range(ITERS):
        for length in [1, INPUT_SIZE]:
            start, end = _get_random_range_of_length(input, length)
            assert end - start == length
            assert start >= 0
            assert end <= INPUT_SIZE


def test_get_random_range_with_max_length():
    from fandango.evolution.havoc import _get_random_range_with_max_length

    # testing edge cases of length values
    with pytest.raises(ValueError):
        _get_random_range_with_max_length(bytearray([0] * INPUT_SIZE), 0)
    with pytest.raises(ValueError):
        _get_random_range_with_max_length(bytearray([0] * INPUT_SIZE), INPUT_SIZE + 1)

    # testing edge cases of input_ size
    with pytest.raises(ValueError):
        _get_random_range_with_max_length(bytearray([]), 1)

    input = bytearray([0] * INPUT_SIZE)
    for _ in range(1, ITERS):
        for max_length in [1, INPUT_SIZE]:
            start, end = _get_random_range_with_max_length(input, max_length)
            assert start < end
            assert start >= 0
            assert end <= INPUT_SIZE
            assert end - start <= max_length
            assert end - start >= 1


@pytest.mark.parametrize("mutation", havoc.havoc_mutations())
@pytest.mark.parametrize("input_size", [0, 1, 2, 255, 256])
def test_return_value(mutation, input_size):
    for _ in range(ITERS):
        input = bytearray(range(input_size))
        input_copy = input.copy()
        expected = mutation.mutate(input)
        actual = input != input_copy
        assert expected == actual, (
            f"Mutator {mutation} reported to {'not ' if not expected else ''}have mutated, "
            f"but the input was {'not ' if not actual else ''}mutated.\n"
            f"Original input: {input_copy}\nMutated input: {input}"
        )


@pytest.mark.parametrize("mutation", havoc.havoc_mutations())
@pytest.mark.parametrize("input_size", [0, 1, 2, 255, 256])
def test_size_changes(mutation, input_size):
    should_change_size = mutation.__class__.__name__ in [
        "BytesDeleteMutation",
        "BytesExpandMutation",
        "BytesInsertMutation",
        "BytesRandInsertMutation",
        "BytesInsertCopyMutation",
    ]
    for _ in range(ITERS):
        input = bytearray(range(input_size))
        expected_size = len(input)
        has_mutated = mutation.mutate(input)
        if has_mutated:
            assert (len(input) != expected_size) == should_change_size, (
                f"{mutation} mutated and should {'not ' if not should_change_size else ''}"
                f"change size but has {'not ' if should_change_size else ''}. "
                f"Input length: {len(input)}, expected size: {expected_size}"
            )
        else:
            assert (
                len(input) == expected_size
            ), f"{mutation} did not mutate but changed size"


def test_bit_flip_mutation():
    from fandango.evolution.havoc import BitFlipMutation

    mutation = BitFlipMutation()
    for _ in range(ITERS):
        input = bytearray([0] * INPUT_SIZE)
        assert mutation.mutate(input)
        c = Counter(input)
        assert c[0] == INPUT_SIZE - 1
        assert len(c.keys()) == 2
        other_key = [k for k in c.keys() if k != 0][0]
        assert bin(other_key).lstrip("0b").rstrip("0") == "1"


def test_byte_flip_mutation():
    from fandango.evolution.havoc import ByteFlipMutation

    mutation = ByteFlipMutation()
    for _ in range(ITERS):
        input = bytearray([0] * INPUT_SIZE)
        assert mutation.mutate(input)
        c = Counter(input)
        assert c[0] == INPUT_SIZE - 1
        assert c[0xFF] == 1


def test_byte_inc_mutation():
    from fandango.evolution.havoc import ByteIncMutation

    mutation = ByteIncMutation()

    for _ in range(ITERS):
        for value in [0, 1, 255]:
            input = bytearray([value] * INPUT_SIZE)
            assert mutation.mutate(input)
            c = Counter(input)
            assert c[value] == INPUT_SIZE - 1
            assert c[(value + 1) % 256] == 1


def test_byte_dec_mutation():
    from fandango.evolution.havoc import ByteDecMutation

    mutation = ByteDecMutation()
    for _ in range(ITERS):
        for value in [0, 1, 255]:
            input = bytearray([value] * INPUT_SIZE)
            assert mutation.mutate(input)
            c = Counter(input)
            assert c[value] == INPUT_SIZE - 1
            assert c[(value - 1) % 256] == 1


def test_byte_neg_mutation():
    from fandango.evolution.havoc import ByteNegMutation

    mutation = ByteNegMutation()
    for _ in range(ITERS):
        input = bytearray([1] * INPUT_SIZE)
        assert mutation.mutate(input)
        c = Counter(input)
        assert c[1] == INPUT_SIZE - 1
        assert c[255] == 1, f"Found unexpected count: {str(c)} in input: {str(input)}"

        input = bytearray(range(256))
        # 128 maps back to 128, so it's possible there is no mutation
        if mutation.mutate(input):
            found_mutation = False
            for i in range(len(input)):
                if i != input[i]:
                    assert not found_mutation, "Found multiple mutations"
                    found_mutation = True
                    assert input[i] + i == 256
            assert found_mutation, "No mutation found yet reported to be mutated"


def test_byte_rand_mutation():
    from fandango.evolution.havoc import ByteRandMutation

    mutation = ByteRandMutation()
    for _ in range(ITERS):
        for i in [0, 1, 255]:
            input = bytearray([i] * INPUT_SIZE)
            mutated = mutation.mutate(input)
            assert mutated == (
                input != (bytearray([i] * INPUT_SIZE))
            ), f"Found unexpected mutated input: {str(input)}"


@pytest.mark.parametrize(
    "mode",
    [(havoc.ArithmeticOperation.ADD, 0xFF), (havoc.ArithmeticOperation.SUB, 0x00)],
)
@pytest.mark.parametrize("num_bytes", [1, 2, 4, 8])
@pytest.mark.parametrize("little_endian", [True, False])
def test_multi_byte_arithmetic_mutation(mode, num_bytes, little_endian):
    from fandango.evolution.havoc import MultiByteArithmeticMutation

    mutation = MultiByteArithmeticMutation(num_bytes, mode[0], little_endian)
    for _ in range(ITERS):
        input = bytearray([mode[1]] * INPUT_SIZE)
        has_mutated = mutation.mutate(input)
        if has_mutated:
            assert input != bytearray([mode[1]] * INPUT_SIZE)
            # overflow should lead to all values being changed
            assert num_bytes == len([i for i in input if i != mode[1]])
        else:
            assert input == bytearray([mode[1]] * INPUT_SIZE)


@pytest.mark.parametrize("num_bytes", [1, 2, 4])
def test_multi_byte_interesting_mutation(num_bytes):
    from fandango.evolution.havoc import MultiByteInterestingMutation

    UNINTERESTING_BYTE = ord("A")
    mutation = MultiByteInterestingMutation(num_bytes)
    for _ in range(ITERS):
        input = bytearray([UNINTERESTING_BYTE] * INPUT_SIZE)
        assert mutation.mutate(input)
        c = Counter(input)
        assert c[UNINTERESTING_BYTE] == INPUT_SIZE - num_bytes
        other_values = [v for (k, v) in c.items() if k != UNINTERESTING_BYTE]
        assert sum(other_values) == num_bytes


def test_bytes_delete_mutation():
    from fandango.evolution.havoc import BytesDeleteMutation

    mutation = BytesDeleteMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        assert mutation.mutate(input)
        assert len(input) < 256
        c = Counter(adjacent_diff(input))
        other_keys = [k for k in c.keys() if k != 1]

        match len(other_keys):
            case 0:
                # deletion from the extremes
                mutated_from_start = input[0] != 0
                mutated_from_end = input[-1] != 255
                assert mutated_from_start ^ mutated_from_end
            case 1:
                # deletion from the middle
                assert len(input) + other_keys[0] == 257  # diff => prior length + 1
            case _:
                # should never happen
                assert False


def test_bytes_expand_mutation():
    from fandango.evolution.havoc import BytesExpandMutation

    mutation = BytesExpandMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        assert mutation.mutate(input)
        assert input[256:] in input[:256]


def test_bytes_insert_mutation():
    from fandango.evolution.havoc import BytesInsertMutation

    mutation = BytesInsertMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        assert mutation.mutate(input)
        start = -1
        stop = -1
        jumps = []
        for i in range(1, len(input)):
            if input[i] == input[i - 1]:
                if start == -1:
                    start = i
                elif len([k for k in input[start:i] if k != input[i]]) == 0:
                    # if all values between start and i are the same, we are in the repetition
                    stop = i
                else:
                    assert (
                        False
                    ), f"Found multiple repetitions after index {i} in input {input}. start: {start}, stop: {stop}"
            elif input[i] != input[i - 1] + 1:
                jumps.append(i)
        if len(jumps) > 2:
            assert False, f"Found unexpected number of jumps: {jumps} in input {input}"

        input = bytearray([0] * INPUT_SIZE)
        assert mutation.mutate(input)
        assert len(input) > INPUT_SIZE
        assert len(Counter(input)) == 1


def test_bytes_rand_insert_mutation():
    from fandango.evolution.havoc import BytesRandInsertMutation

    mutation = BytesRandInsertMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        assert mutation.mutate(input)
        start = -1
        stop = -1
        jumps = []
        for i in range(1, len(input)):
            if input[i] == input[i - 1]:
                if start == -1:
                    start = i
                elif len([k for k in input[start:i] if k != input[i]]) == 0:
                    # if all values between start and i are the same, we are in the repetition
                    stop = i
                else:
                    assert (
                        False
                    ), f"Found multiple repetitions after index {i} in input {input}. start: {start}, stop: {stop}"
            elif input[i] != input[i - 1] + 1:
                jumps.append(i)
        if len(jumps) > 2:
            assert False, f"Found unexpected number of jumps: {jumps} in input {input}"

        input = bytearray([0] * INPUT_SIZE)
        assert mutation.mutate(input)
        assert len(input) > INPUT_SIZE
        c = Counter(input)
        other_keys = [k for k in c.keys() if k != 0]
        match len(other_keys):
            case 0:
                pass  # chose 0 again
            case 1:
                indices = [i for i, v in enumerate(input) if v == other_keys[0]]
                # ensure all other values are consecutive
                assert (
                    len(
                        [
                            v
                            for i, v in enumerate(indices[:-1])
                            if v + 1 != indices[i + 1]
                        ]
                    )
                    == 0
                )
            case _:
                assert False


def test_bytes_set_mutation():
    from fandango.evolution.havoc import BytesSetMutation

    mutation = BytesSetMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        has_mutated = mutation.mutate(input)
        if not has_mutated:
            assert input == bytearray(range(256))
            return
        start = -1
        stop = -1
        jumps = []
        for i in range(1, len(input)):
            if input[i] == input[i - 1]:
                if start == -1:
                    start = i
                elif len([k for k in input[start:i] if k != input[i]]) == 0:
                    # if all values between start and i are the same, we are in the repetition
                    stop = i
                else:
                    assert (
                        False
                    ), f"Found multiple repetitions after index {i} in input {input}. start: {start}, stop: {stop}"
            elif input[i] != input[i - 1] + 1:
                jumps.append(i)
        if len(jumps) > 2:
            assert False, f"Found unexpected number of jumps: {jumps} in input {input}"

        input = bytearray([0] * INPUT_SIZE)
        mutation.mutate(input)
        assert len(Counter(input)) == 1


def test_bytes_rand_set_mutation():
    from fandango.evolution.havoc import BytesRandSetMutation

    mutation = BytesRandSetMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        if not mutation.mutate(input):
            assert input == bytearray(range(256))
            return
        start = -1
        stop = -1
        jumps = []
        for i in range(1, len(input)):
            if input[i] == input[i - 1]:
                if start == -1:
                    start = i
                elif len([k for k in input[start:i] if k != input[i]]) == 0:
                    # if all values between start and i are the same, we are in the repetition
                    stop = i
                else:
                    assert (
                        False
                    ), f"Found multiple repetitions after index {i} in input {input}. start: {start}, stop: {stop}"
            elif input[i] != input[i - 1] + 1:
                jumps.append(i)
        if len(jumps) > 2:
            assert False, f"Found unexpected number of jumps: {jumps} in input {input}"

        input = bytearray([0] * INPUT_SIZE)
        if not mutation.mutate(input):
            assert input == bytearray([0] * INPUT_SIZE)
            return
        c = Counter(input)
        other_keys = [k for k in c.keys() if k != 0]
        match len(other_keys):
            case 0:
                pass  # chose 0 again
            case 1:
                indices = [i for i, v in enumerate(input) if v == other_keys[0]]
                # ensure all other values are consecutive
                assert (
                    len(
                        [
                            v
                            for i, v in enumerate(indices[:-1])
                            if v + 1 != indices[i + 1]
                        ]
                    )
                    == 0
                )
            case _:
                assert False


def test_bytes_copy_mutation():
    from fandango.evolution.havoc import BytesCopyMutation

    mutation = BytesCopyMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        if not mutation.mutate(input):
            assert input == bytearray(range(256))
            return
        found_duplicate_slice = False
        for start in range(len(input)):
            for end in range(start + 1, len(input)):
                if input[start:end] in input[start + 1 :]:
                    found_duplicate_slice = True
                    break
            if found_duplicate_slice:
                break
        assert found_duplicate_slice, f"Did not find duplicate slice in input {input}"


def test_bytes_insert_copy_mutation():
    from fandango.evolution.havoc import BytesInsertCopyMutation

    mutation = BytesInsertCopyMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        input_copy = input.copy()
        assert mutation.mutate(input)
        diffs = []
        for i in range(1, len(input)):
            if input[i] != input[i - 1] + 1:
                diffs.append(i)
        if len(diffs) == 1:
            # insertion to the extremes
            i = diffs[0]
            if input[:i] == input_copy:  # insertion to the end
                assert input[i:] in input[:i]
            elif input[i:] == input_copy:  # insertion to the start
                assert input[:i] in input[i:]
        elif len(diffs) == 2:
            # insertion to the middle
            i, j = diffs
            temp_reconstructed = input[:i] + input[j:]
            assert (
                input[i:j] in temp_reconstructed
            ), f"input: {input}\ninserted slice (from {i} to {j}): {input[i:j]}"
        else:
            assert False, f"Found unexpected number of diffs: {diffs}"


def test_bytes_swap_mutation():
    from fandango.evolution.havoc import BytesSwapMutation

    mutation = BytesSwapMutation()
    for _ in range(ITERS):
        input = bytearray(range(256))
        input_copy = input.copy()
        if not mutation.mutate(input):
            assert input == input_copy
            return

        assert input != input_copy, "Input is not mutated"
        assert (
            bytearray(sorted(input)) == input_copy
        ), "Input does not contain all elements anymore"

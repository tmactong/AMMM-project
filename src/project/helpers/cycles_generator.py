import itertools
import typing


def get_combinations(count: int, length: int) -> typing.List[typing.Tuple[int, ...]]:
    return list(itertools.combinations(range(1, count+1), length))

def get_permutations_without_using_itertools(digits: typing.List[int]) -> typing.Iterable[str]:
    needed_digits = len(digits)
    def inner_get(fixed_digits:typing.List[int], residual_digits: typing.List[int]) -> typing.Iterable[str]:
        if len(fixed_digits) + 1 == needed_digits:
            yield ''.join(list(map(str, fixed_digits + residual_digits)))
        else:
            for residual_digit in residual_digits:
                yield from inner_get(
                    fixed_digits + [residual_digit],
                    [ x for x in residual_digits if x != residual_digit]
                )
    yield from inner_get([], digits)


def generate_branches(
        branch: typing.List[int],
        pairs: typing.List[typing.Tuple[int, int]]
) -> typing.Iterable[typing.List[int]]:
    continue_search = False
    for pair in pairs:
        if pair[0] == branch[-1]:
            continue_search = True
            yield from generate_branches(branch + [pair[1]], [x for x in pairs if pair[0] not in x])
    if not continue_search:
        yield branch

"""
def get_no_repetition_sequences(digits: typing.List[int]) -> typing.List[str]:
    permutations = get_permutations(digits)
    combinations, all_sequences = list(), list()
    for permutation in permutations:
        if permutation not in all_sequences:
            extended_permutation = permutation + permutation
            reversed_permutation = extended_permutation[::-1]
            sequences = [extended_permutation[i:i + len(digits)] for i in range(len(digits))]
            sequences.extend([reversed_permutation[i:i + len(digits)] for i in range(len(digits))])
            combinations.append(permutation)
            all_sequences.extend(sequences)
    return combinations
"""

def generate_cycle_patterns(digits: typing.List[int]) -> typing.Iterable[typing.List[int]]:
    repetitions = len(digits) - 2
    for i in range(repetitions):
        prefix = [1, digits[i + 1]]
        moving_digits = (digits[1:i + 1] + digits[i + 2:-1])[:i]
        residual_digits = digits[1:i + 1] + digits[i + 2:]
        permutations = itertools.permutations(residual_digits)
        for permutation in permutations:
            ends_with_moving_digit = False
            for moving_digit in moving_digits:
                if permutation[-1] == moving_digit:
                    ends_with_moving_digit = True
            if not ends_with_moving_digit:
                yield prefix + list(permutation)


if __name__ == '__main__':
    n = 6
    # no_repetition_sequences = get_no_repetition_sequences(list(range(1, 1 + n)))
    # print("no repetition sequences: ", len(no_repetition_sequences), no_repetition_sequences)
    # print(20 * "-")
    generated_sequences = list(generate_cycle_patterns(list(range(1, 1 + n))))
    print("generated sequences:     ", len(generated_sequences), generated_sequences)
    # print("two sequences equals: ", no_repetition_sequences == generated_sequences)
    #p = list(get_permutations_without_using_itertools([1,2,3,4]))
    #print(len(p), p)
    # print(get_combinations(5, 2))

import itertools
import typing


def get_combinations(count: int, length: int) -> typing.List[typing.Tuple[int, ...]]:
    return list(itertools.combinations(range(1, count+1), length))

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


def generate_all_permutations(total_count:int, pair:typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
    members = list(itertools.filterfalse(lambda x: x in pair, range(1, total_count + 1)))
    for i in range(1, len(members) + 1):
        for j in itertools.permutations(members, i):
            yield [pair[1]] + list(j) + [pair[0]]


if __name__ == '__main__':
    n = 4
    # generated_sequences = list(generate_cycle_patterns(list(range(1, 1 + n))))
    # print("generated sequences:", len(generated_sequences), generated_sequences)
    # print(get_combinations(5, 3))
    pairs = generate_all_permutations(10, (1,3))
    print(len(list(pairs)))

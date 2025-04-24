import typing
import itertools
from src.project.helpers.cycles_generator import generate_branches

MemberCount = 10
CoveredPairs = []
NotCoveredPairs = []

for i in range(1, MemberCount + 1):
    for j in range(1, MemberCount + 1):
        if i != j:
            CoveredPairs.append((i, j))

for pair in [(2,3), (5,6),(7,8), (5,9), (9,3), (10,2)]:
#for pair in [(2, 3)]:
    CoveredPairs.remove(pair)
    CoveredPairs.remove(pair[::-1])
    NotCoveredPairs.append(pair)
    NotCoveredPairs.append(pair[::-1])


def newly_constructed_cycles(member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
    for branch in generate_branches([member_pair[1]], CoveredPairs):
        if member_pair[0] in branch:
            yield branch[:branch.index(member_pair[0]) + 1]


def old_method(member_pair: typing.Tuple[int, int]) -> typing.List[typing.List[int]]:
    uniq_cycles = list()
    for cycle in newly_constructed_cycles(member_pair):
        if cycle not in uniq_cycles:
            uniq_cycles.append(cycle)
    return [cycle for cycle in uniq_cycles if cycle != list(member_pair[::-1])]


def all_permutation_method(member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
    members = list(itertools.filterfalse(lambda x: x in member_pair, range(1, MemberCount + 1)))
    for i in range(1, len(members) +1):
        for j in itertools.permutations(members, i):
            yield [member_pair[1]] + list(j) + [member_pair[0]]

def all_permutation_method_return_string(member_pair: typing.Tuple[int, int]) -> typing.Iterable[str]:
    members = list(itertools.filterfalse(lambda x: x in member_pair, range(1, MemberCount + 1)))
    for i in range(1, len(members) +1):
        for j in itertools.permutations(members, i):
            yield ','.join(map(str, [member_pair[1]] + list(j) + [member_pair[0]]))


def new_method(member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
    all_cycles = all_permutation_method(member_pair)
    not_covered_pairs = [list(x) for x in NotCoveredPairs]
    for cycle in all_cycles:
        found = True
        for not_covered_pair in not_covered_pairs:
            if any(not_covered_pair == cycle[i:i+2] for i in range(len(cycle) -1)):
                found = False
                break
        if found:
            yield cycle

def new_method2(member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
    all_cycles = all_permutation_method(member_pair)
    not_covered_pairs = [list(x) for x in NotCoveredPairs]
    for cycle in all_cycles:
        if not any(any(not_covered_pair == cycle[i:i+2] for i in range(len(cycle) -1)) for not_covered_pair in not_covered_pairs):
            yield cycle


if __name__ == "__main__":
    member_pairs = new_method((1,3))
    for member_pair in member_pairs:
        print(member_pair)
    # print(len(member_pairs))
    # print(len(new_method((1,3))))

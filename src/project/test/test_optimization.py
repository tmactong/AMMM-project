import typing
import itertools
from src.project.helpers.cycles_generator import generate_branches

MemberCount = 10
CoveredPairs = []

for i in range(1, MemberCount + 1):
    for j in range(1, MemberCount + 1):
        if i != j:
            CoveredPairs.append((i, j))


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


def new_method(member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
    members = list(itertools.filterfalse(lambda x: x in member_pair, range(1, MemberCount + 1)))
    for i in range(1, len(members) +1):
        for j in itertools.permutations(members, i):
            yield [member_pair[1]] + list(j) + [member_pair[0]]


if __name__ == "__main__":
    member_pairs = new_method((1,3))
    for member_pair in member_pairs:
        print(member_pair)
    #print(len(member_pairs))
    # print(len(new_method((1,3))))

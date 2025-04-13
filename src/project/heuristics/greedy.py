import typing
from src.project.heuristics import HeuristicMethod
from src.project.helpers.cycles_generator import generate_branches


class GreedyHeuristic(HeuristicMethod):

    CoveredPairs: typing.List[typing.Tuple[int, int]]

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]]):
        super().__init__(member_count, bids)
        self.CoveredPairs = []

    def update_covered_pairs(self, member_pair: typing.Tuple[int, int]) -> None:
        self.CoveredPairs.append(member_pair)
        self.CoveredPairs.append(member_pair[::-1])

    def update_candidates(self, member_pair: typing.Tuple[int, int], delete_reverse: bool = False) -> None:
        """
        candidates = list()
        for candidate in self.Candidates:
            if candidate != new_member_pair and candidate != new_member_pair[::-1]:
                for member_pair in self.Solution:
                    if set(member_pair) & set(candidate):
                        candidates.append(candidate)
        self.Candidates = candidates
        """
        self.Candidates.remove(member_pair)
        if delete_reverse and member_pair[::-1] in self.Candidates:
            self.Candidates.remove(member_pair[::-1])

    def _singleton_member_pair(self) -> (bool, typing.Tuple[int, int]):
        for pair in self.Candidates:
            if pair[::-1] not in self.Candidates:
                return True, pair
        return False, None

    def sort_candidates_by_quality(self) -> typing.List[typing.Tuple[int, int]]:
        singleton_pair_exists, singleton_pair = self._singleton_member_pair()
        if singleton_pair_exists:
            return [singleton_pair]
        else:
            return sorted(self.Candidates, key=lambda x: self.Bids[x[0]][x[1]], reverse=True)

    def _newly_constructed_cycle_members(self, member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
        # print('member_pair:', member_pair)
        # print('covered pairs:', self.CoveredPairs)
        for branch in generate_branches([member_pair[1]], self.CoveredPairs):
            if member_pair[0] in branch:
                yield branch[:branch.index(member_pair[0])+1]

    def _newly_constructed_cycles(self, member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
        uniq_cycles = list()
        for cycle_members in self._newly_constructed_cycle_members(member_pair):
            if cycle_members not in uniq_cycles:
                # print(cycle_members)
                uniq_cycles.append(cycle_members)
                yield cycle_members

    def validate_candidate(self, candidate: typing.Tuple[int, int]) -> bool:
        new_cycles = self._newly_constructed_cycles(candidate)
        for cycle in new_cycles:
            cycle_priority = 0
            for idx in range(len(cycle) - 1):
                cycle_priority += self.MemberPriorities[cycle[idx]][cycle[idx + 1]]
            if cycle_priority + 1 == len(cycle):
                return False
        return True

    def _solve(self) -> bool:
        while self.Candidates:
            sorted_candidates = self.sort_candidates_by_quality()
            candidate = sorted_candidates.pop(0)
            feasible = self.validate_candidate(candidate)
            if feasible:
                self.update_candidates(candidate, delete_reverse=True)
                print('candidates number:', len(self.Candidates))
                self.update_covered_pairs(candidate)
                self.Solution.append(candidate)
                self.MemberPriorities[candidate[0]][candidate[1]] = 1
                self.update_objective(candidate)
            else:
                print(candidate, 'is not feasible')
                if candidate[::-1] in self.Candidates:
                    self.update_candidates(candidate)
                else:
                    return False
        return True
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

    def update_candidates(self, member_pair: typing.Tuple[int, int]) -> None:
        self.Candidates.remove(member_pair)
        self.Candidates.remove(member_pair[::-1])

    def sort_candidates_by_quality(self) -> typing.List[typing.Tuple[int, int]]:
        return sorted(self.Candidates, key=lambda x: self.Bids[x[0]][x[1]], reverse=True)

    def _newly_constructed_cycles(self, member_pair: typing.Tuple[int, int]) -> typing.Iterable[typing.List[int]]:
        # print('member_pair:', member_pair)
        # print('covered pairs:', self.CoveredPairs)
        for branch in generate_branches([member_pair[1]], self.CoveredPairs):
            if member_pair[0] in branch:
                yield branch[:branch.index(member_pair[0])+1]

    def _uniq_newly_constructed_cycles(self, member_pair: typing.Tuple[int, int]) -> typing.List[typing.List[int]]:
        uniq_cycles = list()
        for cycle in self._newly_constructed_cycles(member_pair):
            if cycle not in uniq_cycles:
                # print('new cycle:', cycle)
                uniq_cycles.append(cycle)
        return uniq_cycles

    def validate_candidate(self, candidate: typing.Tuple[int, int]) -> bool:
        new_cycles = self._uniq_newly_constructed_cycles(candidate)
        for cycle in new_cycles:
            cycle_priority = 0
            for idx in range(len(cycle) - 1):
                cycle_priority += self.MemberPriorities[cycle[idx]][cycle[idx + 1]]
            if cycle_priority + 1 == len(cycle):
                return False
        return True

    def solve(self) -> None:
        while self.Candidates:
            sorted_candidates = self.sort_candidates_by_quality()
            candidate = sorted_candidates.pop(0)
            # print('candidate:', candidate)
            feasible = self.validate_candidate(candidate)
            self.update_candidates(candidate)
            print('candidates number:', len(self.Candidates))
            self.update_covered_pairs(candidate)
            if feasible:
                self.Solution.append(candidate)
                self.MemberPriorities[candidate[0]][candidate[1]] = 1
                self.update_objective(candidate)
            else:
                """
                We can safely add j->i to Solution if i->j is not feasible.
                """
                print(candidate, 'is not feasible')
                self.Solution.append(candidate[::-1])
                self.MemberPriorities[candidate[1]][candidate[0]] = 1
                self.update_objective(candidate[::-1])
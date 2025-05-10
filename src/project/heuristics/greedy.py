import typing
from collections.abc import Callable
from src.project.heuristics import HeuristicMethod
from src.project.helpers.graph import topological_sort

class GreedyHeuristic(HeuristicMethod):

    def update_candidates(self, member_pair: typing.Tuple[int, int]) -> None:
        self.Candidates.remove(member_pair)
        self.Candidates.remove(member_pair[::-1])

    def sort_candidates_by_quality(self) -> typing.List[typing.Tuple[int, int]]:
        return sorted(self.Candidates, key=lambda x: self.Bids[x[0]][x[1]], reverse=True)

    def pop_candidate_from_sorted(self) -> typing.Tuple[int, int]:
        sorted_candidates = self.sort_candidates_by_quality()
        return sorted_candidates.pop(0)

    def validate_candidate(self, candidate: typing.Tuple[int, int]) -> bool:
        _, residual_edges = topological_sort(self.Solution + [candidate])
        if residual_edges:
            return False
        return True

    def greedy_solve(self, pop_candidate_func: Callable[[], typing.Tuple[int, int]]) -> None:
        while self.Candidates:
            candidate = pop_candidate_func()
            feasible = self.validate_candidate(candidate)
            self.update_candidates(candidate)
            print('candidates number:', len(self.Candidates))
            self.CoveredMembers |= set(candidate)
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

    def solve(self) -> None:
        self.greedy_solve(self.pop_candidate_from_sorted)
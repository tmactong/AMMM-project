import typing
from collections.abc import Callable
from src.project.heuristics import HeuristicMethod
from src.project.helpers.graph import trim_graph


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
        #_, residual_edges = topological_sort(self.Solution + [candidate])
        residual_edges = trim_graph(self.Solution + [candidate])
        return len(residual_edges) == 0

    def greedy_solve(self, pop_candidate_func: Callable[[], typing.Tuple[int, int]]) -> None:
        while self.Candidates:
            i,j = pop_candidate_func()
            self.update_candidates((i, j))
            print('candidates number:', len(self.Candidates))
            feasible = self.validate_candidate((i,j))
            self.CoveredMembers |= {i, j}
            if feasible:
                self.Solution.append((i,j))
                self.MemberPriorities[i][j] = 1
                self.update_objective((i,j))
            else:
                """
                We can safely add j->i to Solution if i->j is not feasible.
                """
                print(f'{i}->{j} is not feasible')
                self.Solution.append((j,i))
                self.MemberPriorities[j][i] = 1
                self.update_objective((j,i))

    def solve(self) -> None:
        self.greedy_solve(self.pop_candidate_from_sorted)
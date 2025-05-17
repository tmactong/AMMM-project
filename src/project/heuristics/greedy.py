import typing
from collections.abc import Callable
from src.project.heuristics import HeuristicMethod
from src.project.helpers.graph import topological_sort


class GreedyHeuristic(HeuristicMethod):

    def update_candidates(self, member_pair: typing.Tuple[int, int]) -> None:
        self.Candidates.remove(member_pair)
        self.Candidates.remove(member_pair[::-1])

    def sort_candidates_by_quality(self) -> typing.List[typing.Tuple[int, int]]:
        return sorted(self.Candidates, key=lambda x: (self.Bids[x[0]][x[1]], self.Bids[x[1]][x[0]]), reverse=True)

    def pop_candidate_from_sorted(self) -> typing.Tuple[int, int]:
        sorted_candidates = self.sort_candidates_by_quality()
        self.SortedCandidates = sorted_candidates
        return sorted_candidates.pop(0)

    def validate_candidate(self, candidate: typing.Tuple[int, int]) -> bool:
        topological_order = topological_sort(self.CoveredMembers, self.Solution + [candidate])
        return len(topological_order) == len(self.CoveredMembers)

    def greedy_solve(self,
                     pop_candidate_func: Callable[[], typing.Tuple[int, int]],
                     method: str = 'greedy',
                     alpha: typing.Optional[float] = None
                     ) -> None:
        while self.Candidates:
            i,j = pop_candidate_func()
            self.update_candidates((i, j))
            self.CoveredMembers |= {i, j}
            print('candidates number:', len(self.Candidates))
            feasible = self.validate_candidate((i,j))
            if feasible:
                self.Solution.append((i,j))
                self.MemberPriorities[i][j] = 1
                self.update_objective((i,j))
            else:
                """
                We can safely add j->i to Solution if i->j is not feasible.
                """
                print(f'{i}->{j} is not feasible')
                if self.DrawGraph and method == 'greedy':
                    self.plot_graph('greedy', self.Solution + [(i,j)],
                                    skip_objective=True,rcl=[(i,j)] + self.SortedCandidates, selected_candidate=(i,j))
                    self.plot_graph('greedy', self.Solution + [(i, j)], draw_cycle=True,
                                    rcl=[(i,j)] + self.SortedCandidates, selected_candidate=(i,j))
                    self.plot_graph('greedy', self.Solution + [(i,j)], infeasible_edge=(i,j),
                                    rcl=[(i,j)] + self.SortedCandidates, selected_candidate=(i,j))
                if self.DrawGraph and method == 'grasp':
                    self.plot_graph(
                        'grasp', self.Solution + [(i,j)], infeasible_edge=(i,j), draw_cycle=True, alpha=alpha,
                        rcl=self.SortedCandidates, selected_candidate=(i,j)
                    )
                self.InfeasiblePairs.append((i, j))
                self.Solution.append((j,i))
                self.MemberPriorities[j][i] = 1
                self.update_objective((j,i))
            if self.DrawGraph and method == 'greedy':
                self.plot_graph(method,self.Solution,rcl=[(i,j)] + self.SortedCandidates, selected_candidate=(i,j))
            if self.DrawGraph and method == 'grasp':
                self.plot_graph(method,self.Solution, alpha=alpha, rcl=self.SortedCandidates, selected_candidate=(i,j))
        self.plot_graph(method, self.Solution)

    def solve(self) -> None:
        self.greedy_solve(self.pop_candidate_from_sorted)
import time
import random
import typing
from src.project.heuristics.local_search import LocalSearch
from src.project.helpers.dump_solution import dump_solution

class Grasp(LocalSearch):

    Alpha: float
    MaxRetryTimes: int = 10

    def __init__(
            self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]], project_name: str, alpha: float = 0
    ) -> None:
        super().__init__(member_count, bids, project_name)
        self.Alpha = alpha

    def pop_random_candidate_from_rcl(self) -> typing.Tuple[int, int]:
        sorted_candidates = self.sort_candidates_by_quality()
        max_bid = self.Bids[sorted_candidates[0][0]][sorted_candidates[0][1]]
        min_bid = self.Bids[sorted_candidates[-1][0]][sorted_candidates[-1][1]]
        rcl = [x for x in sorted_candidates if self.Bids[x[0]][x[1]] >= max_bid - self.Alpha * (max_bid - min_bid)]
        return random.choice(rcl)

    def solve(self) -> None:
        best_objective, best_solution, best_priorities = 0, [], dict()
        for retry in range(1, self.MaxRetryTimes+1):
            print(f"Retry: {retry}")
            start_time = int(time.time())
            self.initialize_variables()
            """ Greedy Construction Phase"""
            print(f'{"*"*20} Greedy Construction Phase {"*"*20}')
            self.greedy_solve(self.pop_random_candidate_from_rcl)
            print(f"Greedy Objective: {self.Objective}")
            """ Local Search Phase """
            print(f'{"*"*20} Local Search Phase {"*"*20}')
            super().solve()
            print(f"Local Search Objective: {self.Objective}")
            dump_solution(
                'grasp', self.ProjectName, start_time, self.Objective, self.Solution,
                self.MemberPriorities, self.Bids, alpha=self.Alpha, retry=retry)
            if self.Objective > best_objective:
                best_objective = self.Objective
                best_solution = self.Solution
                best_priorities = self.MemberPriorities
            print(f'Retry {retry} finished')
        self.Solution = best_solution
        self.Objective = best_objective
        self.MemberPriorities = best_priorities
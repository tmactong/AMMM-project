import random
import typing
from src.project.heuristics.local_search import LocalSearch

class Grasp(LocalSearch):

    Alpha: float

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]], alpha: float = 0) -> None:
        super().__init__(member_count, bids)
        self.Alpha = alpha

    def pop_random_candidate_from_rcl(self) -> typing.Tuple[int, int]:
        sorted_candidates = self.sort_candidates_by_quality()
        max_bid = self.Bids[sorted_candidates[0][0]][sorted_candidates[0][1]]
        min_bid = self.Bids[sorted_candidates[-1][0]][sorted_candidates[-1][1]]
        rcl = [x for x in sorted_candidates if self.Bids[x[0]][x[1]] >= max_bid - self.Alpha * (max_bid - min_bid)]
        return random.choice(rcl)

    def solve(self) -> None:
        """ Greedy Construction Phase"""
        print(f'{"="*20} Greedy Construction Phase {"="*20}')
        self.greedy_solve(self.pop_random_candidate_from_rcl)
        """Local Search Phase"""
        print(f'{"="*20} Local Search Phase {"="*20}')
        super().solve()
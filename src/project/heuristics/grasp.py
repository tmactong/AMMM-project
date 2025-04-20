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
        while self.Candidates:
            candidate = self.pop_random_candidate_from_rcl()
            print(f"bid: {self.Bids[candidate[0]][candidate[1]]}")
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
        """Local Search Phase"""
        print(f'{"="*20} Local Search Phase {"="*20}')
        super().solve()
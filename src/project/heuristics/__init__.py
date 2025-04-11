import typing
import itertools


class HeuristicMethod:

    Candidates: typing.List[typing.Tuple[int, int]]
    Solution: typing.List[typing.Tuple[int, int]]
    Objective: int

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int]]) -> None:
        self.member_count = member_count
        self.bids = bids
        self.initialize_candidates()
        self.Solution = list()
        self.Objective = 0

    def initialize_candidates(self) -> None:
        """
        Example:
            [1,2,3] -> [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
        """
        self.Candidates = list(itertools.permutations(range(1, self.member_count+1), 2))

    def update_candidates(self, combination: typing.Tuple[int, ...]) -> None:
        raise NotImplementedError("Method update_candidates not implemented")

    def solve(self) -> None:
        raise NotImplementedError("Method solve not implemented")
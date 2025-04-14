import typing
import itertools


class HeuristicMethod:

    MemberCount: int
    Bids: typing.Dict[int, typing.Dict[int, int]]
    Candidates: typing.List[typing.Tuple[int, int]]
    Solution: typing.List[typing.Tuple[int, int]]
    MemberPriorities: typing.Dict[typing.Any, typing.Dict[typing.Any, int]]
    Objective: int

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]]) -> None:
        self.MemberCount = member_count
        self.Bids = bids
        self.initialize_candidates()
        self.Solution = list()
        self.MemberPriorities = dict(
            map(lambda _: (
                _, dict(map(lambda _: (_, 0), range(1,member_count+1)))
            ), range(1,member_count+1)))
        self.Objective = 0

    def initialize_candidates(self) -> None:
        """
        Example:
            [1,2,3] -> [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
        """
        self.Candidates = list(itertools.permutations(range(1, self.MemberCount + 1), 2))

    def update_objective(self, pair: typing.Tuple[int, int]) -> None:
        self.Objective += self.Bids[pair[0]][pair[1]]

    def solve(self) -> None:
        raise NotImplementedError("Method solve not implemented")
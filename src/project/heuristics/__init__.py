import typing
import itertools


class HeuristicMethod:

    MemberCount: int
    Bids: typing.Dict[int, typing.Dict[int, int]]
    Candidates: typing.List[typing.Tuple[int, int]]
    Solution: typing.List[typing.Tuple[int, int]]
    MemberPriorities: typing.Dict[typing.Any, typing.Dict[typing.Any, int]]
    Objective: int
    CoveredMembers: typing.Set[int]

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]], project_name: str,) -> None:
        self.MemberCount = member_count
        self.Bids = bids
        self.ProjectName = project_name
        self.initialize_variables()

    def initialize_variables(self) -> None:
        self.Solution = list()
        self.MemberPriorities = dict(
            map(lambda _: (
                _, dict(map(lambda _: (_, 0), range(1, self.MemberCount + 1)))
            ), range(1, self.MemberCount + 1)))
        self.Objective = 0
        self.Candidates = [(i,j) for i,j in itertools.permutations(range(1, self.MemberCount + 1), 2)
                           if self.Bids[i][j] != 0 or self.Bids[j][i] != 0]
        self.CoveredMembers = set()

    def update_objective(self, pair: typing.Tuple[int, int]) -> None:
        self.Objective += self.Bids[pair[0]][pair[1]]

    def solve(self) -> None:
        raise NotImplementedError("Method solve not implemented")
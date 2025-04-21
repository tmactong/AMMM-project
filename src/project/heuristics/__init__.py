import typing
import json
import itertools


class HeuristicMethod:

    MemberCount: int
    Bids: typing.Dict[int, typing.Dict[int, int]]
    Candidates: typing.List[typing.Tuple[int, int]]
    Solution: typing.List[typing.Tuple[int, int]]
    MemberPriorities: typing.Dict[typing.Any, typing.Dict[typing.Any, int]]
    Objective: int
    CoveredPairs: typing.List[typing.Tuple[int, int]]

    def __init__(self, member_count: int, bids: typing.Dict[int, typing.Dict[int, int]], project_name: str,
                 solution_file: typing.Optional[str] = None) -> None:
        self.MemberCount = member_count
        self.Bids = bids
        self.ProjectName = project_name
        self.initialize_variables()
        self.solution_file = solution_file
        if self.solution_file:
            print('import solution from file:', self.solution_file)
            self.load_solution_file()

    def load_solution_file(self):
        with open(self.solution_file, 'r') as f:
            greedy_result = json.load(f)
            solution = greedy_result['Solution']
            self.Solution = [tuple(x) for x in solution]
            member_priorities = greedy_result['MemberPriorities']
            for i in member_priorities:
                for j in member_priorities[i]:
                    self.MemberPriorities[int(i)][int(j)] = member_priorities[i][j]
            self.Objective = greedy_result['Objective']
            for i in range(1, self.MemberCount+1):
                for j in range(1, self.MemberCount+1):
                    if i != j:
                        self.CoveredPairs.append((i, j))

    def initialize_variables(self) -> None:
        self.Solution = list()
        self.MemberPriorities = dict(
            map(lambda _: (
                _, dict(map(lambda _: (_, 0), range(1, self.MemberCount + 1)))
            ), range(1, self.MemberCount + 1)))
        self.Objective = 0
        self.CoveredPairs = []
        self.initialize_candidates()

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
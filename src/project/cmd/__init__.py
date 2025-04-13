import typing
from src.project.helpers.data_parser import parse as data_parser
from src.project.heuristics import HeuristicMethod
from src.project.heuristics.grasp import Grasp
from src.project.heuristics.greedy import GreedyHeuristic
from src.project.heuristics.local_search import LocalSearch


class Algorithm:
    GREEDY = 'greedy'
    LOCAL_SEARCH = 'local_search'
    GRASP = 'grasp'

ALGORITHM = typing.Literal[Algorithm.GREEDY, Algorithm.LOCAL_SEARCH, Algorithm.GRASP]


class Solver:

    MemberCount: int
    Bids: typing.Dict[int, typing.Dict[int, int]]
    SolverInstance: HeuristicMethod
    Algorithm: ALGORITHM

    def __init__(self, data_file: str, algorithm: ALGORITHM) -> None:
        self.data_file = data_file
        self.MemberCount, self.Bids = data_parser(self.data_file)
        self.Algorithm = algorithm

    def __enter__(self) -> HeuristicMethod:
        if self.Algorithm == Algorithm.GREEDY:
            self.SolverInstance = GreedyHeuristic(self.MemberCount, self.Bids)
        elif self.Algorithm == Algorithm.LOCAL_SEARCH:
            self.SolverInstance = LocalSearch(self.MemberCount, self.Bids)
        elif self.Algorithm == Algorithm.GRASP:
            self.SolverInstance = Grasp(self.MemberCount, self.Bids)
        else:
            raise NotImplementedError
        return self.SolverInstance

    def __exit__(self, *args) -> None:
        if self.SolverInstance.Solved:
            print('Found feasible solution')
            for s in sorted(self.SolverInstance.Solution, key=lambda x: x[0]):
                if self.Bids[s[0]][s[1]] > 0:
                    print(s[0], '->', s[1])
            print('Objective:', self.SolverInstance.Objective)
        else:
            print('No feasible solution')
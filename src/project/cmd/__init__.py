import typing
import time
import os
from src.project.helpers.data_parser import parse as data_parser
from src.project.helpers.dump_solution import dump_solution
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
    start_time: int

    def __init__(self, data_file: str, algorithm: ALGORITHM,
                 alpha: typing.Optional[float] = None, do_local_search: typing.Optional[bool] = None,
                 max_iteration: typing.Optional[int] = None
                 ) -> None:
        self.data_file = data_file
        self.MemberCount, self.Bids = data_parser(self.data_file)
        self.Algorithm = algorithm
        self.Alpha = alpha
        self.DoLocalSearch = do_local_search
        self.MaxIteration = max_iteration
        self.start_time = round(time.time()*1000)
        self.ProjectName = os.path.basename(data_file).lstrip('project.').rstrip('.dat')

    def __enter__(self) -> HeuristicMethod:
        if self.Algorithm in [Algorithm.LOCAL_SEARCH, Algorithm.GREEDY] and self.Alpha:
            print(f"can't set alpha for algorithm {self.Algorithm}, ignoring alpha")
        if self.Algorithm == Algorithm.GREEDY:
            self.SolverInstance = GreedyHeuristic(self.MemberCount, self.Bids, self.ProjectName)
        elif self.Algorithm == Algorithm.LOCAL_SEARCH:
            self.SolverInstance = LocalSearch(self.MemberCount, self.Bids, self.ProjectName)
        elif self.Algorithm == Algorithm.GRASP:
            self.SolverInstance = Grasp(
                self.MemberCount, self.Bids, self.ProjectName, alpha=self.Alpha,
                do_local_search=self.DoLocalSearch, max_iteration=self.MaxIteration)
        else:
            raise NotImplementedError
        return self.SolverInstance

    def __exit__(self, *args) -> None:
        print('Solution:')
        for s in sorted(self.SolverInstance.Solution):
            print(s[0], '->', s[1])
        print('Objective:', self.SolverInstance.Objective)
        dump_solution(
            self.Algorithm, self.ProjectName, self.start_time,
            self.SolverInstance.Objective, self.SolverInstance.Solution,
            self.SolverInstance.MemberPriorities, self.Bids, alpha=self.Alpha
        )


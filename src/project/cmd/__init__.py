import typing
import json
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

    def __init__(self, data_file: str, algorithm: ALGORITHM, solution_file: typing.Optional[str] = None, alpha: float = 0) -> None:
        self.data_file = data_file
        self.MemberCount, self.Bids = data_parser(self.data_file)
        self.Algorithm = algorithm
        self.solution_file = solution_file
        self.Alpha = alpha

    def __enter__(self) -> HeuristicMethod:
        if self.Algorithm in [Algorithm.GREEDY, Algorithm.GRASP] and self.solution_file:
            print(f"can't load greedy solution for algorithm {self.Algorithm}, ignoring solution file")
        if self.Algorithm in [Algorithm.LOCAL_SEARCH, Algorithm.GREEDY] and self.Alpha:
            print(f"can't set alpha for algorithm {self.Algorithm}, ignoring alpha")
        if self.Algorithm == Algorithm.GREEDY:
            self.SolverInstance = GreedyHeuristic(self.MemberCount, self.Bids)
        elif self.Algorithm == Algorithm.LOCAL_SEARCH:
            self.SolverInstance = LocalSearch(self.MemberCount, self.Bids, solution_file=self.solution_file)
        elif self.Algorithm == Algorithm.GRASP:
            self.SolverInstance = Grasp(self.MemberCount, self.Bids, alpha=self.Alpha)
        else:
            raise NotImplementedError
        return self.SolverInstance

    def __exit__(self, *args) -> None:
        print('Solution:')
        for s in sorted(self.SolverInstance.Solution):
            if self.Bids[s[0]][s[1]] > 0:
                print(s[0], '->', s[1])
        print('Objective:', self.SolverInstance.Objective)
        with open(f"../result/{self.Algorithm}/solution.json", "w") as file:
            file.write(
                json.dumps(
                    {
                        'Objective': self.SolverInstance.Objective,
                        'Solution': self.SolverInstance.Solution,
                        'MemberPriorities': self.SolverInstance.MemberPriorities,
                        'Bids': self.Bids
                    },
                    indent=4
                )
            )


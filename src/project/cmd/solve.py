import typing
from src.project.helpers.data_parser import parse as data_parser
from src.project.heuristics import HeuristicMethod
from src.project.heuristics.greedy import GreedyHeuristic


class Solver:

    MemberCount: int
    Bids: typing.Dict[int, typing.Dict[int, int]]
    SolverInstance: HeuristicMethod

    def __init__(self, data_file: str) -> None:
        self.data_file = data_file
        self.MemberCount, self.Bids = data_parser(self.data_file)

    def __enter__(self) -> HeuristicMethod:
        self.SolverInstance = GreedyHeuristic(self.MemberCount, self.Bids)
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


def main(data_file) -> None:
    with Solver(data_file) as solver_instance:
        solver_instance.solve()


if __name__ == '__main__':
    # project 6: 8 members
    # main('../testdata/project.6.dat')
    # project 2: 6 members
    main('../testdata/project.2.dat')
    # project 3: 10 members
    # main('../testdata/project.3.dat')
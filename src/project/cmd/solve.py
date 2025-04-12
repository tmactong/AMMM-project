import typing
from src.project.helpers.data_parser import parse as data_parser
from src.project.heuristics import HeuristicMethod
from src.project.heuristics.greedy import GreedyHeuristic


class Solver:
    MemberCount: int
    Bids: typing.Dict[int, typing.Dict[int, int]]

    def __init__(self, data_file: str) -> None:
        self.data_file = data_file
        self.MemberCount, self.Bids = data_parser(self.data_file)

    def __enter__(self) -> HeuristicMethod:
        return GreedyHeuristic(self.MemberCount, self.Bids)

    def __exit__(self) -> None:
        pass


def main(data_file) -> None:
    member_count, bids = data_parser(data_file)
    solver = GreedyHeuristic(member_count, bids)
    if solver.solve():
        print('Found feasible solution')
        # print(solver.Solution)
        for s in sorted(solver.Solution, key=lambda x:x[0]):
            if bids[s[0]][s[1]] > 0:
                print(s[0], '->', s[1])
        print('Objective:', solver.Objective)
    else:
        print('No feasible solution')


if __name__ == '__main__':
    main('../testdata/project.6.dat')
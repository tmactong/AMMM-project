import typing
from src.project.cmd import Solver, ALGORITHM


def main(data_file: str, algorithm: ALGORITHM, solution_file: typing.Optional[str] = None, alpha: float = 0) -> None:
    with Solver(data_file, algorithm, solution_file, alpha) as solver_instance:
        solver_instance.solve()


if __name__ == '__main__':
    # main('../testdata/project.1.dat', 'local_search')
    # project 6: 8 members
    # main('../testdata/project.6.dat', 'greedy')
    # project 2: 6 members
    # main('../testdata/project.2.dat', 'greedy')
    # main('../testdata/project.2.dat', 'local_search')
    main('../testdata/project.2.dat', 'grasp', alpha=0.9)
    # project 3: 10 members
    # main('../testdata/project.3.dat', 'greedy')
    # project 4: 10 members
    # main('../testdata/project.4.dat', 'greedy')
    # main('../testdata/project.4.dat', 'local_search', '../result/greedy/project.4.json')
    # main('../testdata/project.4.dat', 'grasp', alpha=0.5)
    # main('../testdata/project.4.dat', 'local_search', '../result/greedy/project.4.ls_1st.json')
    # test infeasible solution
    # main('../testdata/infeasible_solution.dat', 'greedy')
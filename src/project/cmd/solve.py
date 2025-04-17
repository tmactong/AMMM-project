from src.project.cmd import Solver, ALGORITHM


def main(data_file: str, algorithm: ALGORITHM) -> None:
    with Solver(data_file, algorithm) as solver_instance:
        solver_instance.solve()


if __name__ == '__main__':
    # main('../testdata/project.1.dat', 'local_search')
    # project 6: 8 members
    # main('../testdata/project.6.dat', 'greedy')
    # project 2: 6 members
    # main('../testdata/project.2.dat', 'greedy')
    # project 3: 10 members
    # main('../testdata/project.3.dat', 'greedy')
    # project 4: 10 members
    main('../testdata/project.4.dat', 'local_search')
    # test infeasible solution
    # main('../testdata/infeasible_solution.dat', 'greedy')
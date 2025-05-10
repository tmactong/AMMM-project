from src.project.cmd import Solver, ALGORITHM


def main(data_file: str, algorithm: ALGORITHM, alpha: float = 0) -> None:
    with Solver(data_file, algorithm, alpha) as solver_instance:
        solver_instance.solve()


if __name__ == '__main__':
    # main('../testdata/project.8.dat', 'local_search')
    # project 6: 8 members
    main('../testdata/project.45members.dat', 'local_search')
    # project 2: 6 members
    # main('../testdata/project.8.dat', 'greedy')
    # main('../testdata/project.2.dat', 'local_search')
    # main('../testdata/project.2.dat', 'grasp', alpha=0.9)
    # project 3: 10 members
    #for alpha in (0.1, 0.3, 0.5, 0.7, 0.9):
    #    main('../testdata/project.7.dat', 'grasp', alpha=alpha)
    # project 4: 10 members
    # main('../testdata/project.4.dat', 'greedy')
    # main('../testdata/project.4.dat', 'local_search')
    # main('../testdata/project.4.dat', 'local_search', '../result/project.4/grasp/alpha=0.5/solution.grasp.try=1.objective=154.json')
    # main('../testdata/project.4.dat', 'grasp', alpha=0.9)
    # test infeasible solution
    # main('../testdata/infeasible_solution.dat', 'greedy')
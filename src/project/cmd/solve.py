import argparse
from src.project.cmd import Solver, Algorithm, ALGORITHM

def alpha_type(alpha_value):
    alpha_values = []
    alphas = alpha_value.split(',')
    for alpha in alphas:
        try:
            alpha = float(alpha)
        except ValueError:
            raise argparse.ArgumentTypeError("alpha must be a float")
        if alpha < 0 or alpha > 1:
            raise argparse.ArgumentTypeError("alpha must be a float between 0 and 1")
        alpha_values.append(alpha)
    return alpha_values

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='solve.py',
        description='Solve conflict resolution problem by Heuristics method'
    )
    parser.add_argument('data_file', help='problem data file')
    parser.add_argument(
        '-m', '--method', choices=['greedy', 'local_search', 'grasp'],
        help='heuristics method to solve problem', required=True)
    parser.add_argument('--alpha', type=alpha_type, help='alpha parameter for GRASP method')
    parser.add_argument('--do_local_search', action='store_true', help='do local search or not for GRASP')
    return parser

def run_main(data_file: str, algorithm: ALGORITHM, alpha: float = 0, local_search: bool = False) -> None:
    with Solver(data_file, algorithm, alpha, local_search) as solver_instance:
        solver_instance.solve()

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.method == 'greedy':
        run_main(data_file=args.data_file, algorithm=Algorithm.GREEDY)
    elif args.method == 'local_search':
        run_main(data_file=args.data_file, algorithm=Algorithm.LOCAL_SEARCH)
    elif args.method == 'grasp':
        if not args.alpha:
            raise argparse.ArgumentTypeError("alpha must be specified when using GRASP")
        for alpha in args.alpha:
            run_main(
                data_file=args.data_file, algorithm=Algorithm.GRASP, alpha=alpha, local_search=args.do_local_search)
    else:
        raise argparse.ArgumentTypeError("invalid method '{}'".format(args.method))


if __name__ == '__main__':
    main()
    # args = parser.parse_args()
    #main('../testdata/project.8.dat', 'local_search')
    # project 6: 8 members
    #for i in range(1, 11):
    #    for alpha in (0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1):
    #        main(f'../testdata/project.45-{i}.dat', 'grasp', alpha, local_search=False)
    #run_main('../testdata/project.45members.dat', 'local_search')
    # project 2: 6 members
    # project 3: 10 members
    #for alpha in (0.1, 0.3, 0.5, 0.7, 0.9):
    #    main('../testdata/project.45members.dat', 'grasp', alpha=alpha)
import argparse
from src.project.cmd import Solver, ALGORITHM, Algorithm
import typing as t

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
    parser.add_argument('--max_iteration', type=int, default=10, help='max iteration for GRASP')
    parser.add_argument('--draw', action='store_true', help='draw solution using matplotlib')
    return parser

def run_main(data_file: str, algorithm: ALGORITHM, alpha: float = 0,
             local_search: bool = False, draw: bool = False, max_iteration: t.Optional[int] = None) -> None:
    with Solver(data_file, algorithm, alpha, local_search, draw_graph=draw, max_iteration=max_iteration) as solver_instance:
        solver_instance.solve()

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.method == Algorithm.GREEDY:
        run_main(data_file=args.data_file, algorithm=Algorithm.GREEDY, draw=args.draw)
    elif args.method == Algorithm.LOCAL_SEARCH:
        run_main(data_file=args.data_file, algorithm=Algorithm.LOCAL_SEARCH, draw=args.draw)
    elif args.method == Algorithm.GRASP:
        if not args.alpha:
            raise argparse.ArgumentTypeError("alpha must be specified when using GRASP")
        for alpha in args.alpha:
            run_main(
                data_file=args.data_file, algorithm=Algorithm.GRASP, alpha=alpha,
                local_search=args.do_local_search, draw=args.draw,max_iteration=args.max_iteration)
    else:
        raise argparse.ArgumentTypeError("invalid method '{}'".format(args.method))


if __name__ == '__main__':
    main()
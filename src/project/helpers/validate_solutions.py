import os
import json
from src.project.helpers.graph import trim_graph


def validate_solution(solution_file: str) -> None:
    print(f"Validating {solution_file}")
    with open(solution_file, "r") as file:
        solution = json.load(file)
        Solution = [(x[0], x[1]) for x in solution["Solution"]]
        member_count = int(sorted(map(int, solution['MemberPriorities'].keys()))[-1])
        #_, residual = topological_sort(Solution)
        residual, _, _ = trim_graph(Solution)
        if residual:
            print('INFEASIBLE')
        else:
            print('FEASIBLE')



if __name__ == "__main__":

    path = "../result/project.45-10"
    for file in os.listdir(path):
        if file.startswith('solution'):
            print(f'validate solution file {file}')
            validate_solution(os.path.join(path, file))
            print(f'{"#"*30}')

    # validate_solution(solution_file="../result/project.45-9/solution.local_search.objective=4870.json")
    # validate_solution("generated_solution.json")
    # print(generate_all_cycles(5))
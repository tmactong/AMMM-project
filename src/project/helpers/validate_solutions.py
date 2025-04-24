import json
import typing
import os
from src.project.helpers.cycles_generator import generate_cycle_patterns, get_combinations

def generate_all_cycles(total_member_count: int) -> typing.Dict[int, typing.List[typing.List[int]]]:
    all_cycles = dict(map(lambda _: (_, []), range(3, total_member_count + 1)))
    for member_count in range(3, total_member_count + 1):
        cycles = list(generate_cycle_patterns(list(range(1, member_count + 1))))
        combinations = get_combinations(total_member_count, member_count)
        for combination in combinations:
            for cycle in cycles:
                cycle_members = []
                for i in cycle:
                    cycle_members.append(combination[i-1])
                cycle_members.append(combination[0])
                all_cycles[member_count].append(cycle_members)
    return all_cycles


def validate_solution(solution_file: str) -> None:
    with open(solution_file, "r") as file:
        feasible = True
        solution = json.load(file)
        _ = solution["MemberPriorities"]
        member_count = int(sorted(map(int,_.keys()))[-1])
        member_priorities = dict(
            map(lambda _: (_, dict(map(lambda _: (_, 0), range(1,member_count+1)))), range(1,member_count+1)))
        for i in _:
            for j in _[i]:
                member_priorities[int(i)][int(j)] = _[i][j]
        all_cycles = generate_all_cycles(member_count)
        print(f"{sum([len(x) for x in all_cycles.values()])} cycles generated")
        for length, cycles in all_cycles.items():
            infeasible_cycles = 0
            for cycle in cycles:
                priority_sum = 0
                for i in range(len(cycle)-1):
                    priority_sum += member_priorities[cycle[i]][cycle[i+1]]
                try:
                    assert(priority_sum != length)
                    assert(priority_sum != 0)
                except AssertionError:
                    print(cycle, priority_sum)
                    feasible = False
                    infeasible_cycles += 1
            if not infeasible_cycles:
                print(f"member count {length}: all {len(cycles)} cycles PASSED")
            else:
                print(f"member count {length}: {infeasible_cycles} of {len(cycles)} cycles NOT PASSED")
    if feasible:
        print("Feasible Solution")
    else:
        print("Infeasible Solution")


if __name__ == "__main__":
    path = "../result/project.5/grasp/alpha=0.1"
    for file in os.listdir(path):
        if file.startswith('solution'):
            print(f'validate solution file {file}')
            validate_solution(os.path.join(path, file))
            print(f'{"#"*30}')
    # validate_solution(solution_file="../result/project.4/grasp/alpha=0.5/solution.grasp.try=4.objective=159.json")
    # validate_solution("../result/project.4/solution.greedy.objective=152.json")
    # print(generate_all_cycles(5))
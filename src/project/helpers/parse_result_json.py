import os
import re
import json
import typing as t

SolutionFolder = '../result/'


def get_time_and_objective(method: str):
    times = []
    objectives = []
    for i in range(1,11):
        folder = f'{SolutionFolder}/project.45-{i}'
        files = os.listdir(folder)
        for file in files:
            if file.startswith(f'solution.{method}'):
                solution_json = json.load(open(os.path.join(folder, file)))
                objective = solution_json['Objective']
                solving_time = (solution_json['EndTime'] - solution_json['StartTime']) / 1000
                times.append(solving_time)
                objectives.append(objective)
    for idx, solving_time in enumerate(times):
        print(f'{idx+1}\t{solving_time}')
    print('\n')
    for idx, objective in enumerate(objectives):
        print(f'{idx+1}\t{objective}')

def get_grasp_time_and_objective():
    times = [[] for _ in range(10)]
    objectives = []
    for i in range(1,11):
        folder = f'{SolutionFolder}/project.45-{i}/grasp/alpha=0.0'
        files = os.listdir(folder)
        for file in files:
            if file.startswith(f'solution.grasp.try='):
                solution_json = json.load(open(os.path.join(folder, file)))
                solving_time = (solution_json['EndTime'] - solution_json['StartTime']) / 1000
                times[i-1].append(solving_time)
    for idx, solving_times in enumerate(times):
        print(f'{idx+1}\t{sum(solving_times)}')
    for i in range(1,11):
        best_objective = 0
        folder = f'{SolutionFolder}/project.45-{i}'
        for file in os.listdir(folder):
            if file.startswith(f'solution.grasp.alpha='):
                objective = json.load(open(os.path.join(folder, file)))['Objective']
                if objective > best_objective:
                    best_objective = objective
        objectives.append(best_objective)
    for idx, objective in enumerate(objectives):
        print(f'{idx+1}\t{objective}')


def grasp_alpha_objecitve():
    r = re.compile(r"solution.grasp.alpha=(\d{1}.\d{1}).objective=(\d+).json")
    objectives = {x:{} for x in range(1,11)}
    for i in range(1, 11):
        folder = f'{SolutionFolder}/project.45-{i}'
        files = os.listdir(folder)
        for file in files:
            if file.startswith(f'solution.grasp.alpha='):
                searched = r.search(file)
                objectives[i][searched.group(1)] = searched.group(2)
    for i in range(1,11):
        print(f'project.45-{i}')
        print('id\tobjective')
        for alpha in ['0.0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']:
            print(f'{alpha}\t{objectives[i][alpha]}')
        print('max:', max(objectives[i].values()))
        print('\n')

def main(method: t.Literal['greedy', 'local_search', 'grasp']):
    if method in ['greedy', 'local_search']:
        get_time_and_objective(method)
    elif method == 'grasp':
        get_grasp_time_and_objective()

if __name__ == "__main__":
    main('local_search')
    #grasp_alpha_objecitve()
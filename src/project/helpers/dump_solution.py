import os
import json
import time
import typing

def dump_solution(
        algorithm:str, project_name: str, start_time: int, objective: int,
        solution: typing.List[typing.Tuple[int, int]], member_priorities: typing.Dict[typing.Any, typing.Dict[typing.Any, int]],
        bids: typing.Dict[int, typing.Dict[int, int]], alpha: typing.Optional[float] = None, retry: typing.Optional[int] = None,
        local_search: typing.Optional[bool] = None
):
    if algorithm == 'grasp':
        if retry is not None:
            dirname = f"../result/project.{project_name}/grasp/alpha={alpha}"
            filename = f"solution.{algorithm}.try={retry}{'.local_search' if local_search else ''}.objective={objective}.json"
        else:
            dirname = f"../result/project.{project_name}"
            filename = f"solution.{algorithm}.alpha={alpha}{'.local_search' if local_search else ''}.objective={objective}.json"
    else:
        dirname = f"../result/project.{project_name}"
        filename = f"solution.{algorithm}.objective={objective}.json"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(f"{dirname}/{filename}", "w") as file:
        file.write(
            json.dumps(
                {
                    'Objective': objective,
                    'Solution': solution,
                    'MemberPriorities': member_priorities,
                    'Bids': bids,
                    'StartTime': start_time,
                    'EndTime': round(time.time()*1000)
                },
                indent=4
            )
        )
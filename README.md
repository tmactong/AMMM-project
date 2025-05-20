# AMMM Final Project: Conflict Resolution Problem

### Members
- [Xin Tong](mailto:xin.tong@estudiantat.upc.edu)
- [Qiuchi Chen](mailto:qiuchi.chen@estudiantat.upc.edu)


### Prerequisite

Install `matplotlib`, `networkx`, `pillow`
```shell
pip install -r requirements.txt
```

### Directed Graph Drawing
[**solve.py**](src/project/cmd/solve.py)
```console
% python solve.py --help
usage: solve.py [-h] -m {greedy,local_search,grasp} [--alpha ALPHA] [--do_local_search] [--max_iteration MAX_ITERATION] [--draw] data_file

Solve conflict resolution problem by Heuristics method

positional arguments:
  data_file             problem data file

options:
  -h, --help            show this help message and exit
  -m {greedy,local_search,grasp}, --method {greedy,local_search,grasp}
                        heuristics method to solve problem
  --alpha ALPHA         alpha parameter for GRASP method
  --do_local_search     do local search or not for GRASP
  --max_iteration MAX_ITERATION
                        max iteration for GRASP
  --draw                draw solution using matplotlib
```
For example:
1. Solve [project.45-4.dat](src/project/testdata/project.45-4.dat) using Greedy method.
```shell
python solve.py ../testdata/project.45-4.dat --method greedy --draw
```
2. Solve [project.45-4.dat](src/project/testdata/project.45-4.dat) using Local Search method.
```shell
python solve.py ../testdata/project.45-4.dat --method local_search --draw
```
3. Solve [project.45-4.dat](src/project/testdata/project.45-4.dat) using GRASP method with 1 iteration, setting alpha to 0.2, while enabling the local search phase.
```shell
python solve.py ../testdata/project.45-4.dat --method grasp --max_iteration 1 --alpha 0.2 --do_local_search --draw
```
4. Solve [project.45-4.dat](src/project/testdata/project.45-4.dat) using GRASP method with 1 iterations, setting alpha to 0.2, while not enabling local search phase.
```shell
python solve.py ../testdata/project.45-4.dat --method grasp --max_iteration 1 --alpha 0.2 --draw
```
When you execute the commands above, image files will be generated in the folder labeled [project.4](src/project/assets/image/solution/project.4).

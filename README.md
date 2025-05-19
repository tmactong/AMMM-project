# AMMM Final Project: Conflict Resolution Problem

### Members
- [Xin Tong](mailto:xin.tong@estudiantat.upc.edu)
- [Qiuchi Chen](mailto:qiuchi.chen@estudiantat.upc.edu)


### Main structure of the code
- **[cmd](src/project/cmd) folder**: Contains the main executable program responsible for solving the problem and generating problem instances.
- **[heuristics](src/project/heuristics) folder**: Includes Python implementations of Greedy, Local Search, and GRASP methods.
- **[opl](src/project/opl) folder**: Contains the OPL code for the Integer Linear Programming (ILP) model.
- **[helpers](src/project/helpers) folder**: Comprises useful tools and libraries, including solution validator, graph processor, and more.
- **[result](src/project/result) folder**: Stores solutions in JSON format.
- **[testdata](src/project/testdata) folder**: Houses generated problem instances.

### Instance Generator
[**generate_data.py**](src/project/cmd/generate_data.py)
```shell
python generate_data.py <dataset_count> <member_count>
```
For example: I would like to generate 10 data files with 20 members.
```shell
python generate_data.py 10 20
```
The generated data files can be found in folder [testdata](src/project/testdata) with prefix `project.20-`

### Solving Conflict Problem
[**solve.py**](src/project/cmd/solve.py)
```console
% python solve.py --help
usage: solve.py [-h] -m {greedy,local_search,grasp} [--alpha ALPHA] [--do_local_search] [--max_iteration MAX_ITERATION] data_file

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
```
For example:
1. Solve [project.45-1.dat](src/project/testdata/project.45-1.dat) using Greedy method.
```shell
python solve.py ../testdata/project.45-1.dat --method greedy
```
2. Solve [project.45-1.dat](src/project/testdata/project.45-1.dat) using Local Search method.
```shell
python solve.py ../testdata/project.45-1.dat --method local_search
```
3. Solve [project.45-1.dat](src/project/testdata/project.45-1.dat) using GRASP method with 10 iterations, setting alpha to 0.1, 0.2, and 0.3, while enabling the local search phase.
```shell
python solve.py ../testdata/project.45-1.dat --method grasp --max_iteration 10 --alpha 0.1,0.2,0.3 --do_local_search 
```
4. Solve [project.45-1.dat](src/project/testdata/project.45-1.dat) using GRASP method with 100 iterations, setting alpha to 0.1,0.2, and 0.3, while not enabling local search phase.
```shell
python solve.py ../testdata/project.45-1.dat --method grasp --max_iteration 100 --alpha 0.1,0.2,0.3 
```


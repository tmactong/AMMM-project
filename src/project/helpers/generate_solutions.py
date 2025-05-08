from data_parser import parse
import json

def main():
    n, priority = parse('sol_from_cplex.dat')
    with open('generated_solution.json', 'w') as f:
        f.write(json.dumps({'MemberPriorities': priority}, indent=4))

if __name__ == '__main__':
    main()
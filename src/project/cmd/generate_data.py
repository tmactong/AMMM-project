import sys
import random
MaxBid = 10

def generate(dataset_count: int, member_count:int):
    for i in range(dataset_count):
        with open(f'../testdata/project.{member_count}-{i+1}.dat', 'w') as f:
            f.write(f'N = {member_count};\n\nm = [\n')
            for _ in range(member_count):
                f.write(f'\t[ { " ".join(
                    map(
                        str,
                        [x if idx != _ else 0 for idx, x in enumerate(random.choices(range(MaxBid), k=member_count))]
                    )
                )} ]\n')
            f.write(f'];')



if __name__ == "__main__":
    if sys.argv.__len__() < 3:
        print('Usage: python generate_data.py <dataset_count> <member_count>')
    generate(int(sys.argv[1]), int(sys.argv[2]))
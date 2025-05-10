import random

MaxDigit = 10


def generate(member_count):
    with open(f'../testdata/project.{member_count}members.dat', 'w') as f:
        f.write(f'N = {member_count};\n\nm = [\n')
        for _ in range(member_count):
            f.write(f'\t[ { " ".join(
                map(str, [x if idx != _ else 0 for idx, x in enumerate(random.choices(range(MaxDigit), k=member_count))  ])
            )} ]\n')
        f.write(f'];')



if __name__ == "__main__":
    generate(45)
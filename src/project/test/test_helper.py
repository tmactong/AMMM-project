from src.project.helpers import cycles_generator

def get_tree():
    yield from cycles_generator.generate_branches(
        [3],
        [(1, 4), (4, 1), (2, 1), (1, 2), (4, 3), (3, 4), (6, 1), (1, 6), (5, 6), (6, 5), (6, 3), (3, 6), (4, 6), (6, 4),
         (6, 2), (2, 6)]
    )


if __name__ == '__main__':
    # (1,3)
    tree = get_tree()
    for i in tree:
        print(i)
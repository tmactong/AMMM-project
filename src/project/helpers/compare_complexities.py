import sys

def get_combination_count(all: int, chosen: int) -> int:
    total = 1
    for i in range(all, all-chosen, -1):
        total *= i
    for i in range(1, chosen+1):
        total /= i
    return int(total)

def get_permutation_count(all: int) -> int:
    total = 1
    for i in range(all, 0, -1):
        total *= i
    return total

def deduplicate_loop_count(count: int) -> int:
    total = 0
    for i in range(0, count -2):
        loop_count = 1
        for j in range(1, i+1):
            loop_count *= count - 2 -j
        permutation_count = get_permutation_count(count - 2 -i)
        loop_count *= permutation_count
        total += loop_count
    return total

def duplicate_loop_count(count: int) -> int:
    return get_permutation_count(count)


def compare(all: int):
    total_deduplicated = 0
    total_duplicated = 0
    for i in range(3, all+1):
        combination_count = get_combination_count(all, i)
        deduplicated_loop_count = deduplicate_loop_count(i)
        total_deduplicated += deduplicated_loop_count * combination_count
        permutation_count = get_permutation_count(i)
        total_duplicated += permutation_count * combination_count
    return total_duplicated, total_deduplicated*2


if __name__ == "__main__":
    n = int(sys.argv[1])
    # print(get_combination_count(5, 3))
    # print(get_permutation_count(5))
    # print(deduplicate_loop_count(5))
    # print(duplicate_loop_count(5))
    print("n=%d" %n, ", ".join(list(map(str, compare(n)))))
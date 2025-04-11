import typing
import re


def parse(filename: str) -> (int, typing.Dict[int, typing.Dict[int, int]]):
    """
    data format:
    "N = 3;"
    m = [
        [  0   3   5  ]
        [  5   0   2  ]
        [  4   5   0  ]
    ];
    """
    n, m, m_started = 0, list(), False
    with open(filename, "r") as file:
        for line in file.readlines():
            if line.startswith("N"):
                match = re.search(r"N\s?=\s?(\d+);", line)
                if match:
                    n = int(match.group(1))
                else:
                    raise ValueError("N is not found")
            elif line.startswith("m"):
                m_started = True
            elif line.startswith("];"):
                break
            elif m_started:
                row = re.findall(r"\s+(\d+)", line)
                if len(row) != n:
                    raise ValueError("items of row is not compatible with N")
                else:
                    m.append([int(x) for x in row])
    if n == 0 or not m:
        raise IOError("no items found")
    return n, m


if __name__ == "__main__":
    n,m = parse("../testdata/project.1.dat")
    print(n)
    print(m)
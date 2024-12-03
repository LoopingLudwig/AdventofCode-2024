import re
from pathlib import Path


def parse_infile(path):
    RE_1 = re.compile(r"^\s*(\d+)\s+(\d+)\s*$", re.MULTILINE)

    with path.open() as f:
        matches = RE_1.findall(f.read())

    l1, l2 = zip(*matches)

    list1 = [int(i) for i in l1]
    list2 = [int(i) for i in l2]

    return list1, list2


def calc_1(list1, list2):
    sort_zip = zip(sorted(list1), sorted(list2))

    result = sum([abs(x - y) for x, y in sort_zip])

    return result


def calc_2(list1, list2):
    sim_score = 0
    for i in list1:
        sim_score += i * sum([1 for j in list2 if j == i])

    return sim_score


if __name__ == "__main__":
    l1, l2 = parse_infile(Path(__file__).parent / r"../input/input.txt")

    # Part one
    result_1 = calc_1(l1, l2)
    print(f"Result part one: {result_1}")

    # Part two
    result_2 = calc_2(l1, l2)
    print(f"Result part two: {result_2}")

import re
from pathlib import Path


def calc_1(path):
    RE_1 = re.compile(r"mul\((\d+),(\d+)\)")

    with path.open() as f:
        matches = RE_1.findall(f.read())

    res = sum([int(a) * int(b) for a, b in matches])

    return res


def calc_2(path):
    RE_1 = re.compile(r"mul\((\d+),(\d+)\)|don't\(\)|do\(\)")

    with path.open() as f:
        matches = RE_1.finditer(f.read())

    enable = True
    sum = 0

    for ma in matches:
        match ma.group(0):
            case "do()":
                enable = True
            case "don't()":
                enable = False
            case _:
                if enable:
                    sum += int(ma.group(1)) * int(ma.group(2))

    return sum


if __name__ == "__main__":
    # Part one
    result_1 = calc_1(Path(__file__).parent / r"../input/input.txt")
    print(f"Result part one: {result_1}")

    # Part two
    result_2 = calc_2(Path(__file__).parent / r"../input/input.txt")
    print(f"Result part two: {result_2}")

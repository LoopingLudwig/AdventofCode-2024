import re
from pathlib import Path

INPATH = Path(__file__).parent / r"input.txt"


def parse_input(s_in):
    RE_1 = re.compile(r"^(\d+): ((?:\s?\d+)*)$", re.MULTILINE)

    eqations = []
    for grp in RE_1.findall(s_in):
        eqations.append((int(grp[0]), [int(i) for i in grp[1].split(" ")]))

    return eqations


def test_operators(a, b, concat=False):
    res = []
    for x in b:
        res.append(a * x)
        res.append(a + x)
        if concat:
            res.append(int(f"{x}{a}"))
    return res


def test_equation(eq, concat=False):
    value = eq[0]
    operands = eq[1]

    posibl = operands[:1]
    for i in range(1, len(operands)):
        posibl = test_operators(operands[i], posibl, concat)
    return value in posibl


def calc_1(eqats):
    res = 0

    for eq in eqats:
        if test_equation(eq):
            # print(f"JA: {value}")
            res += eq[0]
    return res


def calc_2(eqats):
    res = 0

    for eq in eqats:
        if test_equation(eq):
            # print(f"JA: {value}")
            res += eq[0]
        elif test_equation(eq, True):
            res += eq[0]
    return res


if __name__ == "__main__":
    with INPATH.open() as f:
        s_input = f.read()

    s_test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    eqs = parse_input(s_input)

    # Part one
    result_1 = calc_1(eqs)
    print(f"Result part one: {result_1}")

    # Part one
    result_2 = calc_2(eqs)
    print(f"Result part two: {result_2}")

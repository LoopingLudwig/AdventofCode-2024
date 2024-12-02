import itertools
from pathlib import Path


def parse_infile(path):
    res = []
    with path.open() as f:
        for line in f.readlines():
            res.append([int(j) for j in line.split(" ")])
    return res


def check_pair(a, b):
    if abs(a - b) > 3 or a == b:
        return None
    else:
        return b > a


def check_report(report):
    levels_pairs = itertools.pairwise(report)
    if (first := check_pair(*next(levels_pairs))) is not None:
        for pair in levels_pairs:
            if check_pair(*pair) != first:
                break
        else:
            return True
    return False


def calc_1(reports):
    save_reports = 0
    for report in reports:
        if check_report(report):
            save_reports += 1
    return save_reports


# Lösung kann erst Nummer nicht löschen, dann halt try and error
def calc_2_wrong(reports):
    save_reports = 0
    for levels in reports:
        first = check_pair(levels[0], levels[1])
        last_value = levels[0]

        if first is None:
            i = 2
            bad_levels = 1
            first = check_pair(levels[0], levels[2])
            if first is None:
                continue
        else:
            i = 1
            bad_levels = 0

        while i < len(levels):
            if check_pair(last_value, levels[i]) == first:
                last_value = levels[i]
                i += 1
            else:
                i += 2
                bad_levels += 1

            if bad_levels > 1:
                break
        if bad_levels < 2:
            save_reports += 1
    return save_reports


# Mit der Brechstange, versuchsweise löschen
def calc_2(reports):
    save_reports = 0
    for report in reports:
        if check_report(report):
            save_reports += 1
        else:
            for del_pos in range(len(report)):
                if check_report(report[:del_pos] + report[del_pos + 1 :]):
                    save_reports += 1
                    break
    return save_reports


if __name__ == "__main__":
    l_input = parse_infile(Path(__file__).parent / r"../input/input.txt")

    # Part one
    result_1 = calc_1(l_input)
    print(f"Result part one: {result_1}")

    # Part two
    result_2 = calc_2(l_input)
    print(f"Result part two: {result_2}")

import re
from pathlib import Path

INPATH = Path(__file__).parent / r"../input/input.txt"


def parse_input(s_in):
    RE_rule = re.compile(r"^(\d+)\|(\d+)$", re.MULTILINE)
    RE_order = re.compile(r"^\d+,(?:\d+,?)*$", re.MULTILINE)

    rules = [(int(x), int(y)) for x, y in RE_rule.findall(s_in)]

    orders = [
        [int(pos) for pos in order.group(0).split(",")]
        for order in RE_order.finditer(s_in)
    ]

    return rules, orders


def check_rule(rule, order):
    if not (rule[0] in order and rule[1] in order):
        return True
    elif not (order.index(rule[0]) < order.index(rule[1])):
        return False
    else:
        return True


def check_order(order, rules):
    for rule in rules:
        if not check_rule(rule, order):
            return False
    else:
        return True


def fix_order(order, rule):
    if check_rule(rule, order):
        return order

    idx_x = order.index(rule[0])
    diff = idx_x - order.index(rule[1])

    order.insert(idx_x - diff, order.pop(idx_x))
    return order


def calc_1(rules, orders):
    middlesum = 0
    for order in orders:
        if check_order(order, rules):
            middlesum += order[len(order) // 2]
    return middlesum


def calc_2(rules, orders):
    fixed_orders = []

    for order in orders:
        if check_order(order, rules):
            continue
        new_order = order[:]
        while not check_order(order, rules):
            for rule in rules:
                new_order = fix_order(order, rule)
        fixed_orders.append(new_order)

    return calc_1(rules, fixed_orders)


if __name__ == "__main__":
    with INPATH.open() as f:
        s_input = f.read()

    s_test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    rules, orders = parse_input(s_input)

    # Part one
    result_1 = calc_1(rules, orders)
    print(f"Result part one: {result_1}")

    result_2 = calc_2(rules, orders)
    print(f"Result part two: {result_2}")

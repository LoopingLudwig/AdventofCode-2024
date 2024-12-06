import copy
from pathlib import Path

INPATH = Path(__file__).parent / r"../input/input.txt"


def parse_input(s_in):
    karte = []

    start_pos = ()

    for i, line in enumerate(s_in.splitlines()):
        if "^" in line:
            start_pos = (i, line.find("^"))
            karte.append(list(line.replace("^", "X")))
        else:
            karte.append(list(line))

    return karte, start_pos


def calc_1(karte_in, start_pos):
    karte = copy.deepcopy(karte_in)

    walk_dir = 0
    cur_pos = start_pos

    while True:
        match walk_dir:
            case 0:
                next_pos = (cur_pos[0] - 1, cur_pos[1])
            case 1:
                next_pos = (cur_pos[0], cur_pos[1] + 1)
            case 2:
                next_pos = (cur_pos[0] + 1, cur_pos[1])
            case 3:
                next_pos = (cur_pos[0], cur_pos[1] - 1)

        if (
            not (next_pos[0] < len(karte) and next_pos[1] < len(karte[0]))
            or min(next_pos) < 0
        ):
            break
        elif karte[next_pos[0]][next_pos[1]] == "#":
            walk_dir = (walk_dir + 1) % 4
        else:
            karte[next_pos[0]][next_pos[1]] = "X"
            cur_pos = next_pos

        # print("\n".join(["".join(i) for i in karte]))

    kart_s = "\n".join(["".join(i) for i in karte])

    return kart_s, kart_s.count("X")


def check_looped(karte_in, start_pos, obstacle):
    karte = copy.deepcopy(karte_in)

    karte[obstacle[0]][obstacle[1]] = "#"

    walk_dir = 0
    cur_pos = start_pos

    turns_on_walked_path = 0
    while True:
        match walk_dir:
            case 0:
                next_pos = (cur_pos[0] - 1, cur_pos[1])
            case 1:
                next_pos = (cur_pos[0], cur_pos[1] + 1)
            case 2:
                next_pos = (cur_pos[0] + 1, cur_pos[1])
            case 3:
                next_pos = (cur_pos[0], cur_pos[1] - 1)

        if (
            not (next_pos[0] < len(karte) and next_pos[1] < len(karte[0]))
            or min(next_pos) < 0
        ):
            return False
        elif karte[next_pos[0]][next_pos[1]] == "#":
            walk_dir = (walk_dir + 1) % 4
            turns_on_walked_path += 1
            if turns_on_walked_path > 4:
                # ("\n".join(["".join(i) for i in karte]))
                return True

        else:
            if karte[next_pos[0]][next_pos[1]] == ".":
                turns_on_walked_path = 0
            karte[next_pos[0]][next_pos[1]] = "X"
            cur_pos = next_pos


# Bruteforce 4 the win
def calc_2(karte, start_pos):
    pos_obstacle = 0
    for line in range(len(karte)):
        for col in range(len(karte[0])):
            if (line, col) == start_pos:
                continue
            elif check_looped(karte, start_pos, (line, col)):
                # print(f"Mögliche Hindernispositon: {line}, {col}")
                pos_obstacle += 1

    # print(f"Insgesamt {pos_obstacle} mögliche Positionen für Hindernisse")
    return pos_obstacle


if __name__ == "__main__":
    with INPATH.open() as f:
        s_input = f.read()

    s_test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    karte, start_pos = parse_input(s_input)

    # Part one
    karte_s, positions = calc_1(karte, start_pos)
    print(f"Result part one: {positions}")

    result_2 = calc_2(karte, start_pos)
    print(f"Result part two: {result_2}")

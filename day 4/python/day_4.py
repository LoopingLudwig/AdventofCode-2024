import re
from pathlib import Path

INPATH = Path(__file__).parent / r"../input/input.txt"


def transpose_str(s_in):
    trans = ""
    lines = s_in.splitlines()
    for i in range(len(lines[0])):
        trans_line = ""
        for line in lines:
            trans_line += line[i]
        trans += trans_line + "\n"
    return trans


def day_4(s_in):
    RE_1 = re.compile(r"XMAS")
    RE_2 = re.compile(r"SAMX")

    words = 0

    # Geradeaus:
    words += len(RE_1.findall(s_in))
    # Rückwärts
    words += len(RE_2.findall(s_in))

    #
    # Senkrecht
    trans = transpose_str(s_in)
    words += len(RE_1.findall(trans))
    words += len(RE_2.findall(trans))

    # Diagonal nach rechts
    lines = s_in.splitlines()
    for i in range(len(lines) - 3):
        temp_lines = []
        for j in range(0, 4):
            temp_lines.append(lines[i + j][j:] + " " * j)
        temp_trans = transpose_str("\n".join(temp_lines))
        words += len(RE_1.findall(temp_trans))
        words += len(RE_2.findall(temp_trans))

    # Diagonal nach links
    for i in range(len(lines) - 3):
        temp_lines = []
        for j in range(0, 4):
            temp_lines.append(lines[i + j][3 - j :] + " " * (3 - j))
        temp_trans = transpose_str("\n".join(temp_lines))
        words += len(RE_1.findall(temp_trans))
        words += len(RE_2.findall(temp_trans))

    print(f"Anzahl Teil 1: {words}")


# Mit der Brechstange, weil müde
def day_4_two(s_in):
    lines = s_in.splitlines()

    RE_1 = re.compile(r"^M.S$")
    RE_2 = re.compile(r"^S.M$")
    RE_3 = re.compile(r"^S.S$")
    RE_4 = re.compile(r"^M.M$")

    crosses = 0
    for i in range(len(lines) - 2):
        for j in range(len(lines[0]) - 2):
            # A in der Mitte ist Pflicht
            if not lines[i + 1][j + 1] == "A":
                continue

            if (
                (
                    (RE_1.match(lines[i][j : j + 3]) is not None)
                    & (RE_1.match(lines[i + 2][j : j + 3]) is not None)
                )
                | (
                    (RE_2.match(lines[i][j : j + 3]) is not None)
                    & (RE_2.match(lines[i + 2][j : j + 3]) is not None)
                )
                | (
                    (RE_3.match(lines[i][j : j + 3]) is not None)
                    & (RE_4.match(lines[i + 2][j : j + 3]) is not None)
                )
                | (
                    (RE_4.match(lines[i][j : j + 3]) is not None)
                    & (RE_3.match(lines[i + 2][j : j + 3]) is not None)
                )
            ):
                crosses += 1
    print(f"Anzahl Teil 2: {crosses}")


if __name__ == "__main__":
    with INPATH.open() as f:
        s_input = f.read()

    s_test = """.M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    .........."""

    day_4(s_input)
    day_4_two(s_input)

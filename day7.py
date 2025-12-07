import sys

lines: list[str] = []

while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    lines.append(line)

startpos = lines[0].find("S")
beams = {startpos}

sol1 = 0

for line in lines[1:]:
    new_beams: set[int] = set()
    for beam in beams:
        if line[beam] == "^":
            sol1 += 1
            if beam > 0:
                new_beams.add(beam - 1)
            if beam < len(line):
                new_beams.add(beam + 1)
        else:
            new_beams.add(beam)
    beams = new_beams

print(f"Solution 1: {sol1}")

cache: dict[tuple[int, int], int] = {}


def get_sol2(line: int, pos: int) -> int:
    global lines
    global cache
    if (line, pos) in cache:
        return cache[(line, pos)]

    if line == len(lines):
        return 1

    if lines[line][pos] == ".":
        rec = get_sol2(line + 1, pos)
        cache[(line, pos)] = rec
        return rec

    rec = 0
    if pos > 0:
        rec += get_sol2(line + 1, pos - 1)
    if pos < len(lines[line]):
        rec += get_sol2(line + 1, pos + 1)

    cache[(line, pos)] = rec
    return rec


sol2 = get_sol2(1, startpos)

print(f"Solutions 2: {sol2}")

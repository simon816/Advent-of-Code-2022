import sys

MAX = 4000000

scanners = []

for line in sys.stdin.readlines():
    line = line.strip()
    spos, bpos = line.split(':')
    spos = spos[len('Sensor at '):]
    bpos = bpos[len('closest beacon is at '):]
    spos_x, spos_y = tuple(int(p[p.index('=') + 1:]) for p in spos.split(','))
    bpos_x, bpos_y = tuple(int(p[p.index('=') + 1:]) for p in bpos.split(','))

    distance = abs(spos_x - bpos_x) + abs(spos_y - bpos_y)

    scanners.append((spos_x, spos_y, distance))

for line in range(MAX + 1):
    ranges = []
    for (spos_x, spos_y, distance) in scanners:
        if spos_y >= line and spos_y - line <= distance:
            num_on_line = distance - (spos_y - line)
        elif spos_y <= line and line - spos_y <= distance:
            num_on_line = distance - (line - spos_y)
        else:
            continue
        if num_on_line < 0:
            continue

        lower = spos_x - num_on_line
        upper = spos_x + num_on_line
        if lower <= 4000000 and upper >= 0:
            ranges.append((max(0, lower), min(MAX, upper)))
    ranges = sorted(ranges)
    coverage = 0
    found_x = None
    for (lower, upper) in ranges:
        if lower > coverage + 1:
            found_x = coverage + 1
            break
        else:
            coverage = max(coverage, upper)
    if found_x is not None:
        break
print("Found", found_x, line)
print((found_x * 4000000) + line)

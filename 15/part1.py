import sys

Y_LINE = 2000000

x_pos_set = set()
beacons_on_line = set()

for line in sys.stdin.readlines():
    line = line.strip()
    spos, bpos = line.split(':')
    spos = spos[len('Sensor at '):]
    bpos = bpos[len('closest beacon is at '):]
    spos_x, spos_y = tuple(int(p[p.index('=') + 1:]) for p in spos.split(','))
    bpos_x, bpos_y = tuple(int(p[p.index('=') + 1:]) for p in bpos.split(','))

    if bpos_y == Y_LINE:
        beacons_on_line.add(bpos_x)

    distance = abs(spos_x - bpos_x) + abs(spos_y - bpos_y)

    if spos_y >= Y_LINE and spos_y - Y_LINE <= distance:
        num_on_line = distance - (spos_y - Y_LINE)
    elif spos_y <= Y_LINE and Y_LINE - spos_y <= distance:
        num_on_line = distance - (Y_LINE - spos_y)
    else:
        continue
    if num_on_line < 0:
        continue

    lower = spos_x - num_on_line
    upper = spos_x + num_on_line
    for x in range(lower, upper + 1):
        x_pos_set.add(x)

print(len(x_pos_set - beacons_on_line))

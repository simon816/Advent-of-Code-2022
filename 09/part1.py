import sys

hpos_x, hpos_y = 0, 0
tpos_x, tpos_y = 0, 0

visits = set([(0, 0)])

for line in sys.stdin.readlines():
    dir, num = line.strip().split(' ')
    num = int(num)

    for _ in range(num):

        if dir == 'R':
            hpos_x += 1
            if abs(hpos_x - tpos_x) < 2:
                pass
            elif tpos_y == hpos_y:
                tpos_x += 1
            elif tpos_y == hpos_y - 1:
                tpos_x += 1
                tpos_y += 1
            elif tpos_y == hpos_y + 1:
                tpos_x += 1
                tpos_y -= 1
            else:
                assert False, (tpos_x, tpos_y, hpos_x, hpos_y)

        elif dir == 'U':

            hpos_y += 1
            if abs(hpos_y - tpos_y) < 2:
                pass
            elif tpos_x == hpos_x:
                tpos_y += 1
            elif tpos_x == hpos_x - 1:
                tpos_y += 1
                tpos_x += 1
            elif tpos_x == hpos_x + 1:
                tpos_y += 1
                tpos_x -= 1
            else:
                assert False, (tpos_x, tpos_y, hpos_x, hpos_y)

        elif dir == 'L':

            hpos_x -= 1
            if abs(hpos_x - tpos_x) < 2:
                pass
            elif tpos_y == hpos_y:
                tpos_x -= 1
            elif tpos_y == hpos_y - 1:
                tpos_x -= 1
                tpos_y += 1
            elif tpos_y == hpos_y + 1:
                tpos_x -= 1
                tpos_y -= 1
            else:
                assert False, (tpos_x, tpos_y, hpos_x, hpos_y)

        elif dir == 'D':
            hpos_y -= 1
            if abs(hpos_y - tpos_y) < 2:
                pass
            elif tpos_x == hpos_x:
                tpos_y -= 1
            elif tpos_x == hpos_x - 1:
                tpos_y -= 1
                tpos_x += 1
            elif tpos_x == hpos_x + 1:
                tpos_y -= 1
                tpos_x -= 1
            else:
                assert False, (tpos_x, tpos_y, hpos_x, hpos_y)
 
        visits.add((tpos_x, tpos_y))
#        print((tpos_x, tpos_y), (hpos_x, hpos_y))

print(len(visits))

import sys

def move_tail(hpos, tpos):
    hpos_x, hpos_y = hpos
    tpos_x, tpos_y = tpos

    if abs(hpos_x - tpos_x) == 2:
        if tpos_y < hpos_y:
            tpos_y += 1
        elif tpos_y > hpos_y:
            tpos_y -= 1
        
        if hpos_x > tpos_x:
            tpos_x += 1
        else:
            tpos_x -= 1

    if abs(hpos_y - tpos_y) == 2:
        if tpos_x < hpos_x:
            tpos_x += 1
        elif tpos_x > hpos_x:
            tpos_x -= 1
        
        if hpos_y > tpos_y:
            tpos_y += 1
        else:
            tpos_y -= 1

    return (tpos_x, tpos_y)

hpos_x, hpos_y = 0, 0
chain = [(0, 0) for _ in range(9)]

visits = set([chain[-1]])

for line in sys.stdin.readlines():
    dir, num = line.strip().split(' ')
    num = int(num)

    for _ in range(num):

        if dir == 'R':
            hpos_x += 1

        elif dir == 'U':
            hpos_y += 1

        elif dir == 'L':
            hpos_x -= 1

        elif dir == 'D':
            hpos_y -= 1

        prev = (hpos_x, hpos_y)
        for i, tail in enumerate(chain):
            chain[i] = move_tail(prev, tail)
            prev = chain[i]

        visits.add(chain[-1])

print(len(visits))

import sys

grid = [['.'] * 1000 for _ in range(1000)]

bottom = 0

for line in sys.stdin.readlines():
    line = line.strip()
    path = [tuple(map(int, n.split(','))) for n in line.split(' -> ')]

    prev_x, prev_y = None, None
    for (x, y) in path:
        if prev_x is None:
            grid[y][x] = '#'
        else:
            for new_y in range(min(y, prev_y), max(y, prev_y) + 1):
                grid[new_y][x] = '#'
            for new_x in range(min(x, prev_x), max(x, prev_x) + 1):
                grid[y][new_x] = '#'
        prev_x, prev_y = x, y
        bottom = max(bottom, y + 2)

count = 0
full = False
while not full:
    pos_x, pos_y = 500, 0

    while True:
        if pos_y + 1 == bottom:
            grid[pos_y][pos_x] = 'o'
            count += 1
            break
        elif grid[pos_y + 1][pos_x] == '.':
            pos_y += 1
        elif grid[pos_y + 1][pos_x - 1] == '.':
            pos_y += 1
            pos_x -= 1
        elif grid[pos_y + 1][pos_x + 1] == '.':
            pos_y += 1
            pos_x += 1
        else:
            grid[pos_y][pos_x] = 'o'
            count += 1
            if pos_x == 500 and pos_y == 0:
                full = True
            break

print(count)

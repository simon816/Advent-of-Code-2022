import sys

grid = [['.'] * 1000 for _ in range(1000)]


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

count = 0
forever = False
while not forever:
    pos_x, pos_y = 500, 0

    while True:
        if grid[pos_y + 1][pos_x] == '.':
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
            break
        if pos_y < 0 or pos_y == 999 or pos_x < 0 or pos_x == 1000:
            forever = True
            break

print(count)

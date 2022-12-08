import sys

grid = []

width = 0

for row in sys.stdin.readlines():
    cols = [int(n) for n in row.strip()]
    width = max(width, len(cols))
    grid.append(cols)

count = 0

for y in range(len(grid)):
    for x in range(width):
        val = grid[y][x]
        visible = True
        for look_x in range(0, x):
            if grid[y][look_x] < val:
                visible = True
            else:
                visible = False
                break
        if not visible:
            visible = True
            for look_x in range(x + 1, width):
                if grid[y][look_x] < val:
                    visible = True
                else:
                    visible = False
                    break
        if not visible:
            visible = True
            for look_y in range(0, y):
                if grid[look_y][x] < val:
                    visible = True
                else:
                    visible = False
                    break
        if not visible:
            visible = True
            for look_y in range(y + 1, len(grid)):
                if grid[look_y][x] < val:
                    visible = True
                else:
                    visible = False
                    break
        if visible:
            count += 1

print(count)

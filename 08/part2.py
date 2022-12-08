import sys

grid = []

width = 0

for row in sys.stdin.readlines():
    cols = [int(n) for n in row.strip()]
    width = max(width, len(cols))
    grid.append(cols)

max_score = 0

for y in range(len(grid)):
    for x in range(width):
        val = grid[y][x]
        distance_1 = 0
        distance_2 = 0
        distance_3 = 0
        distance_4 = 0
        for look_y in range(y - 1, -1, -1):
            if grid[look_y][x] < val:
                distance_1 += 1
            else:
                distance_1 += 1
                break
        for look_x in range(x - 1, -1, -1):
            if grid[y][look_x] < val:
                distance_2 += 1
            else:
                distance_2 += 1
                break
        for look_y in range(y + 1, len(grid)):
            if grid[look_y][x] < val:
                distance_3 += 1
            else:
                distance_3 += 1
                break
        for look_x in range(x + 1, width):
            if grid[y][look_x] < val:
                distance_4 += 1
            else:
                distance_4 += 1
                break
        score = distance_1 * distance_2 * distance_3 * distance_4
        max_score = max(score, max_score)

print(max_score)

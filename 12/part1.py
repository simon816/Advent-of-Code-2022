import sys

goal_x = 0
goal_y = 0

pos_x = 0
pos_y = 0

width = 0

grid = []
for line in sys.stdin.readlines():
    if 'S' in line:
        pos_y = len(grid)
        pos_x = line.index('S')
    if 'E' in line:
        goal_y = len(grid)
        goal_x = line.index('E')
    grid.append([ord(c) for c in line.strip()])
    width = len(grid[-1])

grid[pos_y][pos_x] = ord('a')
grid[goal_y][goal_x] = ord('z')

def get_adj(x, y):
    adj = []
    if y > 0:
        adj.append((x, y - 1))
    if x > 0:
        adj.append((x - 1, y))
    if y < len(grid) - 1:
        adj.append((x, y + 1))
    if x < width - 1:
        adj.append((x + 1, y))
    return adj

visited = set()

costs = {}

costs[(pos_x, pos_y)] = 0
cur_cost = 0

while (pos_x, pos_y) != (goal_x, goal_y):
    cur_cost = costs[(pos_x, pos_y)] = min(cur_cost, costs[(pos_x, pos_y)])
    visited.add((pos_x, pos_y))
    adj = get_adj(pos_x, pos_y)
    cur_val = grid[pos_y][pos_x]
    for (x, y) in adj:
        if (x, y) in visited:
            continue
        if grid[y][x] <= cur_val + 1:
            if (x, y) in costs:
                costs[(x, y)] = min(costs[(x, y)], cur_cost + 1)
            else:
                costs[(x, y)] = cur_cost + 1
    
    non_perms = list(filter(lambda e: e[0] not in visited, costs.items()))
    assert non_perms, "No Route!"
    lowest = min(map(lambda e: e[1], non_perms))
    matching = filter(lambda e: e[1] == lowest, non_perms)
    pos_x, pos_y = next(matching)[0]
    cur_cost += 1

print(costs[(goal_x, goal_y)])

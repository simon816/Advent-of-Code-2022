import sys

read_steps = False

width = None
grid = []
steps = []

for line in sys.stdin.readlines():
    line = line.strip('\n')
    if not line:
        read_steps = True
        continue

    if read_steps:
        n = ''
        for c in line:
            if c.isdigit():
                n += c
            else:
                steps.append(int(n))
                steps.append(c)
                n = ''
        if n:
            steps.append(int(n))
    else:
        if width is None:
            width = len(line)
        grid.append(line)

def rightmost(row):
    return max(row.rindex('.'), row.rindex('#'))

def leftmost(row):
    return min(row.index('.'), row.index('#'))

def lowermost(grid, col):
    for y in range(len(grid) - 1, -1, -1):
        if col > len(grid[y]) - 1:
            continue
        if grid[y][col] != ' ':
            return y

def uppermost(grid, col):
    for y in range(0, len(grid)):
        if col > len(grid[y]) - 1:
            continue
        if grid[y][col] != ' ':
            return y

move_map = [
    (1, 0), # east
    (0, 1), # south
    (-1, 0), # west
    (0, -1), # north
]
facing = 0
pos = (0, grid[0].index('.')) # row, col

for move in steps:
    if move == 'L':
        facing = (facing - 1) % 4
    elif move == 'R':
        facing = (facing + 1) % 4
    else:
        f = move_map[facing]
        for _ in range(move):
            new_row, new_col = pos[0] + f[1], pos[1] + f[0]
            # n.b. assumes only one of new_row or new_col changes
            if f[1] == 0:
                if new_col < 0:
                    new_col = rightmost(grid[new_row])
                elif new_col > len(grid[new_row]) - 1:
                    new_col = leftmost(grid[new_row])
                elif grid[new_row][new_col] == ' ':
                    if f[0] == 1:
                        new_col = leftmost(grid[new_row])
                    else:
                        new_col = rightmost(grid[new_row])
            if f[0] == 0:
                if new_row < 0:
                    new_row = lowermost(grid, new_col)
                elif new_row > len(grid) - 1:
                    new_row = uppermost(grid, new_col)
                if new_col > len(grid[new_row]) - 1 or grid[new_row][new_col] == ' ':
                    # we've gone up/down and passed the end of the next row
                    if new_row > pos[0]:
                        new_row = uppermost(grid, new_col)
                    elif new_row < pos[0]:
                        new_row = lowermost(grid, new_col)
                    else:
                        assert False
            if grid[new_row][new_col] == '#':
                break
            pos = new_row, new_col

print((pos[0] + 1) * 1000 + (pos[1] + 1) * 4 + facing)

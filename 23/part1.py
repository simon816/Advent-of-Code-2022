import sys

grid = []
for line in sys.stdin.readlines():
    grid.append(list(line.strip()))

def check_north(row, col):
    if row == 0:
        return (-1, col)
    if grid[row - 1][col] == '.' and \
       (col == 0 or grid[row - 1][col - 1] == '.') and \
       (col == len(grid[row - 1]) - 1 or grid[row - 1][col + 1] == '.'):
        return (row - 1, col)
    return None

def check_south(row, col):
    if row == len(grid) - 1:
        return (row + 1, col)
    if grid[row + 1][col] == '.' and \
       (col == 0 or grid[row + 1][col - 1] == '.') and \
       (col == len(grid[row + 1]) - 1 or grid[row + 1][col + 1] == '.'):
        return (row + 1, col)
    return None

def check_west(row, col):
    if col == 0:
        return (row, -1)
    if grid[row][col - 1] == '.' and \
       (row == 0 or grid[row - 1][col - 1] == '.') and \
       (row == len(grid) - 1 or grid[row + 1][col - 1] == '.'):
        return (row, col - 1)
    return None

def check_east(row, col):
    if col == len(grid[row]) - 1:
        return (row, col + 1)
    if grid[row][col + 1] == '.' and \
       (row == 0 or grid[row - 1][col + 1] == '.') and \
       (row == len(grid) - 1 or grid[row + 1][col + 1] == '.'):
        return (row, col + 1)
    return None

checkers = [check_north, check_south, check_west, check_east]

for _ in range(10):
    proposed = {}
    for row_num, row in enumerate(grid):
        for col_num, c in enumerate(row):
            if c == '#':
                first_loc = None
                can_do_all = True
                for check in checkers:
                    new_loc = check(row_num, col_num)
                    if first_loc is None:
                        first_loc = new_loc
                    if new_loc is None:
                        can_do_all = False
                if first_loc is not None and not can_do_all:
                    if first_loc in proposed:
                        del proposed[first_loc]
                    else:
                        proposed[first_loc] = (row_num, col_num)

    new_west = ['.'] * len(grid) 
    new_east = ['.'] * len(grid)
    new_north = ['.'] * len(grid[0])
    new_south = ['.'] * len(grid[0])
    for (new_row, new_col), (old_row, old_col) in proposed.items():
        grid[old_row][old_col] = '.'
        if new_row == -1:
            new_north[new_col] = '#'
        elif new_row == len(grid):
            new_south[new_col] = '#'
        elif new_col == -1:
            new_west[new_row] = '#'
        elif new_col == len(grid[new_row]):
            new_east[new_row] = '#'
        else:
            grid[new_row][new_col] = '#'

    if any(c == '#' for c in new_west):
        new_north.insert(0, '.')
        new_south.insert(0, '.')
        for i, row in enumerate(grid):
            row.insert(0, new_west[i])
    if any(c == '#' for c in new_east):
        new_north.append('.')
        new_south.append('.')
        for i, row in enumerate(grid):
            row.append(new_east[i])
    if any(c == '#' for c in new_north):
        grid.insert(0, new_north)
    if any(c == '#' for c in new_south):
        grid.append(new_south)

    checkers.append(checkers.pop(0))


min_row = max_row = None
min_col = max_col = None
for i, row in enumerate(grid):
    idx = -1
    try:
        idx = row.index('#')
    except ValueError:
        pass
    if idx != -1:
        if min_row is None:
            min_row = i
            max_row = i
            min_col = idx
            max_col = idx
        max_row = i
        min_col = min(min_col, idx)
        for j in range(len(row) - 1, -1, -1):
            if row[j] == '#':
                max_col = max(max_col, j)
                break

count = 0
for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col + 1):
        if grid[r][c] == '.':
            count += 1

print(count)

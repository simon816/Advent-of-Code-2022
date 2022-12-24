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

EAST, SOUTH, WEST, NORTH = range(4)

# heading off the west side
def wrap_west(pos):
    #print("Wrap west")
    row, _ = pos
    if row >= 0 and row < 50:
        return EAST, 149 - row, 0
    elif row >= 50 and row < 100:
        return SOUTH, 100, row - 50
    elif row >= 100 and row < 150:
        return EAST, 149 - row, 50
    elif row >= 150 and row < 200:
        return SOUTH, 0, row - 100
    else:
        assert False, pos

# heading off the east side
def wrap_east(pos):
    #print("Wrap east")
    row, _ = pos
    if row >= 0 and row < 50:
        return WEST, 149 - row, 99
    elif row >= 50 and row < 100:
        return NORTH, 49, 100 + (row - 50)
    elif row >= 100 and row < 150:
        return WEST, 149 - row, 149 
    elif row >= 150 and row < 200:
        return NORTH, 149, row - 100
    else:
        assert False, pos

def wrap_south(pos):
    #print("Wrap south")
    _, col = pos
    if col >= 0 and col < 50:
        return SOUTH, 0, col + 100
    elif col >= 50 and col < 100:
        return WEST, col + 100, 49
    elif col >= 100 and col < 150:
        return WEST, col - 50, 99
    else:
        assert False, pos

def wrap_north(pos):
    #print("Wrap north")
    _, col = pos
    if col >= 0 and col < 50:
        return EAST, col + 50, 50
    elif col >= 50 and col < 100:
        return EAST, col + 100, 0
    elif col >= 100 and col < 150:
        return NORTH, 199, col - 100
    else:
        assert False, pos

move_map = [
    (1, 0), # east
    (0, 1), # south
    (-1, 0), # west
    (0, -1), # north
]
facing = 0
pos = (0, grid[0].index('.')) # row, col

face_sym = [
    '>', 'v', '<', '^'
]

def print_grid():
    before = []
    after = []
    for r, row in enumerate(grid):
        if r == pos[0]:
            row = list(row)
            row[pos[1]] = '\x1b[47m\033[92m%s\033[00m\x1b[40m' % face_sym[facing]
            row = ''.join(row)
        if r <= pos[0]:
            before.append(row)
        else:
            after.append(row)
    H = 40
    n = min(H // 2, len(before))
    for i in range(n):
        print(before[ - (n - i) ])
    for i in range(n, H):
        print(after.pop(0))
    print()
    input()

for move in steps:
    #print("Move", move)
    if move == 'L':
        facing = (facing - 1) % 4
    elif move == 'R':
        facing = (facing + 1) % 4
    else:
        for _ in range(move):
            #print_grid()
            f = move_map[facing]
            new_facing = facing
            new_row, new_col = pos[0] + f[1], pos[1] + f[0]
            # n.b. assumes only one of new_row or new_col changes
            # east/west
            if f[1] == 0:
                if new_col < 0:
                    new_facing, new_row, new_col = wrap_west(pos)
                elif new_col > len(grid[new_row]) - 1:
                    new_facing, new_row, new_col = wrap_east(pos)
                elif grid[new_row][new_col] == ' ':
                    if f[0] == 1:
                        # heading east
                        new_facing, new_row, new_col = wrap_east(pos)
                    else:
                        # heading west
                        new_facing, new_row, new_col = wrap_west(pos)
            # north/south
            elif f[0] == 0:
                if new_row < 0:
                    new_facing, new_row, new_col = wrap_north(pos)
                elif new_row > len(grid) - 1:
                    new_facing, new_row, new_col = wrap_south(pos)
                elif new_col > len(grid[new_row]) - 1 or grid[new_row][new_col] == ' ':
                    # we've gone up/down and passed the end of the next row
                    if new_row > pos[0]:
                        new_facing, new_row, new_col = wrap_south(pos)
                    elif new_row < pos[0]:
                        new_facing, new_row, new_col = wrap_north(pos)
                    else:
                        assert False
            else:
                assert False
            #print((facing, *pos), "->", (new_facing, new_row, new_col))
            assert grid[new_row][new_col] != ' ', (new_row, new_col)
            if grid[new_row][new_col] == '#':
                break
            pos = new_row, new_col
            facing = new_facing

print((pos[0] + 1) * 1000 + (pos[1] + 1) * 4 + facing)

import sys
from collections import namedtuple
import queue

class Tile(namedtuple('Tile', 'up down left right wall')):

    def __str__(self):
        if self.wall:
            return '#'
        sum = self.get_sum()
        if sum > 1:
            return str(sum)
        if self.up:
            return '^'
        if self.down:
            return 'v'
        if self.left:
            return '<'
        if self.right:
            return '>'
        return '.'

    def get_sum(self):
        return self.up + self.down + self.left + self.right

    def empty(self):
        return not self.wall and self.get_sum() == 0

def mk_tile(c):
    up = down = left = right = 0
    wall = False
    if c == '^':
        up = 1
    elif c == 'v':
        down = 1
    elif c == '<':
        left = 1
    elif c == '>':
        right = 1
    elif c == '#':
        wall = True
    return Tile(up, down, left, right, wall)

def replace(grid, row, col, up=False, down=False, left=False, right=False):
    if row == 0:
        assert grid[row][col].wall
        row = len(grid) - 2
    elif row == len(grid) - 1:
        assert grid[row][col].wall
        row = 1
    if col == 0:
        assert grid[row][col].wall
        col = len(grid[row]) - 2
    elif col == len(grid[row]) - 1:
        assert grid[row][col].wall
        col = 1
    tile = grid[row][col]
    if up:
        tile = tile._replace(up=tile.up + 1)
    if down:
        tile = tile._replace(down=tile.down + 1)
    if left:
        tile = tile._replace(left=tile.left + 1)
    if right:
        tile = tile._replace(right=tile.right + 1)
    grid[row][col] = tile

def decrement(grid, row, col, up=False, down=False, left=False, right=False):
    tile = grid[row][col]
    if up:
        assert tile.up > 0
        tile = tile._replace(up=tile.up - 1)
    if down:
        assert tile.down > 0
        tile = tile._replace(down=tile.down - 1)
    if left:
        assert tile.left > 0
        tile = tile._replace(left=tile.left - 1)
    if right:
        assert tile.right > 0
        tile = tile._replace(right=tile.right - 1)
    grid[row][col] = tile

def get_next(state):
    new_state = [[t for t in row] for row in state]
    for row_num, row in enumerate(state):
        for col_num, tile in enumerate(row):
            if tile.up:
                replace(new_state, row_num - 1, col_num, up=True)
                decrement(new_state, row_num, col_num, up=True)
            if tile.down:
                replace(new_state, row_num + 1, col_num, down=True)
                decrement(new_state, row_num, col_num, down=True)
            if tile.left:
                replace(new_state, row_num, col_num - 1, left=True)
                decrement(new_state, row_num, col_num, left=True)
            if tile.right:
                replace(new_state, row_num, col_num + 1, right=True)
                decrement(new_state, row_num, col_num, right=True)
    return tuple(tuple(r) for r in new_state)

grids = []
grid_ids = {}

def get_adj(state):
    (row, col), grid_id = state
    grid = grids[grid_id]
    adj = []
    new_grid = get_next(grid)

    if new_grid in grid_ids:
        n_id = grid_ids[new_grid]
    else:
        n_id = len(grids)
        grid_ids[new_grid] = n_id
        grids.append(new_grid)

    if row < len(new_grid) - 1 and new_grid[row + 1][col].empty():
        adj.append(((row + 1, col), n_id))
    if row > 0 and new_grid[row - 1][col].empty():
        adj.append(((row - 1, col), n_id))
    if col < len(grid[row]) - 1 and new_grid[row][col + 1].empty():
        adj.append(((row, col + 1), n_id))
    if col > 0 and new_grid[row][col - 1].empty():
        adj.append(((row, col - 1), n_id))
    if new_grid[row][col].empty():
        adj.append(((row, col), n_id))
    return adj

grid = []
for line in sys.stdin.readlines():
    grid.append([mk_tile(c) for c in line.strip()])

q = queue.PriorityQueue()

states = []
state_ids = {}

def state_id(state):
    if state not in state_ids:
        state_ids[state] = len(states)
        states.append(state)
    return state_ids[state]

pos = (0, grid[0].index(mk_tile('.')))
init_grid = tuple(tuple(r) for r in grid)
grids.append(init_grid)
grid_ids[init_grid] = 0
state = (pos, grid_ids[init_grid])
s_id = state_id(state)

visited = set()
costs = {}
costs[s_id] = 0
cur_cost = 0
# while not on the bottom row
while state[0][0] != len(grid) - 1:
    state = states[s_id]
    cur_cost = costs[s_id] = min(cur_cost, costs[s_id])
    visited.add(s_id)
    adj = get_adj(state)
    for new_state in adj:
        n_id = state_id(new_state)
        if n_id in visited:
            continue
        if n_id in costs:
            prev = costs[n_id]
            if cur_cost + 1 < prev:
                costs[n_id] = cur_cost + 1
                q.put((costs[n_id], n_id))
        else:
            costs[n_id] = cur_cost + 1
            q.put((costs[n_id], n_id))

    p, s_id = q.get()
    while s_id in visited:
        p, s_id = q.get()
    cur_cost += 1

print(costs[s_id])

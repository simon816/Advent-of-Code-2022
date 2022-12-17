import itertools
import sys

moves = list(sys.stdin.read().strip())

shapes = [
    [
        '@@@@'
    ],
    [
        '.@.',
        '@@@',
        '.@.'
    ],
    [
        '..@',
        '..@',
        '@@@'
    ],
    [
        '@',
        '@',
        '@',
        '@'
    ],
    [
        '@@',
        '@@'
    ]
]

def merge(loffset, target, source):
    # First do a check
    for i in range(len(source)):
        if target[loffset + i] != '.':
            return False
    # Then do the merge if we can
    for i in range(len(source)):
        target[loffset + i] = source[i]
    return True

def rindex(l, find):
    for i in range(len(l) - 1, -1, -1):
        if l[i] == find:
            return i
    raise ValueError(l)

def rfind(l, find, max_idx = None):
    start = len(l) - 1 if max_idx is None else min(len(l) - 1, max_idx)
    for i in range(start, -1, -1):
        if l[i] == find:
            return i
    return -1

def lfind(l, find, min_idx = None):
    start = 0 if min_idx is None else min_idx
    for i in range(start, len(l)):
        if l[i] == find:
            return i
    return -1

def check_move(move, row):
    if move == '>':
        idx = rindex(row, '@')
        return idx < 6 and row[idx + 1] == '.'
    elif move == '<':
        idx = row.index('@')
        return idx > 0 and row[idx - 1] == '.'
    else:
        assert False, move

def do_move(move, row):
    if move == '>':
        max_idx = 1000
        while True:
            idx = rfind(row, '@', max_idx)
            if idx != -1:
                row[idx + 1] = '@'
            else:
                break
            max_idx = idx - 1
        row[max_idx + 1] = '.'
    elif move == '<':
        min_idx = 0
        while True:
            idx = lfind(row, '@', min_idx)
            if idx != -1:
                row[idx - 1] = '@'
            else:
                break
            min_idx = idx + 1
        row[min_idx - 1] = '.'
    else:
        assert False, move

def check_fall(row_idx, chamber):
    if row_idx == len(chamber) - 1:
        return False
    for i in range(0, 7):
        if chamber[row_idx][i] == '@' and chamber[row_idx + 1][i] == '#':
            return False
    return True

def do_fall(row_idx, chamber):
    for i in range(0, 7):
        if chamber[row_idx][i] == '@':
            chamber[row_idx + 1][i] = '@'
            chamber[row_idx][i] = '.'

def solidify(row):
    for i in range(len(row)):
        if row[i] == '@':
            row[i] = '#'

shape_iter = itertools.cycle(shapes)
highest = 0
chamber = []

shape_bottom = None
shape_height = None

need_shape = True

stop_count = 0

for move in itertools.cycle(moves):

    if need_shape:
        shape = next(shape_iter)
        # 3 units away from highest
        # grow chamber upwards to make space
        while highest < len(shape) + 3:
            chamber.insert(0, list('.' * 7))
            highest += 1

        ins = highest - 4
        shape_height = len(shape)
        shape_bottom = ins
        for i in range(len(shape) - 1, -1, -1):
            assert merge(2, chamber[ins], shape[i])
            ins -= 1
        need_shape = False

    can_move = True
    for i in range(shape_bottom, shape_bottom - shape_height, -1):
        if not check_move(move, chamber[i]):
            can_move = False
            break

    if can_move:
        for i in range(shape_bottom, shape_bottom - shape_height, -1):
            do_move(move, chamber[i])

    can_fall = True
    for i in range(shape_bottom, shape_bottom - shape_height, -1):
        if not check_fall(i, chamber):
            can_fall = False
            break

    if can_fall:
        for i in range(shape_bottom, shape_bottom - shape_height, -1):
            do_fall(i, chamber)
        shape_bottom += 1
    else:
        for i in range(shape_bottom, shape_bottom - shape_height, -1):
            solidify(chamber[i])
        stop_count += 1
        need_shape = True
        # highest is the index of the top of the shape, so -1 the height
        highest = min(highest, shape_bottom - (shape_height - 1))

    if stop_count == 2022:
        break

print(len(chamber) - highest)

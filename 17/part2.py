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
    is_full = True
    for i in range(len(row)):
        if row[i] == '@':
            row[i] = '#'
        if is_full and row[i] != '#':
            is_full = False
    return is_full

def run_simulation(callback):
    shape_idx = 0
    highest = 0
    chamber = []
    shape_bottom = None
    shape_height = None
    need_shape = True
    stop_count = 0

    for move in itertools.cycle(moves):

        if need_shape:
            shape = shapes[shape_idx]
            shape_idx = (shape_idx + 1) % len(shapes)
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
                is_full = solidify(chamber[i])
            stop_count += 1
            need_shape = True
            # highest is the index of the top of the shape, so -1 the height
            shape_top = shape_bottom - (shape_height - 1)
            highest = min(highest, shape_top)
            is_flat = is_full and highest == shape_top
            height = len(chamber) - highest
            if callback(is_flat, stop_count, height, shape_idx):
                break

known_shape_cycle = None
seen_shape_flat = set()
def discover_shape(is_flat, stop_count, height, shape_idx):
    global known_shape_cycle
    if is_flat:
        if shape_idx in seen_shape_flat:
            known_shape_cycle = shape_idx
            return True
        seen_shape_flat.add(shape_idx)
    return False

run_simulation(discover_shape)

offset_height = None
offset_count = None
prev_height = None
prev_count = None
seen_delta = set()
def discover_period(is_flat, stop_count, height, shape_idx):
    global offset_height, offset_count, prev_height, prev_count
    if is_flat and shape_idx == known_shape_cycle:
        if offset_height is None:
            offset_height = height
            offset_count = stop_count
        else:
            delta = (height - prev_height, stop_count - prev_count)
            if delta in seen_delta:
                return True
            seen_delta.add(delta)
        prev_height = height
        prev_count = stop_count
    return False

run_simulation(discover_period)
period_height = sum(d[0] for d in seen_delta)
period_count = sum(d[1] for d in seen_delta)

# Subtract offset, we add it's height back at the end
num_stopped = 1000000000000 - offset_count
# get the number of times we repeat the period
# tail is the remainder offset
period_times, tail = divmod(num_stopped, period_count)

# Measure the height of "tail" counts, starting from the offset
stop_at_count = tail
tail_height = None
def measure_height_at_count_offset(is_flat, stop_count, height, shape_idx):
    global tail_height
    if stop_count - offset_count == stop_at_count:
        tail_height = height - offset_height
        return True
    return False

run_simulation(measure_height_at_count_offset)
# Trail height is initial offset height + final tail height
trail_height = tail_height + offset_height

# Finally, multiply the period height by number of times needed
# and add the trail height
print((period_times * period_height) + trail_height)

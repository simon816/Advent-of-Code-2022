import sys

cubes = set()

min_x, min_y, min_z = None, None, None
max_x, max_y, max_z = None, None, None

for line in sys.stdin.readlines():
    line = line.strip()
    x, y, z = cube = tuple(map(int, line.split(',')))
    cubes.add(cube)
    if min_x is None:
        min_x, min_y, min_z = x, y, z
        max_x, max_y, max_z = x, y, z
    else:
        min_x, min_y, min_z = min(x, min_x), min(y, min_y), min(z, min_z)
        max_x, max_y, max_z = max(x, max_x), max(y, max_y), max(z, max_z)

def get_adj(x, y, z):
    yield (x - 1, y, z)
    yield (x, y - 1, z)
    yield (x, y, z - 1)
    yield (x + 1, y, z)
    yield (x, y + 1, z)
    yield (x, y, z + 1)

external = set()
internal = set()

import queue

def is_external(node):
    all_nodes = set()
    search = queue.Queue()
    search.put(node)
    while not search.empty():
        node = search.get()
        if node in external:
            external.update(all_nodes)
            return True
        if node in internal:
            internal.update(all_nodes)
            return False
        all_nodes.add(node)
        x, y, z = node
        if x < min_x or x > max_x \
           or y < min_y or y > max_y \
           or z < min_z or z > max_z:
            external.update(all_nodes)
            return True
        for adj in get_adj(x, y, z):
            if adj not in cubes and adj not in all_nodes:
                search.put(adj)
                all_nodes.add(adj)
    internal.update(all_nodes)
    return False

t = 0
for (x, y, z) in cubes:
    for adj in get_adj(x, y, z):
        if adj not in cubes:
            if is_external(adj):
                t += 1
print(t)

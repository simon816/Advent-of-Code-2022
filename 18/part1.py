import sys

cubes = set()

for line in sys.stdin.readlines():
    line = line.strip()
    cube = tuple(map(int, line.split(',')))
    cubes.add(cube)

t = 0

for (x, y, z) in cubes:
    faces = 6
    if (x - 1, y, z) in cubes:
        faces -= 1
    if (x, y - 1, z) in cubes:
        faces -= 1
    if (x, y, z - 1) in cubes:
        faces -= 1
    if (x + 1, y, z) in cubes:
        faces -= 1
    if (x, y + 1, z) in cubes:
        faces -= 1
    if (x, y, z + 1) in cubes:
        faces -= 1
    t += faces

print(t)

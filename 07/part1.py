import sys
import os

commands = []
cmd = None
args = []
output = []

for line in sys.stdin.readlines():
    line = line.strip()
    if line.startswith('$'):
        if cmd:
            commands.append((cmd, args, output))
        _, cmd, *args = line.split(' ')
        output = []
    else:
        output.append(line)

commands.append((cmd, args, output))

tree = {}
sizes = {}
parents = {}
cwd = '/'
for (cmd, args, output) in commands:
    if cmd == 'cd':
        cwd = os.path.normpath(os.path.join(cwd, args[0]))
    elif cmd == 'ls':
        size = 0
        tree[cwd] = []
        for file in output:
            a, b = file.split(' ')
            if a == 'dir':
                path = os.path.normpath(os.path.join(cwd, b))
                parents[path] = cwd
                tree[cwd].append(path)
            else:
                size += int(a)
        sizes[cwd] = size

def get_size(path):
    size = sizes[path]
    for subpath in tree[path]:
        size += get_size(subpath)
    return size

total = 0
for path in sizes.keys():
    size = get_size(path)
    if size <= 100000:
        total += size

print(total)

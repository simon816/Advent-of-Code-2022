import sys

stacks = []

read_stacks = True

commands = []

for line in sys.stdin.readlines():
    if read_stacks:
        line = list(line.strip('\n'))
        if not line:
            read_stacks = False
            continue
        for i in range(0, len(line), 4):
            stack_num = i // 4
            while len(stacks) - 1 < stack_num:
                stacks.append([])
            val = line[i + 1]
            if val != ' ':
                stacks[stack_num].append(val)
    else:
        _, count, _, src, _, dest = line.split(' ')
        count, src, dest = int(count), int(src), int(dest)
        commands.append((count, src, dest))

        

stack_by_id = {}
for stack in stacks:
    stack_id = int(stack.pop())
    stack.reverse()
    stack_by_id[stack_id] = stack

for (count, src, dest) in commands:
    move = []
    for _ in range(count):
        move.append(stack_by_id[src].pop())
    move.reverse()
    stack_by_id[dest].extend(move)

print(''.join(stack_by_id[k][-1] for k in sorted(stack_by_id.keys())))

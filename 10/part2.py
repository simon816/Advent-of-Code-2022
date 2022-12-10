import sys

reg_x = 1

display = [[]]

cycles = 0

def draw():
    cur_line = display[-1]
    pos = len(cur_line)
    if reg_x == pos or abs(pos - reg_x) == 1:
        cur_line.append('#')
    else:
        cur_line.append('.')
    if cycles % 40 == 0:
        display.append([])

for line in sys.stdin.readlines():
    cmd, *args = line.strip().split(' ')
    if cmd == 'noop':
        cycles += 1
        draw()
    elif cmd == 'addx':
        v = int(args[0])
        cycles += 1
        draw()
        cycles += 1
        draw()
        reg_x += v

for line in display:
    print(''.join(line))

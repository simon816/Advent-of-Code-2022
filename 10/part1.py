import sys

reg_x = 1

cycles = 0

sum = 0

want_cycles = set((20, 60, 100, 140, 180, 220))

for line in sys.stdin.readlines():
    cmd, *args = line.strip().split(' ')
    if cmd == 'noop':
        cycles += 1
        if cycles in want_cycles:
            strength = cycles * reg_x
            sum += strength
    elif cmd == 'addx':
        v = int(args[0])
        cycles += 1
        if cycles in want_cycles:
            strength = cycles * reg_x
            sum += strength
        cycles += 1
        if cycles in want_cycles:
            strength = cycles * reg_x
            sum += strength
        reg_x += v

print(sum)

import sys

monkeys = {}

curr = None

for line in sys.stdin.readlines():
    line = line.strip()
    if line.startswith('Monkey'):
        curr = int(line.split(' ')[1].split(':')[0])
        monkeys[curr] = {'count': 0}
    elif line:
        k, v = line.split(':')
        if k == 'Starting items':
            v = [int(i) for i in v.split(', ')]
            k = 'items'
        elif k == 'Test':
            assert v.startswith(' divisible by ')
            v = int(v[len(' divisible by '):])
            k = 'test'
        elif k.startswith('If '):
            k = k[3:].lower()
            assert v.startswith(' throw to monkey ')
            v = int(v[len(' throw to monkey '):])
        elif k == 'Operation':
            assert v.startswith(' new = old ')
            k = 'op'
            v = v[len(' new = old '):].split(' ')
            if v[1].isdigit():
                v[1] = int(v[1])
        monkeys[curr][k] = v

def do_op(op, val):
    op, right = op
    if right == 'old':
        right = val
    if op == '*':
        return val * right
    elif op == '+':
        return val + right
    else:
        assert False

for _ in range(20):
    for m in range(0, len(monkeys)):
        curr = monkeys[m]
        l = curr['items']
        curr['items'] = []
        curr['count'] += len(l)
        for worry in l:
            worry = do_op(curr['op'], worry)
            worry //= 3
            if worry % curr['test'] == 0:
                monkeys[curr['true']]['items'].append(worry)
            else:
                monkeys[curr['false']]['items'].append(worry)

counts = [m['count'] for m in monkeys.values()]
counts = sorted(counts)
print(counts[-1] * counts[-2])

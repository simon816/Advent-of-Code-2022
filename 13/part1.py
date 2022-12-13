import sys

groups = []

group = []

for line in sys.stdin.readlines():
    line = line.strip()
    if not line:
        groups.append(group)
        group = []
        continue
    stack = []
    acc = None
    acc_type = None
    for c in line:
        if c == '[':
            stack.append([])
        elif c.isdigit():
            if acc_type is None:
                acc_type = 'int'
                acc = c
            elif acc_type == 'int':
                acc += c
            else:
                assert False, acc_type
        elif c == ',':
            if acc_type == 'int':
                val = int(acc)
            elif acc_type == 'list':
                val = acc
            else:
                assert False, acc_type
            stack[-1].append(val)
            acc = None
            acc_type = None
        elif c == ']':
            if acc_type is not None:
                if acc_type == 'int':
                    val = int(acc)
                elif acc_type == 'list':
                    val = acc
                stack[-1].append(val)
            acc_type = 'list'
            acc = stack.pop()
    group.append(acc)

groups.append(group)

def cmp(a, b):
    return (a > b) - (a < b) 

def compare(left, right):
    if type(left) == int and type(right) == list:
        left = [left]
    elif type(right) == int and type(left) == list:
        right = [right]

    if type(left) == int:
        return cmp(left, right)

    for i in range(min(len(left), len(right))):
        result = compare(left[i], right[i])
        if result != 0:
            return result
    return cmp(len(left), len(right))

i = 1
s = 0
for pair in groups:
    assert len(pair) == 2
    if compare(*pair) == -1:
        s += i
    i += 1
print(s)

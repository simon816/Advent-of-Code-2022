import sys
import functools

mapping = {}

for line in sys.stdin.readlines():
    name, expr = line.strip().split(': ')
    mapping[name] = int(expr) if expr.isdigit() else expr


@functools.lru_cache(maxsize=None)
def get_value(name):
    v = mapping[name]
    if type(v) == int:
        return v
    left, op, right = v.split(' ')
    left = get_value(left)
    right = get_value(right)
    if op == '+':
        return left + right
    if op == '*':
        return left * right
    if op == '-':
        return left - right
    if op == '/':
        return left // right

print(get_value('root'))

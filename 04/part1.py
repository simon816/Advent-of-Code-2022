from collections import namedtuple
import sys

Range = namedtuple('Range', 'min max')

def mkrange(s):
    return Range(*map(int, s.split('-')))

def contains(range, check):
    return check.min >= range.min and check.max <= range.max

count = 0
for line in sys.stdin.readlines():
    line = line.strip()
    first, second = tuple(map(mkrange, line.split(',')))
    if contains(first, second) or contains(second, first):
        count += 1
print(count)

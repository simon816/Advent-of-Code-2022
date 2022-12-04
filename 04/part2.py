from collections import namedtuple
import sys

Range = namedtuple('Range', 'min max')

def mkrange(s):
    return Range(*map(int, s.split('-')))

def overlaps(r1, r2):
    return r1.max >= r2.min and r1.min <= r2.max or \
           r2.max >= r1.min and r2.min <= r1.max

count = 0
for line in sys.stdin.readlines():
    line = line.strip()
    first, second = tuple(map(mkrange, line.split(',')))
    if overlaps(first, second):
        count += 1
print(count)

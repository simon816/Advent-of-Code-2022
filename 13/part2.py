#!/usr/bin/env python2

# PYTHON2!!

import sys

packets = [
    [[2]],
    [[6]]
]

for line in sys.stdin.readlines():
    line = line.strip()
    if not line:
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
    packets.append(acc)

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

class Packet(object):

    def __init__(self, val):
        self.val = val

    def __cmp__(self, other):
        if isinstance(other, Packet):
            return compare(self.val, other.val)
        assert False

packets = sorted(list(map(Packet, packets)))

key = 1
for i, p in enumerate(packets):
    if p.val in ([[2]], [[6]]):
        key *= i + 1
print(key)

import sys

numbers = [int(n) * 811589153 for n in sys.stdin.readlines()]

class Node:

    def __init__(self, val, id):
        self.id = id
        self.val = val
        self.next = None
        self.prev = None

    def __repr__(self):
        return 'Node(%d, %d)' % (self.id, self.val)

    def list(self):
        l = [self.val]
        next = self.next
        while next != self:
            l.append(next.val)
            next = next.next
        return l

first = prev = Node(numbers[0], 0)
id_node_map = { 0: first }
for i in range(1, len(numbers)):
    node = Node(numbers[i], i)
    id_node_map[i] = node
    prev.next = node
    node.prev = prev
    prev = node
prev.next = first
first.prev = prev

for _ in range(10):
    for i in range(len(numbers)):
        v = numbers[i]
        n = abs(v)
        n = n % (len(numbers) - 1)
        node = id_node_map[i]
        if v < 0:
            for _ in range(n):
                next = node.next
                prev = node.prev
                node.prev = prev.prev
                prev.prev.next = node
                node.next = prev
                prev.prev = node
                prev.next = next
                next.prev = prev
        elif v > 0:
            for _ in range(n):
                next = node.next
                prev = node.prev
                node.prev = next
                node.next = next.next
                next.next.prev = node
                prev.next = next
                next.prev = prev
                next.next = node

newlist = first.list()
zero = newlist.index(0)
print(sum((newlist[(zero + 1000) % len(newlist)],
      newlist[(zero + 2000) % len(newlist)],
      newlist[(zero + 3000) % len(newlist)])))

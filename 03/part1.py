import sys

sum = 0

for line in sys.stdin.readlines():
    line = line.strip()
    half = len(line) // 2
    first, second = set(line[:half]), set(line[half:])
    intersection = first & second
    for l in intersection:
        if l.isupper():
            pri = (ord(l) - ord('A')) + 27
        else:
            pri = (ord(l) - ord('a')) + 1
        sum += pri
print(sum)

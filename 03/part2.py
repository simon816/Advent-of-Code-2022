import sys

groups = []

counter = 2

for line in sys.stdin.readlines():
    line = line.strip()
    items = set(line)
    if counter == 2:
        groups.append(items)
        counter = 0    
    else:
        groups[-1] &= items
        counter += 1

sum = 0
for group in groups:
    for l in group:
        if l.isupper():
            pri = (ord(l) - ord('A')) + 27
        else:
            pri = (ord(l) - ord('a')) + 1
        sum += pri
print(sum)

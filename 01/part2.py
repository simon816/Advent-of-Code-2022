import sys
from collections import Counter

if __name__ == '__main__':
    count = Counter()
    id = 0
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            id += 1
            continue
        count[id] += int(line)
    print(sum([v for k, v in count.most_common(3)]))


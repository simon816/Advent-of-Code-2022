import sys

if __name__ == '__main__':
    max = 0
    total = 0
    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            if total > max:
                max = total
            total = 0
            continue
        total += int(line)
    print(max)


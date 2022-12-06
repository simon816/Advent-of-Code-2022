import sys

input = sys.stdin.read().strip()

for i in range(14, len(input)):
    if len(set(input[i - 14:i])) == 14:
        print(i)
        break

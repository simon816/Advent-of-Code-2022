import sys

input = sys.stdin.read().strip()

for i in range(4, len(input)):
    if len(set(input[i - 4:i])) == 4:
        print(i)
        break

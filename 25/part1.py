import sys

s = 0

for line in sys.stdin.readlines():
    num = line.strip()
    val = 0
    place = 1
    for i in range(len(num) - 1, -1, -1):
        if num[i] == '=':
            n = -2
        elif num[i] == '-':
            n = -1
        else:
            n = int(num[i])
        val += n * place
        place *= 5
    s += val

n = ''

while s:
    s, v = divmod(s, 5)
    if v == 3:
        s += 1
        n = '=' + n
    elif v == 4:
        s += 1
        n = '-' + n
    else:
        n = str(v) + n

print(n)

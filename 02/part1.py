import sys

mapping = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors'
}

score = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}

def winner(a, b):
    if a == b:
        return 0
    if a == 'rock':
        return 1 if b == 'scissors' else 2
    if a == 'paper':
        return 1 if b == 'rock' else 2
    if a == 'scissors':
        return 1 if b == 'paper' else 2

me_score = 0
opp_score = 0

for line in sys.stdin.readlines():
    if not line.strip():
        break
    opp, me = line.strip().split(' ')
    opp = mapping[opp]
    me = mapping[me]
    win = winner(opp, me)
    opp_score += score[opp]
    me_score += score[me]
    if win == 0:
        me_score += 3
        opp_score += 3
    elif win == 1:
        opp_score += 6
    elif win == 2:
        me_score += 6

print(me_score)

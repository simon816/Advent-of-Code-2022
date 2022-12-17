import sys
import functools

adj = {}
rates = {}

for line in sys.stdin.readlines():
    line = line.strip()
    l, r = line.split(';')
    valve = l[len('Valve '):l.index(' has flow')]
    rate = int(l[l.index('=') + 1:])
    if r.find('tunnels') != -1:
        tunnels = r[len(' tunnels lead to valves '):].split(', ')
    else:
        tunnels = r[len(' tunnel leads to valve '):].split(', ')
    adj[valve] = tunnels
    rates[valve] = rate

@functools.lru_cache(maxsize=None)
def max_value(node, time, openset):
    if node not in openset:
        v = rates[node] * (time - 1)
    else:
        v = 0
    max_val = 0
    # If the valve is not open and has a rate, we can either
    # not open it for a cost of 1, or open it for a cost of 2
    # Find the best option
    if v > 0:
        adj_max = 0
        new_set = frozenset((*openset, node))
        if time > 1:
            for a in adj[node]:
                adj_max = max(adj_max, max_value(a, time - 2, new_set))
        max_val = v + adj_max
    if time > 1:
        adj_max = 0
        for a in adj[node]:
            adj_max = max(adj_max, max_value(a, time - 1, openset))
        max_val = max(adj_max, max_val)
    return max_val

print(max_value('AA', 30, frozenset()))

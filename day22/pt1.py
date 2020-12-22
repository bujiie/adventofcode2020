#!/usr/bin/env python3

import sys

filename=sys.argv[1]

p1 = []
p2 = []
p = []
with open(filename) as fp:
    for index, line in enumerate(fp):
        line = line.strip()
        if line.startswith('Player 1'):
            p = p1
            continue
        elif line.startswith('Player 2'):
            p = p2
            continue
        elif len(line) == 0:
            continue

        p.append(int(line))

while len(p1) > 0 and len(p2) > 0:
    c1 = p1.pop(0)
    c2 = p2.pop(0)

    if c1 > c2:
        p1.append(c1)
        p1.append(c2)
    else:
        p2.append(c2)
        p2.append(c1)

p = p1 if len(p1) > 0 else p2

ans = 0
for i,c in enumerate(reversed(p)):
    ans += (c*(i+1))

print(ans)



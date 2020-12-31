#!/usr/bin/env python3

import sys

filename=sys.argv[1]

T = {}
E = {}

with open(filename) as fp:
    id = None
    for index, line in enumerate(fp):
        line = line.strip()

        if line.startswith('Tile'):
            id = line.split(' ')[1][:-1]
            T[id] = []
        elif len(line) == 0:
            id = None
        else:
            T[id].append(line)

for id in T:
    # Top, Right, Bottom, Left
    E[id] = []
    left = ''
    right = ''
    for i, row in enumerate(T[id]):
        if i == 0:
            E[id].append(row)
        left += row[0]
        right += row[-1]
        if i == len(T[id])-1:
            E[id].append(right)
            E[id].append(row)
            E[id].append(left)

NM = []

for id in E:
    target_edges = E[id]
    for edge in target_edges:
        matched = False

        for id2 in E:
            if id == id2:
                continue

            check_edges = E[id2]
            for edge2 in check_edges:
                reverse = False
                if edge == edge2 or edge == edge2[::-1]:
                    matched = True
                    break

            if matched:
                break

        if not matched:
            NM.append((id, edge))
            matched = False

CNM = {}
for n in NM:
    key, edge = n
    if key not in CNM:
        CNM[key] = 1
    else:
        CNM[key] += 1

ans = 1
corners = 0
edges = 0
for key in CNM:
    if CNM[key] == 1:
        edges += 1
    if CNM[key] == 2:
        corners += 1
        ans *= int(key)

print(NM)
print('corners=',corners,'edges=',edges)
print(ans)



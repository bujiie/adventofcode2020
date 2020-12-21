#!/usr/bin/env python3

import sys
from collections import deque

filename=sys.argv[1]

T = {}
E = {}

def rotate(frame, n = 1):
    # assume we read all frames top->bottom, left-> right
    frame.rotate(n)
    return [f[::-1] for f in frame if n%2 == 0]

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
    E[id] = deque()

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
print(E)

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
        CNM[key] = [edge]
    else:
        CNM[key].append(edge)

CM = {}

for key in CNM:
    if len(CNM[key]) == 2:
        for edge in CNM[key]:
            if key not in CM:
                CM[key] = {}

            loc = E[key].index(edge)
            print(key, loc, edge)
            if loc == 0:
                CM[key]['T'] = edge
            elif loc == 1:
                CM[key]['R'] = edge
            elif loc == 2:
                CM[key]['B'] = edge
            elif loc == 3:
                CM[key]['L'] = edge

print('')
print(CM)

# print(CNM)



#!/usr/bin/env python3

import sys
from collections import deque
import pprint
from copy import deepcopy
import math

filename=sys.argv[1]

T = {}
E = {}

def rotate(frame, n = 1):
    # assume we read all frames top->bottom, left-> right
    frame.rotate(n)
    return [f[::-1] for f in frame if n%2 == 0]


def edge_sides_for_matching(frame, edge_side):
    # if bound edge is the LEFT, as we move counter clockwise
    # the indices will reset back to 0. Easier to just
    # hardcode this boundary condition
    if edge_side == 3:
        return [frame[2],frame[0]]
    else:
        return [frame[i] for i in [-1,1]]


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

BORDER = {}
corners = {}

# Find all the corner pieces and indicate which edges are unmatched.
# Top (0), Right (1), Bottom (2), Left (3)
for key in CNM:
    sides = []
    for edge in CNM[key]:
        if key not in BORDER:
            BORDER[key] = {}

        loc = E[key].index(edge)
        if loc == 0:
            BORDER[key]['T'] = edge
            sides.append('T')
        elif loc == 1:
            BORDER[key]['R'] = edge
            sides.append('R')
        elif loc == 2:
            BORDER[key]['B'] = edge
            sides.append('B')
        elif loc == 3:
            BORDER[key]['L'] = edge
            sides.append('L')
    sides = sorted(sides)
    if 'T' in sides:
        sides = reversed(sides)
    sides = tuple(sides)

    if len(CNM[key]) == 2:
        if sides not in corners:
            corners[sides] = []
        corners[sides].append(key)

# print(corners)

def frame(number, rot = 0):
    if rot % 360 == 0:
        return E[number]
    return rotate(E[number], int((rot/90) % 4))

# ('T','L'),('T','R'),('B','R'),('B','L')

dimension = math.floor(math.sqrt(len(T)))
# IMPORTANT: deepcopy() required otherewise you're creating a list with
# references to the same single nested list. Updating one nested list will show
# up in each nested list.
G = [deepcopy([0 for x in range(dimension)]) for y in range(dimension)]

# Manually set corners for now since there are not that many combinations
# {('B', 'R'): ['2801', '2719'], ('B', 'L'): ['3823', '1759']}
# Top, Left
G[0][0] = ('1759', 90)
# Top, Right
G[0][-1] = ('2719', 270)
# Bottom, Left
G[-1][0] = ('3823', 0)
# Bottom, Right
G[-1][-1] = ('2801', 0)

for key in BORDER:
    if len(BORDER[key]) > 1:
        continue


print(CNM)
# print(G)


# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(BORDER)




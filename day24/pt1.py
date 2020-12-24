#!/usr/bin/env python3

import sys
import re
from copy import deepcopy

filename=sys.argv[1]

S = []
directions = {
    'e': (2, 0),
    'se': (1, -1),
    'sw': (-1, -1),
    'w': (-2, 0),
    'nw': (-1, 1),
    'ne': (1, 1)
}

with open(filename) as fp:
    for index, line in enumerate(fp):
        line = line.strip()
        S.append(re.findall(r'(e|se|sw|w|nw|ne)', line))

Floor = []

dimension = 100
for x in range(dimension):
    row = []
    for y in range(dimension):
        if (x+y) % 2 == 0:
            row.append('w')
        else:
            row.append('.')
    Floor.append(row)

def flip_tile(seq = [], loc = (0, 0)):
    if len(seq) == 0:
        return loc

    top = seq[0]
    diff = directions[top]
    return flip_tile(seq[1:], (loc[0]+diff[0], loc[1]+diff[1]))

for seq in S:
    x, y = flip_tile(seq, (0, 0))
    # print("flip=",x,y)
    if Floor[x][y] == 'w':
        Floor[x][y] = 'b'
    elif Floor[x][y] == 'b':
        Floor[x][y] = 'w'

ans = 0
for x in range(dimension):
    for y in range(dimension):
        if Floor[x][y] == 'b':
            ans += 1

print(ans)

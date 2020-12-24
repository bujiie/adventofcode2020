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

FM = {}

def flip_tile(seq = [], loc = (0, 0)):
    if len(seq) == 0:
        return loc

    top = seq[0]
    diff = directions[top]
    return flip_tile(seq[1:], (loc[0]+diff[0], loc[1]+diff[1]))

def flip_tile_conditional(loc = (0, 0), fm = {}):
    x,y = loc

    neighbor_b = 0
    for diff in directions.values():
        dx, dy = diff
        xx = x + dx
        yy = y + dy
        if (xx,yy) in fm and fm[(xx,yy)] == 'b':
            neighbor_b += 1

    if fm[loc] == 'b' and neighbor_b not in [1,2]:
        return (loc, 'w')
    if fm[loc] == 'w' and neighbor_b == 2:
        return (loc, 'b')
    return None

def count_black_tiles(fm = {}):
    return sum(v == 'b' for v in fm.values())

for seq in S:
    loc = flip_tile(seq, (0,0))
    if loc not in FM:
        FM[loc] = 'b'
    elif FM[loc] == 'b':
        FM[loc] = 'w'
    elif FM[loc] == 'w':
        FM[loc] = 'b'
    x, y = loc
    for diff in directions.values():
        dx, dy = diff
        xx = x + dx
        yy = y + dy
        if (xx,yy) not in FM:
            FM[(xx,yy)] = 'w'

days = 100
F = deepcopy(FM)
count_flag = False

for i in range(days):
    F_copy = deepcopy(F)

    for loc in F.keys():
        flip = flip_tile_conditional(loc, F)
        if not flip:
            continue
        f_loc, c = flip
        F_copy[f_loc] = c

        x,y = f_loc
        for diff in directions.values():
            dx, dy = diff
            xx = x + dx
            yy = y + dy
            if (xx,yy) not in F_copy:
                F_copy[(xx,yy)] = 'w'

    if count_flag:
        ans = count_black_tiles(F_copy)
        print(f"Day {i+1}: {ans}")
    F = F_copy

print(count_black_tiles(F))


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
    if n % 2 == 0:
        return [f[::-1] for f in frame]
    return frame

# rot should be increments of 90deg. Function will round up to the closest
# 90deg increment. rot MUST be in the positive CW direction (90deg CCW should
# be 270deg)
# Also assumes frame is square.
def rotate_frame(frame, rot=90):
    rot_as_index = int(math.ceil((rot/90)) % 4)
    dimension = len(frame)
    for k in range(rot_as_index):
        new_frame = []
        for j in range(dimension):
            new_layer = []
            for i in reversed(range(dimension)):
                new_layer.append(frame[i][j])
            new_frame.append(''.join(new_layer))
        frame = new_frame
    return frame

def flip_frame(frame):
    for i in len(frame):
        frame[i] = frame[i][::-1]
    return frame

def get_frame(frame_number):
    if frame_number in T:
        return T[frame_number]
    return None

def get_edge(frame, side = 'T'):
    if side == 'T':
        return frame[0]
    elif side == 'B':
        return frame[-1]
    elif side == 'L':
        edge = []
        for i in range(len(frame)):
            edge.append(frame[i][0])
        return ''.join(edge)
    elif side == 'R':
        edge = []
        for i in range(len(frame)):
            edge.append(frame[i][-1])
        return ''.join(edge)


def get_index_for_side(side):
    sides = {'T': 0, 'R': 1, 'B': 2, 'L': 3}
    if side in sides:
        return sides[side]
    return -1

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


def get_frame2(number, rot = 0):
    if rot % 360 == 0:
        return E[number]
    return rotate(E[number], int((rot/90) % 4))

def get_frame_edge(number, side):
    side_index = get_side_index(side)
    return T[number][side_index]

def rotate_frame2(frame, rot):
    return rotate(frame, int((rot/90) % 4))

def lock_frame(frame_number, lock_edge, side):
    frame = E[frame_number]
    lock_me = -1
    for i,edge in enumerate(frame):
        if edge == lock_edge:
            lock_me = i
            break
    lock_to = get_side_index(side)
    rot = get_rotate(lock_me, lock_to)
    return (rotate_frame2(frame, rot), rot)

def get_rotate(start_side, target_side):
    sides = deque(list(range(0,4)))
    sides.rotate(-(start_side+1))
    return (sides.index(target_side)+1)*90


def get_side_index(side):
    sides = {'T': 0, 'R': 1, 'B': 2, 'L': 3}
    return sides[side]


# ('T','L'),('T','R'),('B','R'),('B','L')

dimension = math.floor(math.sqrt(len(T)))
# IMPORTANT: deepcopy() required otherewise you're creating a list with
# references to the same single nested list. Updating one nested list will show
# up in each nested list.
G = [deepcopy([None for x in range(dimension)]) for y in range(dimension)]

# Manually set corners for now since there are not that many combinations
# {('B', 'R'): ['2801', '2719'], ('B', 'L'): ['3823', '1759']}
# # Top, Left
# G[0][0] = ('1759', 90)
# # Top, Right
# G[0][-1] = ('2719', 270)
# # Bottom, Left
# G[-1][0] = ('3823', 0)
# # Bottom, Right
# G[-1][-1] = ('2801', 0)

# {('B', 'L'): ['1951', '1171'], ('T', 'L'): ['2971'], ('T', 'R'): ['3079']}
# Top, Left
G[0][0] = ('2971', 0)
# Top, Right
G[0][-1] = ('3079', 0)
# Bottom, Left
G[-1][0] = ('1951', 0)
# Bottom, Right
G[-1][-1] = ('1171', 90)

edges = []
for key in BORDER:
    if len(BORDER[key]) > 1:
        continue
    edges.append((key, BORDER[key]))

used = []
GNO ={}

for x in range(dimension):
    for y in range(dimension):
        if x not in [0,dimension-1] and y in [1, dimension-2]:
            # only care about the top/bottom rows and the edge pieces going
            # down the side of the frame
            continue

        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx != dy and not (dx == 1 and dy == -1) and not (dx == -1 and dy == 1):
                    xx = x + dx
                    yy = y + dy
                    if 0 <= xx < dimension and 0 <= yy < dimension:
                        if G[xx][yy] == None:
                            break

                        (f_number, r) = G[xx][yy]
                        f = rotate_frame(get_frame(f_number), r)

                        found_rot = None
                        found_key = None

                        for key in T:
                            if key in ['2971','3079','1951','1171'] and key not in used:
                                continue

                            frame = get_frame(key)
                            for rot in [0, 90, 180, 270]:
                                frame = rotate_frame(frame, rot)
                                left_edge = get_edge(frame, 'L')
                                right_edge = get_edge(frame, 'R')
                                top_edge = get_edge(frame, 'T')
                                bottom_edge = get_edge(frame, 'B')

                                if dx == 0:
                                    if dy == -1:
                                        if left_edge == get_edge(f, 'R'):
                                            found_rot = rot
                                            break
                                    else:
                                        if right_edge == get_edge(f, 'L'):
                                            found_rot = rot
                                            break
                                elif dy == 0:
                                    if dx == -1:
                                        if bottom_edge == get_edge(f, 'T'):
                                            found_rot = rot
                                            break
                                    else:
                                        if top_edge == get_edge(f, 'B'):
                                            found_rot = rot
                                            break
                            if found_rot != None:
                                found_key = key
                                break
                            else:
                                GNO[x][y].append(key)


frame_dimension = -1
for key in E:
    frame_dimension = len(T[key])
    break

def print_grid(grid, empty_char='o'):
    dimension = len(grid)
    for i in range(dimension):
        for k in range(frame_dimension):
            line = []
            for j in range(dimension):
                if G[i][j] == None:
                    line.append(empty_char*frame_dimension)
                else:
                    frame_number, rot = G[i][j]
                    frame = rotate_frame(get_frame(frame_number), rot)
                    line.append(frame[k])
            print('\t'.join(line))
        print('\n')


print_grid(G, '-')
# print('')




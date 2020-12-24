#!/usr/bin/env python3

import sys
from collections import deque
import pprint
from copy import deepcopy
import math

filename=sys.argv[1]

Tiles = {}
Edges = {}

with open(filename) as fp:
    id = None
    for index, line in enumerate(fp):
        line = line.strip()

        if line.startswith('Tile'):
            id = line.split(' ')[1][:-1]
            Tiles[id] = []
        elif len(line) == 0:
            id = None
        else:
            Tiles[id].append(line)

# Compile all the edges for each tile
for id in Tiles:
    # Top, Right, Bottom, Left
    Edges[id] = []

    left_edge = ''
    right_edge = ''
    for i, row in enumerate(Tiles[id]):
        if i == 0:
            Edges[id].append(row)
        left_edge += row[0]
        right_edge += row[-1]

        if i == len(Tiles[id]) -1:
            Edges[id].append(right_edge)
            Edges[id].append(row)
            Edges[id].append(left_edge)


def get_tile(id, edges = []):
    if id in edges:
        return edges[id]
    return None

def rotate_tile(tile, rot=90):
    tile = deepcopy(tile)
    for _ in range(int(rot/90)):
        last = tile.pop()
        tile.insert(0, last)
        tile[0] = tile[0][::-1]
        tile[2] = tile[2][::-1]
    return tile

def flip_tile_horizontal(tile):
    tile = deepcopy(tile)
    tile[1], tile[3] = tile[3], tile[1]
    tile[0] = tile[0][::-1]
    tile[2] = tile[2][::-1]
    return tile

def flip_tile_vertical(tile):
    tile = deepcopy(tile)
    tile[0], tile[2] = tile[2], tile[0]
    tile[1] = tile[1][::-1]
    tile[3] = tile[3][::-1]
    return tile

def flip_tile(tile, direction='h'):
    if direction == 'h':
        return flip_tile_horizontal(tile)
    elif direction == 'v':
        return flip_tile_vertical(tile)

def get_tile_edge(tile, edge='T'):
    edge_to_index = {'T': 0, 'R': 1, 'B': 2, 'L': 3}
    if edge not in edge_to_index:
        return None
    return tile[edge_to_index[edge]]

def find_matching_tile_orientation(ctx_tile, target_edge, candidate):
    ctx_tile_edge = get_tile_edge(ctx_tile, target_edge)
    edge_pairs = {'T': 'B', 'B': 'T', 'L': 'R', 'R': 'L'}

    look_at_edge = edge_pairs[target_edge]
    for rot in [0, 90, 180, 270]:
        for flip in ['n','h','v']:
            xform_tile = rotate_tile(candidate, rot)
            if flip != 'n':
                xform_tile = flip_tile(xform_tile, flip)
            xform_tile_edge = get_tile_edge(xform_tile, look_at_edge)
            if ctx_tile_edge == xform_tile_edge:
                return (rot, flip)
    return None

# for edges
def print_tile(tile, empty_cell='x'):
    dimension = len(tile[0])
    print(tile[0])
    for x in range(1, dimension-1):
        print(tile[3][x], end='')
        print(empty_cell*(dimension-2), end='')
        print(tile[1][x])
    print(tile[2])


# def get_tile(id, tiles = []):
#     if id in tiles:
#         return tiles[id]
#     return None

# def rotate_tile(tile, rot=90):
#     new_tile = deepcopy(tile)
#     i = int(rot/90)

#     for _ in range(i):
#         intermediate_tile = []
#         for y in range(len(new_tile)):
#             line = ''
#             for x in reversed(range(len(new_tile))):
#                 line += new_tile[x][y]
#             intermediate_tile.append(line)
#         new_tile = intermediate_tile
#     return new_tile

# def flip_tile_horizontal(tile):
#     for x in range(len(tile)):
#         tile[x] = tile[x][::-1]
#     return tile

# def flip_tile_vertical(tile):
#     new_tile = []
#     for x in reversed(tile):
#         new_tile.append(x)
#     return new_tile

# def flip_tile(tile, direction='h'):
#     if direction == 'h':
#         return flip_tile_horizontal(tile)
#     elif direction == 'v':
#         return flip_tile_vertical(tile)

# def get_tile_edge(tile, edge='T'):
#     line = ''
#     if edge == 'T':
#         line = tile[0]
#     elif edge == 'B':
#         line = tile[-1]
#     elif edge == 'L':
#         for x in range(len(tile)):
#             line += tile[x][0]
#     elif edge == 'R':
#         for x in range(len(tile)):
#             line += tile[x][-1]
#     return line

# def find_tiles_match(tile, edge, candidate):
#     tile_edge = get_tile_edge(tile, edge)
#     matching_edges = {'T': 'B', 'B': 'T', 'L': 'R', 'R': 'L'}

#     look_at_edge = matching_edges[edge]
#     for rot in [0, 90, 180, 270]:
#         for flip in ['n','h','v']:
#             xform_tile = rotate_tile(candidate, rot)
#             if flip != 'n':
#                 xform_tile = flip_tile(xform_tile, flip)
#             xform_tile_edge = get_tile_edge(xform_tile, look_at_edge)
#             if tile_edge == xform_tile_edge:
#                 return (rot, flip)
#     return None

# def print_tile(tile):
#     for x in range(len(tile)):
#         print(tile[x])

G = [deepcopy([None for x in range(len(Tiles)+1)]) for y in range(len(Tiles)+1)]

edge1 = [
    '12345',
    '56789',
    '....9',
    '1....'
]

edge2 = [
    '1....',
    '.....',
    '5....',
    '12345'
]

print_tile(edge1)
print('')
print_tile(edge2)
print('')

rot, flip = find_matching_tile_orientation(edge1, 'T', edge2)
print('rot=',rot,'flip=',flip)

xform_tile = rotate_tile(edge2, rot)
if flip != 'n':
    xform_tile = flip_tile(xform_tile, flip)
print_tile(xform_tile)

# tile1 = [
#     '12345',
#     '....6',
#     '....7',
#     '....8',
#     '....9',
# ]

# tile2 = [
#     '1....',
#     '2....',
#     '3....',
#     '4....',
#     '5....'
# ]

# print_tile(tile1)
# print('')
# print_tile(tile2)
# print('')

# rot, flip = find_tiles_match(tile1, 'T', tile2)
# xform_tile = rotate_tile(tile2, rot)
# if flip != 'n':
#     xform_tile = flip_tile(xform_tile)

# print_tile(xform_tile)







# def edge_sides_for_matching(frame, edge_side):
#     # if bound edge is the LEFT, as we move counter clockwise
#     # the indices will reset back to 0. Easier to just
#     # hardcode this boundary condition
#     if edge_side == 3:
#         return [frame[2],frame[0]]
#     else:
#         return [frame[i] for i in [-1,1]]




# for id in T:
#     # Top, Right, Bottom, Left
#     E[id] = deque()

#     left = ''
#     right = ''
#     for i, row in enumerate(T[id]):
#         if i == 0:
#             E[id].append(row)
#         left += row[0]
#         right += row[-1]
#         if i == len(T[id])-1:
#             E[id].append(right)
#             E[id].append(row)
#             E[id].append(left)

# NM = []

# for id in E:
#     target_edges = E[id]
#     for edge in target_edges:
#         matched = False

#         for id2 in E:
#             if id == id2:
#                 continue

#             check_edges = E[id2]
#             for edge2 in check_edges:
#                 reverse = False
#                 if edge == edge2 or edge == edge2[::-1]:
#                     matched = True
#                     break

#             if matched:
#                 break

#         if not matched:
#             NM.append((id, edge))
#             matched = False


# CNM = {}
# for n in NM:
#     key, edge = n
#     if key not in CNM:
#         CNM[key] = [edge]
#     else:
#         CNM[key].append(edge)

# BORDER = {}
# corners = {}

# # Find all the corner pieces and indicate which edges are unmatched.
# # Top (0), Right (1), Bottom (2), Left (3)
# for key in CNM:
#     sides = []
#     for edge in CNM[key]:
#         if key not in BORDER:
#             BORDER[key] = {}

#         loc = E[key].index(edge)
#         if loc == 0:
#             BORDER[key]['T'] = edge
#             sides.append('T')
#         elif loc == 1:
#             BORDER[key]['R'] = edge
#             sides.append('R')
#         elif loc == 2:
#             BORDER[key]['B'] = edge
#             sides.append('B')
#         elif loc == 3:
#             BORDER[key]['L'] = edge
#             sides.append('L')
#     sides = sorted(sides)
#     if 'T' in sides:
#         sides = reversed(sides)
#     sides = tuple(sides)

#     if len(CNM[key]) == 2:
#         if sides not in corners:
#             corners[sides] = []
#         corners[sides].append(key)


# def get_frame2(number, rot = 0):
#     if rot % 360 == 0:
#         return E[number]
#     return rotate(E[number], int((rot/90) % 4))

# def get_frame_edge(number, side):
#     side_index = get_side_index(side)
#     return T[number][side_index]

# def rotate_frame2(frame, rot):
#     return rotate(frame, int((rot/90) % 4))

# def lock_frame(frame_number, lock_edge, side):
#     frame = E[frame_number]
#     lock_me = -1
#     for i,edge in enumerate(frame):
#         if edge == lock_edge:
#             lock_me = i
#             break
#     lock_to = get_side_index(side)
#     rot = get_rotate(lock_me, lock_to)
#     return (rotate_frame2(frame, rot), rot)

# def get_rotate(start_side, target_side):
#     sides = deque(list(range(0,4)))
#     sides.rotate(-(start_side+1))
#     return (sides.index(target_side)+1)*90


# def get_side_index(side):
#     sides = {'T': 0, 'R': 1, 'B': 2, 'L': 3}
#     return sides[side]


# # ('T','L'),('T','R'),('B','R'),('B','L')

# dimension = math.floor(math.sqrt(len(T)))
# # IMPORTANT: deepcopy() required otherewise you're creating a list with
# # references to the same single nested list. Updating one nested list will show
# # up in each nested list.
# G = [deepcopy([None for x in range(dimension)]) for y in range(dimension)]

# # Manually set corners for now since there are not that many combinations
# # {('B', 'R'): ['2801', '2719'], ('B', 'L'): ['3823', '1759']}
# # # Top, Left
# # G[0][0] = ('1759', 90)
# # # Top, Right
# # G[0][-1] = ('2719', 270)
# # # Bottom, Left
# # G[-1][0] = ('3823', 0)
# # # Bottom, Right
# # G[-1][-1] = ('2801', 0)

# # {('B', 'L'): ['1951', '1171'], ('T', 'L'): ['2971'], ('T', 'R'): ['3079']}
# # Top, Left
# G[0][0] = ('2971', 0)
# # Top, Right
# G[0][-1] = ('3079', 0)
# # Bottom, Left
# G[-1][0] = ('1951', 0)
# # Bottom, Right
# G[-1][-1] = ('1171', 90)

# edges = []
# for key in BORDER:
#     if len(BORDER[key]) > 1:
#         continue
#     edges.append((key, BORDER[key]))

# used = []
# GNO ={}

# for x in range(dimension):
#     for y in range(dimension):
#         if x not in [0,dimension-1] and y in [1, dimension-2]:
#             # only care about the top/bottom rows and the edge pieces going
#             # down the side of the frame
#             continue

#         for dx in [-1,0,1]:
#             for dy in [-1,0,1]:
#                 if dx != dy and not (dx == 1 and dy == -1) and not (dx == -1 and dy == 1):
#                     xx = x + dx
#                     yy = y + dy
#                     if 0 <= xx < dimension and 0 <= yy < dimension:
#                         if G[xx][yy] == None:
#                             break

#                         (f_number, r) = G[xx][yy]
#                         f = rotate_frame(get_frame(f_number), r)

#                         found_rot = None
#                         found_key = None

#                         for key in T:
#                             if key in ['2971','3079','1951','1171'] and key not in used:
#                                 continue

#                             frame = get_frame(key)
#                             for rot in [0, 90, 180, 270]:
#                                 frame = rotate_frame(frame, rot)
#                                 left_edge = get_edge(frame, 'L')
#                                 right_edge = get_edge(frame, 'R')
#                                 top_edge = get_edge(frame, 'T')
#                                 bottom_edge = get_edge(frame, 'B')

#                                 if dx == 0:
#                                     if dy == -1:
#                                         if left_edge == get_edge(f, 'R'):
#                                             found_rot = rot
#                                             break
#                                     else:
#                                         if right_edge == get_edge(f, 'L'):
#                                             found_rot = rot
#                                             break
#                                 elif dy == 0:
#                                     if dx == -1:
#                                         if bottom_edge == get_edge(f, 'T'):
#                                             found_rot = rot
#                                             break
#                                     else:
#                                         if top_edge == get_edge(f, 'B'):
#                                             found_rot = rot
#                                             break
#                             if found_rot != None:
#                                 found_key = key
#                                 break
#                             else:
#                                 GNO[x][y].append(key)


# frame_dimension = -1
# for key in E:
#     frame_dimension = len(T[key])
#     break

# def print_grid(grid, empty_char='o'):
#     dimension = len(grid)
#     for i in range(dimension):
#         for k in range(frame_dimension):
#             line = []
#             for j in range(dimension):
#                 if G[i][j] == None:
#                     line.append(empty_char*frame_dimension)
#                 else:
#                     frame_number, rot = G[i][j]
#                     frame = rotate_frame(get_frame(frame_number), rot)
#                     line.append(frame[k])
#             print('\t'.join(line))
#         print('\n')


# print_grid(G, '-')
# # print('')




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


def get_tile(id, tiles = []):
    if id in tiles:
        return tiles[id]
    return None

def rotate_full_tile(tile, rot=90):
    tile = deepcopy(tile)
    dimension = len(tile)
    for _ in range(int(rot/90)):
        new_tile = []
        for y in range(dimension):
            line = ''
            for x in reversed(range(dimension)):
                line += tile[x][y]
            new_tile.append(line)
        tile = new_tile
    return tile

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

# for full tile
def print_full_tile(tile):
    for line in tile:
        print(line)


def get_permutations(tile):
    skip = [(180,'v'),(180,'h'),(270,'v'),(270,'h')]
    res = {}
    for rot in [0, 90, 180, 270]:
        for flip in ['n', 'v', 'h']:
            if (rot,flip) in skip:
                continue
            xform_tile = rotate_tile(tile, rot)
            if flip != 'n':
                xform_tile = flip_tile(xform_tile, flip)
            res[(rot, flip)] = xform_tile
    return res

def print_grid(grid, empty_char='o'):
    r_len = len(grid)
    c_len = len(grid[0])

    for x in range(r_len):
        for y in range(c_len):
            id, rot, flip, _ = grid[x][y]
            tile = get_tile(id, Tiles)
            xform_tile = rotate_tile(tile, rot)


dimension = int(math.sqrt(len(Tiles)))
G = [[None for x in range(dimension)] for y in range(dimension)]

used = set()
r_len = len(G)
c_len = len(G[0])
edges = list(Edges.keys())
edge_pairs = {'T':'B','B':'T','L':'R','R':'L'}
target_edges = {(-1,0):'R',(1,0):'L',(0,1):'B',(0,-1):'T'}

for x in range(r_len):
    for y in range(c_len):
        print("observing=",x,y, G[x][y])
        # skip if this coord already has a tile
        if G[x][y]:
            continue

        # collect all neighbor edges that need to match
        edges_to_match = {}
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # we don't need to match diagonal neighbors
                if dx != 0 or dy != 0:
                    continue

                xx = x + dx
                yy = y + dy
                if 0 <= xx < r_len and 0 <= yy < c_len:
                    # if there's no neighbor at this coord. skip because we
                    # don't need to match any edges
                    if G[xx][yy] == None:
                        continue

                    target_edge_id = target_edges[(xx,yy)]
                    # assumes data shape (id, rot, flip, edges[])
                    edges_to_match[target_edge_id] = get_tile_edge(G[xx][yy][3], target_edge_id)

        for id in edges:
            if id in used:
                continue

            edge = Edges[id]
            permutations = get_permutations(edge)
            match = None
            for perm in permutations:
                rot, flip = perm

                perm_edges = permutations[perm]
                if 'T' in edges_to_match and perm_edges[2] != edges_to_match['T']:
                    continue
                elif 'B' in edges_to_match and perm_edges[0] != edges_to_match['B']:
                    continue
                elif 'L' in edges_to_match and perm_edges[1] != edges_to_match['L']:
                    continue
                elif 'R' in edges_to_match and perm_edges[3] != edges_to_match['R']:
                    continue
                else:
                    match = perm
                    break

            if match:
                rot, flip = match
                print(f"updating G at {x}, {y}", id, rot, flip)
                G[x][y] = (id, rot, flip, edge)
                used.add(id)
                break

# print(G)







            # G[x][y] = ():



# edge1 = [
#     '12345',
#     '56789',
#     '....9',
#     '1....'
# ]

# edge2 = [
#     '1....',
#     '.....',
#     '5....',
#     '12345'
# ]

# print_tile(edge1)
# print('')
# print_tile(edge2)
# print('')

# # rot, flip = find_matching_tile_orientation(edge1, 'T', edge2)
# # print('rot=',rot,'flip=',flip)

# poss = get_permutations(edge2)
# for p in poss:
#     print('rot=',p[0], 'flip=',p[1])
#     print_tile(poss[p])
#     print('')


tile1 = [
    '12345',
    '....6',
    '....7',
    '....8',
    '....9',
]

print_full_tile(tile1)
print('')
xform_tile = rotate_full_tile(tile1, 90)
print_full_tile(xform_tile)

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




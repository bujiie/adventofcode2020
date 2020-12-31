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

CnE = {}

for id in Edges:
    target_edges = Edges[id]
    for i, edge in enumerate(target_edges):
        matched = False

        for id2 in Edges:
            if id == id2:
                continue

            check_edges = Edges[id2]
            for edge2 in check_edges:
                reverse = False
                if edge == edge2 or edge == edge2[::-1]:
                    matched = True
                    break

            if matched:
                break

        if not matched:
            if id not in CnE:
                CnE[id] = []
            CnE[id].append((i, edge))
            matched = False

Corners = {}
for id in CnE:
    if len(CnE[id]) == 2:
        Corners[id] = CnE[id]

def rotate_to(subject, target):
    rot = 0
    s0, s1 = subject
    t0, t1 = target

    while s0 != t0 and s1 != t0:
        rot += 1
        if s0 == 3:
            s0 = 0
        else:
            s0 += 1

        if s1 == 3:
            s1 = 0
        else:
            s1 += 1
    return rot*90

def rotate_numbers(nums):
    e1,e2 = nums
    if e1 == 3:
        e1 = 0
    else:
        e1 += 1
    return (e1, e2)


# print(Corners)

# def get_corner_permutations(corners):
#     c = [(id, (corners[id][0][0], corners[id][1][0])) for id in corners]
#     permutations = []
#     for item in c:
#         id1, edges1 = item
#         for

# get_corner_permutations(Corners)

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

def flip_full_tile_horizontal(tile):
    tile = deepcopy(tile)
    for i, line in enumerate(tile):
        tile[i] = tile[i][::-1]
    return tile

def flip_tile_vertical(tile):
    tile = deepcopy(tile)
    tile[0], tile[2] = tile[2], tile[0]
    tile[1] = tile[1][::-1]
    tile[3] = tile[3][::-1]
    return tile

def flip_full_tile_vertical(tile):
    tile = deepcopy(tile)
    tile.reverse()
    return tile

def flip_tile(tile, direction='h'):
    if direction == 'h':
        return flip_tile_horizontal(tile)
    elif direction == 'v':
        return flip_tile_vertical(tile)

def flip_full_tile(tile, direction='h'):
    if direction == 'h':
        return flip_full_tile_horizontal(tile)
    elif direction == 'v':
        return flip_full_tile_vertical(tile)

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

def resolve_grid(grid, empty_char='o'):
    new_grid = deepcopy(grid)

    r_len = len(grid)
    c_len = len(grid[0])
    d_len = len(grid[0][0][3][0])

    for x in range(r_len):
        for y in range(c_len):
            if grid[x][y]:
                id, rot, flip, _ = grid[x][y]
                # get_tile capable of getting full or edge tile representation
                tile = get_tile(id, Tiles)
                xform_tile = rotate_full_tile(tile, rot)
                if flip != 'n':
                    xform_tile = flip_full_tile(xform_tile, flip)
                new_grid[x][y] = xform_tile
            else:
                lines = []
                for _ in range(d_len):
                    lines.append(empty_char*(d_len-1))
                new_grid[x][y] = lines
    return new_grid

# will always print full tiles
def print_grid(grid, empty_char='o'):
    r_len = len(grid)
    c_len = len(grid[0])
    x_len = len(grid[0][0])
    for i in range(r_len):
        for x in range(x_len):
            for j in range(c_len):
                print(grid[i][j][x], end='')
                print('\t', end='')
            print('')
        print('\n\n', end='')


dimension = int(math.sqrt(len(Tiles)))
G = [[None for x in range(dimension)] for y in range(dimension)]
# Top Left (0,3)
G[0][0] = ('2971', 0, 'n', Edges['2971'])
# Bottom Left (2,3)
G[-1][0] = ('1171', 0, 'n', Edges['1171'])
# Top Right (0,1)
G[0][-1] = ('3079', 0, 'n', Edges['3079'])
# Bottom Right (1,2)
G[-1][-1] = ('1951', 180, 'n', Edges['1951'])

used = set()
used.add('3079')
used.add('2971')
used.add('1171')
used.add('1951')

r_len = len(G)
c_len = len(G[0])
edges = list(Edges.keys())
edge_pairs = {'T':'B','B':'T','L':'R','R':'L'}
target_edges = {(-1,0):'R',(1,0):'L',(0,1):'B',(0,-1):'T'}

def match_tiles(t1, t2, dx, dy):
    # t2 is to the LEFT of t1
    if dx == -1:
        pass
    # t2 is to the RIGHT of t1
    if dx == 1:
        pass
    # t2 is ABOVE t1
    if dy == 1:
        pass
    # t2 is BELOW t1
    if dy == -1:
        pass



while len(used) < len(Tiles) and True:
    for x in range(r_len):
        for y in range(c_len):
            print("observing=",x,y, G[x][y])
            # skip if this coord already has a tile
            if G[x][y]:
                continue

            main_opts = get_permutations()
            # collect all neighbor edges that need to match
            edges_to_match = {}
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    # we don't need to match diagonal neighbors
                    if (dx != 0 and dy != 0) or (dx == 0 and dy == 0):
                        continue

                    xx = x + dx
                    yy = y + dy
                    # print('xx=',xx,'yy=',yy)
                    if 0 <= xx < r_len and 0 <= yy < c_len:
                        # if there's no neighbor at this coord. skip because we
                        # don't need to match any edges
                        if G[xx][yy] == None:
                            continue

                        target_edge_id = target_edges[(dx,dy)]
                        # assumes data shape (id, rot, flip, edges[])
                        edges_to_match[target_edge_id] = get_tile_edge(G[xx][yy][3], target_edge_id)

            if len(edges_to_match) == 0:
                id = edges.pop(0)
                G[x][y] = (id, 0, 'n', Edges[id])
            else:
                # print('edges to match', edges_to_match)
                for id in edges:
                    if id in used:
                        continue

                    edge = Edges[id]
                    permutations = get_permutations(edge)
                    match = None
                    for perm in permutations:
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
                        # print(f"updating G at {x}, {y}", id, rot, flip)
                        G[x][y] = (id, rot, flip, edge)
                        print(edge)
                        used.add(id)
                        break


resolved_grid = resolve_grid(G)
print_grid(resolved_grid)







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


# tile1 = [
#     '12345',
#     '....6',
#     '....7',
#     '....8',
#     '....9',
# ]

# print_full_tile(tile1)
# print('')
# xform_tile = rotate_full_tile(tile1, 90)
# print_full_tile(xform_tile)

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




#!/usr/bin/env python3

import sys
from collections import defaultdict
import math
from copy import deepcopy

Tiles = {}
Edges = {}

filename=sys.argv[1]

r_len = 10
c_len = 10
divider_len = 60

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
            Tiles[id].append(list(line))

dim = int(math.sqrt(len(Tiles)))

# Compile all the edges for each tile
for id in Tiles:
    top = []
    right = []
    bottom = []
    left = []
    for r in range(r_len):
        left.append(Tiles[id][r][0])
        right.append(Tiles[id][r][-1])
    for c in range(c_len):
        top.append(Tiles[id][0][c])
        bottom.append(Tiles[id][-1][c])
    # IMPORTANT: The range order of this loop locks the list indices to a respective tile side
    # 0 = top, 1 = right, 2 = bottom, 3 = left
    edges = [e for e in [top, right, bottom, left]]
    Edges[id] = set([tuple(e) for e in edges] + [tuple(reversed(e)) for e in edges])

# For each tile, define a set of other tiles that have a matching edge.
matching_edges = defaultdict(set)
for id1 in Edges:
    for id2 in Edges:
        if id1 == id2:
            continue

        if len(Edges[id1].intersection(Edges[id2])) > 0:
            matching_edges[id1].add(id2)

G = [[None for x in range(dim)] for y in range(dim)]

corners = []
for id in matching_edges:
    if len(matching_edges[id]) == 2:
        corners.append(id)

# Corner
G[0][0] = corners[0]
G[0][1], G[1][0] = matching_edges[corners[0]]
used = {G[0][0],G[0][1],G[1][0]}

# Don't worry about orientation just yet. First put all the tiles in their correct
# places in the grid by checking that they match all of their neighbors edges.
while len(used) < len(Tiles):
    for x in range(dim):
        for y in range(dim):
            if G[x][y] is not None:
                continue

            available = set([a for a in matching_edges.keys() if a not in used])
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    # (0,0) is the context piece
                    if dx == 0 and dy == 0:
                        continue
                    # we are not concerned with the diagonal neighbors
                    if dx == dy or dx == -dy:
                        continue
                    xx = x + dx
                    yy = y + dy
                    if 0 <= xx < dim and 0 <= yy < dim and G[xx][yy] is not None:
                        # For each neighbor that already has a tile, we need to determine which tiles
                        # will match if put in the (x,y) spot. As we ask each neighbor which tiles they
                        # match with, by continually taking the intersection, we will eventually find
                        # 0 or 1 that satisfies all the neighbors.
                        available = available.intersection(matching_edges[G[xx][yy]])

                        if len(available) == 1:
                            match = next(iter(available))
                            G[x][y] = match
                            used.add(match)


# t1 = context tile
# t2 = neighbor tile
# n_coord = relative coord (dx, dy) of t2 with respect to t1
def does_match(t1, t2, n_coord):
    # neighbor tile is to the LEFT of context tile
    if n_coord == (0, -1):
        for i in range(len(t1[0])):
            if t1[i][0] != t2[i][-1]:
                return False
        return True
    # neighbor tile is to the RIGHT of context tile
    elif n_coord == (0, 1):
        for i in range(len(t1[0])):
            if t1[i][-1] != t2[i][0]:
                return False
        return True
    # neighbor tile is BELOW the context tile
    elif n_coord == (-1, 0):
        return t1[0] == t2[-1]
    # neighbor tile is ABOVE the context tile
    elif n_coord == (1, 0):
        return t1[-1] == t2[0]
    else:
        return False


def rotate(t):
    dimension = len(t)
    new_t = []
    for y in range(dimension):
        row = []
        for x in reversed(range(dimension)):
            row.append(t[x][y])
        new_t.append(row)
    return new_t


def flip(t):
    return list(reversed(t))


def orientations(t):
    orients = set()
    transforms = [deepcopy(t), flip(t)]
    for _ in range(4):
        orients.add(tuple([tuple(x) for x in transforms[0]]))
        orients.add(tuple([tuple(x) for x in transforms[1]]))
        transforms = [rotate(transforms[0]), rotate(transforms[1])]
    return orients

# will always print full tiles
def print_grid(grid, separate=True, empty_char='o'):
    r_len = len(grid)
    c_len = len(grid[0])
    x_len = len(grid[0][0])
    for i in range(r_len):
        for x in range(x_len):
            for j in range(c_len):
                print(''.join(grid[i][j][x]), end='')
                if separate:
                    print('\t', end='')
            print('')
        if separate:
            print('\n')

P = [[None for _ in range(dim)] for _ in range(dim)]

# Now we need to orient all the pieces so the edges actually match.
for x in range(dim):
    for y in range(dim):
        orients1 = orientations(Tiles[G[x][y]])

        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                # (0,0) is the context piece
                if dx == 0 and dy == 0:
                    continue
                # we are not concerned with the diagonal neighbors
                if dx == dy or dx == -dy:
                    continue
                xx = x + dx
                yy = y + dy
                if 0 <= xx < dim and 0 <= yy < dim:
                    matches = set()
                    orients2 = orientations(Tiles[G[xx][yy]])
                    for orient1 in orients1:
                        for orient2 in orients2:
                            if does_match(orient1, orient2, (dx, dy)):
                                matches.add(orient1)

                    # For the tile in the (x,y) position, we need to determine which
                    # orientation has a match with all neighboring tiles. We do this
                    # by going through all the combinations of (x,y) tile and neighbor
                    # orientations and keeping track of the matches and taking the
                    # intersection of the sets as we check each neighbor.
                    orients1 = orients1.intersection(matches)

                if len(orients1) == 1:
                    P[x][y] = next(iter(orients1))

print('ALIGNED TILES')
print('='*divider_len)
print_grid(P)

I = [[None for _ in range(dim)] for _ in range(dim)]
# Remove the borders and build the image
for x in range(dim):
    for y in range(dim):
        num_rows = len(P[x][y])
        new_tile = []
        for i in range(num_rows):
            # drop the first and last row
            if i == 0 or i == num_rows - 1:
                continue
            new_tile.append(tuple(P[x][y][i][1:-1]))
        I[x][y] = tuple(new_tile)

print('RECONSTRUCTED IMAGE')
print('='*divider_len)
print_grid(I, separate=False)
print('\n')

# Reduce image to a 2D array instead of separate structures for each tile.
# We don't need to track individual tiles anymore.
rows_of_tiles = len(I)
cols_of_tiles = len(I[0])
rows_in_tile = len(I[0][0])
cols_in_tile = len(I[0][0][0])
new_I = []

for x in range(rows_of_tiles):
    for i in range(rows_in_tile):
        new_line = []
        for y in range(cols_of_tiles):
            new_line += I[x][y][i]
        new_I.append(new_line)
I = new_I

print('FLATTENED IMAGE ARRAY (should be identitcal to previous)')
print('='*divider_len)
print_grid(I, separate=False)
print('\n')


# Find the monster
monster = ['                  # ',
           '#    ##    ##    ###',
           ' #  #  #  #  #  #   ']

monster_rel = {
    (0, 18),
    (1, 0),(1, 5),(1, 6),(1, 11),(1, 12),(1, 17), (1, 18), (1, 19),
    (2, 1),(2, 4), (2, 7), (2, 10), (2, 13), (2, 16)
}

mx_len = len(monster)
my_len = len(monster[0])

num_monsters = 0

orientation = None
monsters = []

for oi, orient in enumerate(orientations(I)):
    ir = len(orient)
    ic = len(orient[0])

    for x in range(ir):
        for y in range(ic):
            # print(oi,"checking for monsters... x,y=",x,y, ir, ic)
            # print("y_len", my_len, "x_len", mx_len)
            maybe_monster = set()
            if y + my_len > ic - 1:
                continue
            if x + mx_len > ir - 1:
                continue

            for rel in monster_rel:
                dx, dy = rel
                # print(rel)
                xx = x + dx
                yy = y + dy
                if orient[xx][yy] == '#':
                    maybe_monster.add((dx,dy))

            if len(monster_rel.difference(maybe_monster)) == 0:
                monsters.append((x,y))
                orientation = (oi, orient)
                num_monsters += 1

# Not necessary, but a nice visual. Replace all monster characters
# with something other than # to make them more visible.
m_replace = 'T'
temp = [list(r) for r in orientation[1]]
for m in monsters:
    x,y = m
    for rel in monster_rel:
        dx,dy = rel
        temp[x+dx][y+dy] = m_replace

print(f'ORIENTATION WITH MONSTERS FOUND (orientation no. {orientation[0]})')
print('='*divider_len)
print_grid(orientation[1], separate=False)
print('\n')

print(f'IMAGE WITH MONSTERS OUTLINED WITH ({m_replace})')
print('='*divider_len)
print_grid(temp, separate=False)
print('\n')

num_pounds = 0
for row in I:
    num_pounds += row.count('#')

num_pounds_monster = 0
for row in monster:
    num_pounds_monster += row.count('#')

print('IMAGE STATS')
print('='*divider_len)
print('monster size: ', num_pounds_monster)
print('no. of monsters: ', num_monsters)
print('no. of pound signs: ', num_pounds)
print('no. of rough seas: ', num_pounds - (num_monsters * num_pounds_monster))
print('\n')







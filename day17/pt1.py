#!/usr/bin/env python3

import sys
import re
from copy import deepcopy
import json

filename=sys.argv[1]

xl,yl,zl = (8,8,8)
cube = [[['.' for i in range(zl)] for j in range(yl)] for k in range(xl)]
cube[1] = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        cube[1].append(list(line.strip()))

def add_new_layer(kube, c='.'):
    side = len(kube)
    new_cube = deepcopy(kube)
    new_row = [c for i in range(side+2)]
    new_face = [new_row for i in range(side+2)]

    for x in range(side):
        for y in range(side):
            new_cube[x][y] = [c, *new_cube[x][y], c]
        new_cube[x] = [deepcopy(new_row), *new_cube[x], deepcopy(new_row)]
    new_cube = [deepcopy(new_face), *new_cube, deepcopy(new_face)]
    return new_cube

def print_cube(cube):
    side = len(cube)
    for x in range(side):
        not_empty = False
        layers = []
        for y in range(side):
            layer = ''.join(cube[x][y])
            layers.append(layer)
            if '#' in layer:
                not_empty = True
        if not_empty:
            print('x=', x)
            print('\n'.join(layers))
            print('')


max_iter = 6
cycle = 0
print_cube(cube)

cube = add_new_layer(add_new_layer(cube))

while cycle < max_iter:
    print('='*40, cycle, '='*40)

    new_cube = deepcopy(cube)
    length = len(new_cube)-1

    for x in range(1,length):
        for y in range(1,length):
            for z in range(1,length):

                # check all surrounding coordinates
                active_neighbors = 0
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        for dz in [-1,0,1]:
                            if not (dx == 0 and dy == 0 and dz == 0):
                                xx = x + dx
                                yy = y + dy
                                zz = z + dz
                                #print("checking",xx,yy,zz)
                                if 0 <= xx < length and 0 <= yy < length and 0 <= zz < length:
                                    if cube[xx][yy][zz] == '#':
                                        active_neighbors += 1

                # if 0 <= x < old_length and 0 <= y < old_length and 0 <= z < old_length:
                flipping = False
                if cube[x][y][z] == '#':
                    if active_neighbors not in [2,3]:
                        new_cube[x][y][z] = '.'
                        flipping = True
                    # print(x,y,z,'is active', 'neighbors (active)',active_neighbors, flipping)
                elif cube[x][y][z] == '.':
                    if active_neighbors in [3]:
                        new_cube[x][y][z] = '#'
                        flipping = True
                    # print(x,y,z,'is inactive', 'neighbors (active)', active_neighbors, flipping)
    print_cube(new_cube)
    cycle += 1
    cube = deepcopy(add_new_layer(new_cube))

s = len(cube)
count = 0
for x in range(s):
    for y in range(s):
        for z in range(s):
            if cube[x][y][z] == '#':
                count += 1

print(count)
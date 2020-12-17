#!/usr/bin/env python3

import sys
import re
from copy import deepcopy
import json

filename=sys.argv[1]

# xl,yl,zl = (3,3,3)
# empty_cube = [[['.' for i in range(zl)] for j in range(yl)] for k in range(xl)]
# cube = deepcopy(empty_cube)
# hyper_cube = [deepcopy(empty_cube) for i in range(xl)]
# cube[1] = []

space=[[[]]]

with open(filename) as fp:
    for index, line in enumerate(fp):
        space[0][0].append(list(line.strip()))

def calc_size(space, p=False):
    w_len = len(space)
    x_len = len(space[0])
    y_len = len(space[0][0])
    z_len = len(space[0][0][0])

    if p:
        print('w=',w_len,'x=',x_len,'y=',y_len,'z=',z_len)
    return (w_len,x_len,y_len,z_len)


def grow(space, c = '.'):
    (w_len, x_len, y_len, z_len) = calc_size(space)
    c_space = deepcopy(space)
    empty_row = [c for i in range(z_len+2)]
    empty_face = [deepcopy(empty_row) for i in range(y_len+2)]
    empty_cube = [deepcopy(empty_face) for i in range(x_len+2)]

    for w in range(w_len):
        for x in range(x_len):
            for y in range(y_len):
                c_space[w][x][y] = [c, *c_space[w][x][y], c]
            c_space[w][x] = [deepcopy(empty_row), *c_space[w][x], deepcopy(empty_row)]
        c_space[w] = [deepcopy(empty_face), *c_space[w], deepcopy(empty_face)]
    c_space = [deepcopy(empty_cube), *c_space, deepcopy(empty_cube)]
    return c_space

def print_space(space, d=False):
    (wlen,xlen,ylen,zlen) = calc_size(space)

    print('='*30,'len(w,x,y,z):',wlen,xlen,ylen,zlen,'='*30)
    for w in range(wlen):
        print('-'*10,'w=',w,'-'*10)
        for x in range(xlen):
            print('w=',w,'x=',x)
            for y in range(ylen):
                if d:
                    print(w,x,y,'space=',space[w][x][y])
                print(''.join(space[w][x][y]))
            print('')

target_cycle = 6
cycle = 0
display = False

if display:
    print_space(space)
space = grow(grow(space))

while cycle < target_cycle:
    n_space = deepcopy(space)

    (wl,xl,yl,zl) = calc_size(n_space)
    w_len = wl-1
    x_len = xl-1
    y_len = yl-1
    z_len = zl-1

    for w in range(1,w_len):
        for x in range(1,x_len):
            for y in range(1,y_len):
                for z in range(1,z_len):
                    # print('checking=',w,x,y,z)
                    active_neighbors = 0
                    for dw in [-1,0,1]:
                        for dx in [-1,0,1]:
                            for dy in [-1,0,1]:
                                for dz in [-1,0,1]:
                                    if not (dw == 0 and dx == 0 and dy == 0 and dz == 0):
                                        ww = w + dw
                                        xx = x + dx
                                        yy = y + dy
                                        zz = z + dz
                                        # print('(ww,xx,yy,zz)',ww,xx,yy,zz)
                                        if 0 <= ww < w_len and 0 <= xx < x_len and 0 <= yy < y_len and 0 <= zz < z_len:
                                            line = f'neighbor ({ww},{xx},{yy},{zz})'
                                            if space[ww][xx][yy][zz] == '#':
                                                line += ' is ACTIVE'
                                                active_neighbors += 1
                                            else:
                                                line += 'is inactive'
                                            # print(line)

                    # print(w,x,y,z,"spacesize=",calc_size(n_space))
                    if space[w][x][y][z] == '#':
                        if active_neighbors not in [2,3]:
                            n_space[w][x][y][z] = '.'
                    elif space[w][x][y][z] == '.':
                        if active_neighbors in [3]:
                            n_space[w][x][y][z] = '#'
    if display:
        print_space(n_space)
    cycle += 1
    space = deepcopy(grow(n_space))


(w_len,x_len,y_len,z_len) = calc_size(space)

count = 0
for w in range(w_len):
    for x in range(x_len):
        for y in range(y_len):
            for z in range(z_len):
                # print(w,x,y,z)
                if space[w][x][y][z] == '#':
                    count += 1

print(count)

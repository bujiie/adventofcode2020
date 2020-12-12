#!/usr/bin/env python3

import sys
import re
import copy
from collections import deque

filename=sys.argv[1]

ro=['E','S','W','N']
p = [0,0,0,0]
# E S W N
wp = deque([10,0,0,1])
with open(filename) as fp:
    for index, line in enumerate(fp):
        action = line.strip()
        (d,u) = (action[0], int(action[1:]))
        if d == 'F':
            # E S W N
            p[0] += wp[0]*u
            p[1] += wp[1]*u
            p[2] += wp[2]*u
            p[3] += wp[3]*u
        elif d in ['N','S','E','W']:
            wp[ro.index(d)] += u
        elif d=='R':
            wp.rotate(int(u/90))
        elif d=='L':
            wp.rotate(-int(u/90))

        print(d,u,wp,p)

r=abs(p[2]-p[0]) + abs(p[3]-p[1])
print(r)




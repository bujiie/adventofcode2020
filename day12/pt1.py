#!/usr/bin/env python3

import sys
import re

filename=sys.argv[1]

ro=['E','S','W','N']
p = {'E':0,'W':0,'S':0,'N':0}
o = 'E'
with open(filename) as fp:
    for index, line in enumerate(fp):
        action = line.strip()
        (d,u) = (action[0], int(action[1:]))
        if d == 'F':
            p[o] += u
        elif d in ['N','S','E','W']:
            p[d] += u
        elif d=='R':
            j=ro.index(o) + int(u/90)
            j=j%len(ro)
            o = ro[j]
        elif d=='L':
            j= ro.index(o) - int(u/90)
            j=j%len(ro)
            o = ro[j]

        print(o,d,u,p)

r=abs(p['E']-p['W']) + abs(p['S']-p['N'])
print(r)




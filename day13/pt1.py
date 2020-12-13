#!/usr/bin/env python3

import sys
import re


filename=sys.argv[1]

etd = -1
s=[]
with open(filename) as fp:
    for index, line in enumerate(fp):
        if index == 0:
            etd=int(line.strip())
        else:
            s=list(map(lambda n: int(n), list(filter(lambda b: b != 'x', line.strip().split(',')))))

diff=-1
b=-1
for i in s:
    m=int(etd/i)
    t=m*i
    if t < etd:
        m+=1
        t+=i
    if diff < 0 or diff > t-etd:
        b=i
        diff=t-etd

print(diff*b)


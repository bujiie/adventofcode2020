#!/usr/bin/env python3

import sys
import re
import math
from functools import reduce

filename=sys.argv[1]

etd = -1
s=[]
with open(filename) as fp:
    for index, line in enumerate(fp):
        s=list(map(lambda n: 0 if n=='x' else int(n), line.strip().split(',')))

l=-1
a=-1
for i,k in enumerate(s):
    if k > a:
        l=i
        a=k

i=1_000_000
# i=3_000
# i=0
inc=int(i/s[l])
start=inc*s[l]

o=[k for k in range(0-l,len(s)-l)]
# print(s,start,o)
while True:
    valid=True
    for j in o:
        # if s[j]!=0:
            # print(start,j,start+j,s[j],(start+j)%s[l+j])
        if s[l+j]!=0 and (start+j)%s[l+j]>0:
            valid=False
            break
    if valid:
        print(start-l)
        break
    start+=s[l]

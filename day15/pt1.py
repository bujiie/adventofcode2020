#!/usr/bin/env python3

import sys

filename=sys.argv[1]

memory=[]
D={}
with open(filename) as fp:
    for index, line in enumerate(fp):
        memory=list(map(lambda n: int(n), line.strip().split(',')))
        for i,m in enumerate(memory):
            D[m]=[i]

i=len(memory)

while i < 2020:
    last=memory[-1]
    if last not in memory[:-1]:
        memory.append(0)
        if 0 not in D:
            D[0]=[]
        D[0].append(i)
    else:
        diff = i - D[last][-2]-1
        memory.append(diff)
        if diff not in D:
            D[diff]=[]
        D[diff].append(i)
    i+=1
print(len(memory), memory[-1])

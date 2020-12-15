#!/usr/bin/env python3

import sys
from itertools import islice

filename=sys.argv[1]

memory=[]
D={}
with open(filename) as fp:
    for index, line in enumerate(fp):
        memory=list(map(lambda n: int(n), line.strip().split(',')))
        for i,m in enumerate(memory):
            D[m]=i

def van_eck(h={}, init=[]):
    # starting index offset by the initial length of the input
    i = len(init) - 1
    # initial history of numbers and their last known index
    seen = h
    # last item from the initial input
    last = init[-1]

    while True:
        yield last
        prev = {last: i}
        last = i - seen.get(last, i)
        seen.update(prev)
        i+=1

target=30000000
print(list(islice(van_eck(D, memory), target-len(memory)+1))[-1])

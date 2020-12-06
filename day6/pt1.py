#!/usr/bin/env python3

import sys

filename=sys.argv[1]

groups = [[]]

with open(filename) as fp:
    for index, line in enumerate(fp):
        clean_line = line.strip()
        
        if len(clean_line) == 0:
            groups.append([])
        else:     
            groups[-1].append(clean_line)     

total = 0

for group in groups:
    flat_group = [answer for person in group for answer in person]
    total = total + len(set(flat_group))

print(total)

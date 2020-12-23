#!/usr/bin/env python3

import sys
from collections import deque

filename=sys.argv[1]

C = {}
C_tail = {}
lookup = {}
max_c = None
min_c = None
with open(filename) as fp:
    for index, line in enumerate(fp):
        p = C
        nums = list(map(lambda n: int(n), list(line.strip())))
        max_c = max(nums)
        min_c = min(nums)
        nums.extend(range(max_c+1, 1_000_001))
        max_c = max(nums)

        for i, c in enumerate(nums):
            if i == len(nums) - 1:
                lookup[c] = p
                p[c] = C
            else:
                lookup[c] = p
                p[c] = {}
            p = p[c]


max_move = 10_000_001
move_count = 0
cc = C

while move_count < max_move:
    picked_nums = []
    # gets the value (next number) from the list
    picked = next(iter(cc.values()))

    node = picked
    # we need to track this so we can unhook its value from the list
    picked_tail_node = None
    for i in range(0, 3):
        picked_nums.append(next(iter(node.keys())))
        picked_tail_node = node
        node = next(iter(node.values()))
    picked_tail_node_num = next(iter(picked_tail_node.keys()))
    cc[next(iter(cc.keys()))] = picked_tail_node[picked_tail_node_num]
    picked_tail_node[picked_tail_node_num] = None

    search_for = next(iter(cc.keys())) - 1
    while search_for in picked_nums or search_for < min_c:
        if search_for < min_c:
            search_for = max_c
        else:
            search_for -= 1

    c, rest = next(iter(lookup[search_for].items()))
    picked_tail_node[next(iter(picked_tail_node.keys()))] = rest
    lookup[search_for][c] = picked
    cc = next(iter(cc.values()))

    move_count += 1

one_found = False
neighbors = []
node = C

while True:
    n, rest = next(iter(node.items()))
    if one_found:
        if len(neighbors) >= 2:
            break
        else:
            neighbors.append(n)
    if n == 1:
        one_found = True
    node = rest

ans = 1
for n in neighbors:
    ans *= n
print(ans)

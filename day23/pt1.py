#!/usr/bin/env python3

import sys
from collections import deque

filename=sys.argv[1]

C = None
with open(filename) as fp:
    for index, line in enumerate(fp):
        C = deque(list(map(lambda n: int(n), list(line.strip()))))

min_c = min(C)
max_c = max(C)

move_count = 0
max_move = 101
while move_count < max_move:
    # always the first item since we rotate the deque at the end of each round.
    cc = C[0]

    print(f"-- move {move_count + 1} --")
    print(f"cups: ", end='')

    for i, c in enumerate(C):
        if c == cc:
            print(f"({c}) ", end='')
        else:
            print(f"{c} ", end='')
    print('')

    picked = [C[1], C[2], C[3]]
    del C[1]
    del C[1]
    del C[1]

    print(f"pick up: {picked}")
    # print(f"after cups removed: ", end='')
    # for i, c in enumerate(C):
    #     if c == cc:
    #         print(f"({c}) ", end='')
    #     else:
    #         print(f"{c} ", end='')
    # print('')

    search_for = cc - 1
    # print('sf=',search_for)
    while search_for in picked or search_for < min_c:
        # print('sf=',search_for,'p=',picked)
        if search_for < min_c:
            search_for = max_c
        else:
            search_for -= 1

    destination_i = None
    for i, c in enumerate(C):
        if c == search_for:
            destination_i = i
            break

    # print("destination index =", destination_i)
    if destination_i != None:
        print(f"destination: {C[destination_i]}")
        C.insert(destination_i+1, picked[2])
        C.insert(destination_i+1, picked[1])
        C.insert(destination_i+1, picked[0])
        C.rotate(-1)
    # print(C)
    print('')

    # destination cup -> find index of cc-1
    move_count += 1
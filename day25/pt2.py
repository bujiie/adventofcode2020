#!/usr/bin/env python3

import sys

filename=sys.argv[1]

DPK = None
CPK = None
with open(filename) as fp:
    for index, line in enumerate(fp):
        line = int(line.strip())

        if index == 0:
            CPK = line
        elif index == 1:
            DPK = line

divisor = 20201227

value = 1
subject_no = 7
c_loop_count = 0
while value != CPK:
    value *= subject_no
    value %= divisor
    c_loop_count += 1

value = 1
subject_no = 7
d_loop_count = 0
while value != DPK:
    value *= subject_no
    value %= divisor
    d_loop_count += 1

loop_size = None
subject_no = None
if c_loop_count < d_loop_count:
    loop_size = c_loop_count
    subject_no = DPK
else:
    loop_size = d_loop_count
    subject_no = CPK

value = 1
for _ in range(loop_size):
    value *= subject_no
    value %= divisor

print(value)

# print('card loop size=', c_loop_count)
# print('door loop size=', d_loop_count)
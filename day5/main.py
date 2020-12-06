#!/usr/bin/env python3

import sys

filename = sys.argv[1]
boarding_passes = []

all_seat_ids = []

for row in range(0, 128):
    for col in range(0, 8):
        all_seat_ids.append(int(row * 8 + col))        


with open(filename) as fp:
    boarding_passes = [bp.strip() for bp in fp.readlines()]    

num_rows = 128
num_cols = 8
largest_seat_id = 0
boarded_seats = []

for boarding_pass in boarding_passes:
    row_range = (0, num_rows)
    col_range = (0, num_cols)

    for char in boarding_pass:
        if char == 'F':
            row_range = (row_range[0], row_range[1]/2)
            #print(f"char=F,range={row_range}")
        elif char == 'B':
            row_range = (row_range[0] + row_range[1]/2, row_range[1]/2)
            #print(f"char=B,range={row_range}")
        elif char == 'L':
            col_range = (col_range[0], col_range[1]/2)
            #print(f"char=L,range={col_range}")
        elif char == 'R':
            col_range = (col_range[0] + col_range[1]/2, col_range[1]/2)
            #print(f"char=R,range={col_range}")

    row = row_range[0] + (row_range[1] - 1)
    col = col_range[0] + (col_range[1] - 1)
    seat_id = row * 8 + col
    boarded_seats.append(int(seat_id))
    #print(f"bp={boarding_pass},row={row},col={col},sid={seat_id}")
    if seat_id > largest_seat_id:
        largest_seat_id = seat_id


boarded_seats.sort()

for seat in range(boarded_seats[0], len(boarded_seats) -1):
    if seat not in boarded_seats:
        print(seat)


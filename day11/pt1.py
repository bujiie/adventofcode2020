#!/usr/bin/env python3

import sys
import re
import copy

def clean(string):
    return string.strip()

def split(string, separator=''):
    return list(map(lambda p: p.strip(), string.split(separator)))

# Use groups () or named groups (?P<name>...) in regex to return specific parts
# of the string.
#
# Returns re.Match (use .groups() or .group('name'))
def parse_from_string(regex, string):
    matches = re.search(regex, string)
    if not matches:
        print(f"Could not parse string={string}. No matches found for regex={regex}")
        return []
    if len(matches.groups()) == 0:
        print(f"A match was found, but no capture groups were included in regex={regex}")
        return []
    return matches

# for_this should be a regular expression.
# Basic example of a simple find word and replace:
#   replace_in_string('blue bag', r'bag', 'bird') -> 'blue bird'
def replace_in_string(search_me, for_this, replace_with):
    return re.sub(for_this, replace_with, search_me)



filename=sys.argv[1]

seats = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        row = clean(line)
        seats.append(list(row))

def get_surrounding_seats(seat, seating=[]):
    (n,m) = seat
    surrounding = [
        (n-1,m-1),
        (n-1,m),
        (n-1,m+1),
        (n,m-1),
        (n,m+1),
        (n+1,m-1),
        (n+1,m),
        (n+1,m+1)
    ]
    # 0-open, 1-taken
    result = [[],[],[]]
    for s in surrounding:
        if s[0] >= 0 and s[0] < len(seating) and s[1] >= 0 and s[1] < len(seating[0]):
            if seating[s[0]][s[1]] == 'L':
                result[0].append(s)
            elif seating[s[0]][s[1]] == '#':
                result[1].append(s)
            elif seating[s[0]][s[1]] == '.':
                result[2].append(s)
    return result

def do_update_seats(seating):
    updated_seats = copy.deepcopy(seating)
    for r_index, row in enumerate(seating):
        for c_index, col in enumerate(row):
            adj_seats = get_surrounding_seats((r_index, c_index), seating)
            #print("r=",r_index,"c=",c_index,"adj=",adj_seats)
            if seating[r_index][c_index] == 'L' and len(adj_seats[1]) == 0:
                updated_seats[r_index][c_index] = '#'
            elif seating[r_index][c_index] == '#' and len(adj_seats[1]) > 3:
                updated_seats[r_index][c_index] = 'L'
    return updated_seats

def get_occupied_seats(seating):
    occupied = []
    for r_index, row in enumerate(seating):
        for c_index, col in enumerate(row):
            if seating[r_index][c_index] == '#':
                occupied.append((r_index,c_index))
    return occupied

count = 20
i = 0
s = copy.deepcopy(seats)
last_hash = ''

while True:
    s = do_update_seats(s)


    mega_line = ''
    for row in s:
        line = ''
        for col in row:
            line += col
            mega_line += col
        # print(line)
    # print("\n")

    if last_hash == mega_line:
        break
    last_hash = mega_line
    i += 1


print(len(get_occupied_seats(s)))




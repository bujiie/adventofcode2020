#!/usr/bin/env python3

import sys
import re
import copy
import itertools

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

def all_indices_of_occureance(lst, find):
    return [i for i, x in enumerate(lst) if x == find]

filename=sys.argv[1]

seats = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        row = clean(line)
        seats.append(list(row))

def get_surrounding_seats(seat, seating=[]):
    (n,m) = seat

    n_min = 0
    n_max = len(seating)
    m_min = 0
    m_max = len(seating[0])

    taken = []
    closest = -1
    for i,s in enumerate(seating[n]):
        if s == '#' and i != m:
            closest = i
        if i == m and closest != -1:
            taken.append((n,closest))
            closest = -1
        if i > m and closest != -1:
            taken.append((n,closest))
            break

    closest = -1
    for i,s in enumerate(seating):
        if s[m] == '#' and i != n:
            closest = i
        if i == n and closest != -1:
            taken.append((closest,m))
            closest = -1
        if i > n and closest != -1:
            taken.append((closest,m))
            break

    closest = -1
    l_max = n if n < m else m
    for i in range(l_max, 0, -1):
        if seating[n-i][m-i] == '#' and (n-i) != n and (m-i) != m and (n-i) >= 0  and (m-i) >= 0:
            taken.append((n-i,m-i))
            break

    closest = -1
    # print("n_max=",n_max,"n=",n,"m_max=",m_max,"m=",m)
    r_max = (n_max - n) if (n_max - n) < (m_max - m) else (m_max - m)
    for i in range(0, r_max):
        if seating[n+i][m+i] == '#' and (n+i) != n and (m+i) != m:
            taken.append((n+i,m+i))
            break

    closest = -1
    l_max = (m_max - m) if (m_max - m) < n else n
    for i in range(0, l_max):
        # print("n=",n,"m=",m,"i=",i, l_max, len(seating), len(seating[n+i]))
        if seating[n-i][m+i] == '#' and (n-i) != n and (n-i) >= 0 and (m+i) != m:
            taken.append((n-i,m+i))
            break

    closest = -1
    r_max = (n_max - n) if (n_max - n) < m else m
    for i in range(0, r_max):
        if seating[n+i][m-i] == '#' and (n+i) != n and (m-i) != m and (m-i) >= 0:
            taken.append((n+i,m-i))
            break

    print("n=",n,"m=",m,"taken=",set(taken))
    return list(set(taken))

def do_update_seats(seating):
    updated_seats = copy.deepcopy(seating)
    for r_index, row in enumerate(seating):
        for c_index, col in enumerate(row):
            taken = get_surrounding_seats((r_index, c_index), seating)
            # print("r=",r_index,"c=",c_index,"adj=",taken)
            if seating[r_index][c_index] == 'L' and len(taken) == 0:
                updated_seats[r_index][c_index] = '#'
            elif seating[r_index][c_index] == '#' and len(taken) > 4:
                updated_seats[r_index][c_index] = 'L'
    return updated_seats

def get_occupied_seats(seating):
    occupied = []
    for r_index, row in enumerate(seating):
        for c_index, col in enumerate(row):
            if seating[r_index][c_index] == '#':
                occupied.append((r_index,c_index))
    return occupied

max_count=1
count = 1
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
        print(line)
    print("\n")

    if last_hash == mega_line:
        break
    if i > max_count:
        break
    last_hash = mega_line
    i += 1

print(i)
print(len(get_occupied_seats(s)))





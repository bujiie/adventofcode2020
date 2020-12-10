#!/usr/bin/env python3

import sys
import re
import itertools
import functools

def clean(string):
    return string.strip()

def split(string, separator):
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
adapters = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        adapters.append(int(clean(line)))

def sort_func(a,b):
    if b - a <= 3:
        return 1
    return -1

adapters.insert(0, 0)
adapters.sort()
print(adapters)
diffs = []

for index, adapter in enumerate(adapters):
    if index + 1 >= len(adapters):
        break
    diffs.append(adapters[index+1] - adapter)

print(diffs)

counts=[]
prev_diff = -1

for diff in diffs:
    if diff != prev_diff and diff != 3:
        counts.append(0)
    if diff == 1:
        counts[-1] += 1
    prev_diff = diff
results = []

for count in counts:
    if count == 1:
        results.append(1)
    elif count == 2:
        results.append(2)
    elif count == 3:
        results.append(4)
    elif count == 4:
        results.append(7)
    elif count == 5:
        results.append(11)

print("counts=",counts)
print("results=",results)
print(functools.reduce(lambda nxt,acc: acc*nxt, results))



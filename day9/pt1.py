#!/usr/bin/env python3

import sys
import re

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

preamble_length = 25
data = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        clean_line = int(clean(line))
        data.append(clean_line)

for i, d in enumerate(data[preamble_length:]):
    preamble = data[i:preamble_length + i]

    found = False

    for p in preamble:
        c_preamble = preamble.copy()
        diff = d - p
        c_preamble.remove(p)
        if diff in c_preamble:
            found = True
            break

    if not found:
        print(d)
        break


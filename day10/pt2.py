#!/usr/bin/env python3

import sys
import re
import itertools

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

def remove_items(test_list, item):
    res = [i for i in test_list if i != item]
    return res

def diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))


filename=sys.argv[1]
adapters = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        adapters.append(int(clean(line)))

adapters.sort()

def get_arrangement():
    arrangement = [0]

    for adapter in adapters:
        if adapter - arrangement[-1] <= 3:
            arrangement.append(adapter)
    return arrangement

print(get_arrangement())















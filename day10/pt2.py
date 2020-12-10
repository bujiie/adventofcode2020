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

def is_sorted(lst):
    # using sort() to
    # check sorted list
    flag = 0
    test_list1 = lst[:]
    test_list1.sort()
    if (test_list1 == lst):
        flag = 1
    return flag

def remove_occurrences_in_list(lst, find):
    return list(filter(lambda n: n != find, lst))

def has_changes_outside_bounds(lst, allowed=[]):
    changes = []
    for i, entity in enumerate(lst):
        next_i = i+1
        if next_i >= len(lst):
            break
        change = lst[next_i] - entity
        changes.append(change)

    for a in allowed:
        changes = remove_occurrences_in_list(changes, a)
    return len(changes) > 0

def sumOfPrevK(N, K):
    arr = [0 for i in range(N)]
    arr[0] = 1

    # Pick a starting point
    for i in range(1,N):
        j = i - 1
        count = 0
        sum = 0

        # Find the sum of all
        # elements till count < K
        while (j >= 0 and count < K):
            sum = sum + arr[j]
            j = j - 1
            count = count + 1

        # Find the value of
        # sum at i position
        arr[i] = sum

    return arr[N-1]

def get_num_combinations(n):
    return sumOfPrevK(n, 3)

filename=sys.argv[1]

# Start with outlet Joltage
adapters = [0]

with open(filename) as fp:
    for index, line in enumerate(fp):
        adapters.append(int(clean(line)))

# Adapters must be in increasing order since each successive adapter must be
# 1 or 3 jolts greater than its predecessor.
adapters.sort()

changes = []
ones_counts = []
last_change = -1

for i, adapter in enumerate(adapters):
    next_i = i+1
    # Exit loop if there is no "next" adapter in the list
    if next_i >= len(adapters):
        break
    change = adapters[next_i] - adapter

    # Whenever we come across a new series of 1s, meaning the previous change
    # was a 3 and the current change is a 1, we want to initialize a new counter
    # to the ones_counts
    if change != last_change and change != 3:
        ones_counts.append(0)
    # We only care about the grouping of 1s
    if change == 1:
        ones_counts[-1] += 1
    last_change = change
    changes.append(change)

print("changes=",changes)
print("ones counts=",ones_counts)

result = 1
for ones_count in ones_counts:

    # get_num_combinations calculates the combinations for a sequence of 'n'
    # numbers. However, ones_count represents the changes between that sequence
    # of numbers which is always n-1 much like a music staff which has 5 lines (n)
    # and four spaces (n-1). To get the correct number of combinations
    # we need to tell the function how many numbers are in the sequence, not
    # the number of changes. Therefore, we need to add 1.
    combos = get_num_combinations(ones_count+1)
    result *= combos

print(result)

# Gets the different combinations
# # for ones_count in ones_counts:
# data=[1,2,3,4,5,6,7,8]
# count = 0
# for i in range(1, len(data)+1):
#     results = itertools.combinations(data, i)
#     for r in results:
#         # For the combination to work, it must meet the following criteria.
#         #    - must be increasing order
#         #    - the first and last number in the sequence must remain the same as
#         #      the original sequence otherwise the next or previous change will
#         #      be greater than 3
#         #    - the changes between the numbers in the combination must be 1, 2
#         #      or 3.
#         if is_sorted(list(r)) and r[0] == data[0] and r[-1] == data[-1] and not has_changes_outside_bounds(r, [1,2,3]):
#             print(r)
#             count += 1
# print(count)
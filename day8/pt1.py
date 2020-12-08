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

instructions = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        clean_line = clean(line)
        matches = parse_from_string(r'^(?P<ins>[a-z]{3})\s(?P<offset>[\+\-0-9]+)', clean_line)
        instructions.append({'ins': clean(matches.group('ins')), 'offset': int(clean(matches.group('offset')))})

ins_ptr = 0
acc = 0
ins_completed = []

while True:
    ins = instructions[ins_ptr]

    #print(ins_ptr, ins, ins_completed)
    if ins_ptr not in ins_completed:
        ins_completed.append(ins_ptr)
        if ins['ins'] == 'nop':
            ins_ptr += 1
        elif ins['ins'] == 'acc':
            acc += ins['offset']
            ins_ptr += 1
        elif ins['ins'] == 'jmp':
            ins_ptr += ins['offset']
        #print("ptr=",ins_ptr,"acc=",acc)
    else:
        break

print(acc)


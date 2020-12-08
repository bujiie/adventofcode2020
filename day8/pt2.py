#!/usr/bin/env python3

import sys
import re
import copy


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

nj_ptrs = []

with open(filename) as fp:
    for index, line in enumerate(fp):
        clean_line = clean(line)
        matches = parse_from_string(r'^(?P<ins>[a-z]{3})\s(?P<offset>[\+\-0-9]+)', clean_line)
        ins = clean(matches.group('ins'))
        instructions.append({'ins': ins, 'offset': int(clean(matches.group('offset')))})
        if ins == 'nop' or ins == 'jmp':
            nj_ptrs.append(index)


def get_acc(instructs):
    ins_ptr = 0
    acc = 0
    ins_completed = []

    while True:
        #print(ins_ptr, ins, ins_completed)
        if ins_ptr in ins_completed:
            return (-1, False)
        if ins_ptr > len(instructs) - 1:
            return (acc, True)

        ins = instructs[ins_ptr]

        ins_completed.append(ins_ptr)
        if ins['ins'] == 'nop':
            ins_ptr += 1
        elif ins['ins'] == 'acc':
            acc += ins['offset']
            ins_ptr += 1
        elif ins['ins'] == 'jmp':
            ins_ptr += ins['offset']
        #print("ins=",ins['ins'],"ptr=",ins_ptr,"acc=",acc,"instructions=",instructs)
    return (-2, False)

for n_ptr in nj_ptrs:
    c_instructions = copy.deepcopy(instructions)
    swap_msg = ''
    if c_instructions[n_ptr]['ins'] == 'nop':
        c_instructions[n_ptr]['ins'] = 'jmp'
        swap_msg = 'nop -> jmp'
    elif c_instructions[n_ptr]['ins'] == 'jmp':
        c_instructions[n_ptr]['ins'] = 'nop'
        swap_msg = 'jmp -> nop'

    (acc, finished) = get_acc(c_instructions)
    if finished:
        print(f"finite loop: swapped {swap_msg} at instruction {n_ptr}")
        print("acc=",acc)
        break
    else:
        print(f"infinite loop: swapped {swap_msg} at instruction {n_ptr}")


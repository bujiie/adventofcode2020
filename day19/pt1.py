#!/usr/bin/env python3

import sys
import re
from copy import deepcopy
import collections

filename=sys.argv[1]

rules = {}
cases = []

is_rules = True

with open(filename) as fp:
    for index, line in enumerate(fp):
        cleaned_line = line.strip()

        if ':' in cleaned_line:
            words = cleaned_line.split()
            name = words[0][:-1]
            rest = ' '.join(words[1:]).replace('"','')
            if '|' in rest:
                rest = f'({rest})'
            elif len(rest) > 1:
                rest = f'{rest}'
            rules[name] = rest
        else:
            cases.append(cleaned_line)

def is_reduced(expr):
    return re.search(r'\d+', expr) == None

reduced = [i for i in rules if len(rules[i]) == 1]
used = []

while len(reduced) > 0:
    literal = reduced.pop(0)
    for key in rules:
        # print(key, literal, reduced, used)
        if key in [literal, *reduced, *used]:
            continue

        rule_list = rules[key].split(' ')

        for i, rule in enumerate(rule_list):
            regex = rf'^[()|]?{literal}[()|]?$'
            # print(i, rule, regex, re.match(regex, rule))
            if re.match(regex, rule) != None:
                # print('match found')
                # print("before=",rule_list[i])
                rule_list[i] = re.sub(rf'{literal}', rules[literal], rule)
                # print("after=",rule_list[i])

        rules[key] = ' '.join(rule_list)


        if is_reduced(rules[key]):
            reduced.append(key)
            continue
    used.append(literal)

for key in rules:
    rules[key] = rules[key].replace(' ','')

def matches(seq, rule):
    return re.match(rf'^{rule}$', seq) != None

print(rules)
ans = 0
for case in cases:
    if matches(case, rules['0']):
        ans += 1

print(ans)


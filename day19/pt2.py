#!/usr/bin/env python3

import sys
import re
import regex

from copy import deepcopy

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
            # 42: 19 84 | 62 47
            # 31: 121 84 | 77 47

            # 19: 3 47 | 13 84
            # 121: 99 47 | 27 84
            if name == '8':
                rest = '42 | 42 8'
            elif name == '11':
                rest = '42 31 | 42 11 31'
            else:
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
recursed = set()

while len(reduced) > 0:
    literal = reduced.pop(0)
    for key in rules:
        # print(key, literal, reduced, used)
        if key in [literal, *reduced, *used]:
            continue

        rule_list = rules[key].split(' ')

        for i, rule in enumerate(rule_list):
            # print('key=',key,'literal=',literal)
            if key == literal:
                print("key = literal")
                pattern = rf'^[()|]?(?R)[()|]?$'
            else:
                pattern = rf'^[()|]?{literal}[()|]?$'
            # print(i, rule, regex, re.match(pattern, rule))
            if re.match(pattern, rule) != None:
                # print('match found')
                # print("before=",rule_list[i])
                rule_list[i] = re.sub(rf'{literal}', rules[literal], rule)
                # print("after=",rule_list[i])

        rules[key] = ' '.join(rule_list)


        if is_reduced(rules[key]):
            print('reduced=',key)
            reduced.append(key)
            if key in recursed:
                recursed.remove(key)
            continue
        else:
            if key != '0':
                recursed.add(key)
    used.append(literal)

for key in recursed:
    rules[key] = re.sub(rf'{key}', '(?R)', rules[key])

rules['0'] = rules['8'] + rules['11']

for key in rules:
    rules[key] = rules[key].replace(' ','')

def matches(seq, rule):
    # print('='*40)
    # print('rule=',rule)
    # print('seq=',seq)
    return regex.match(rf'^{rule}$', seq) != None

print(rules)
ans = 0
for case in cases:
    if matches(case, rules['0']):
        ans += 1

print(ans)


#!/usr/bin/env python3

import sys
import re

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

            # if name == '8':
            #     rest = '42 | 42 8'
            # elif name == '11':
            #     rest = '42 31 | 42 11 31'
            # else:
            #     rest = ' '.join(words[1:]).replace(' | ', '|')

            rest = ' '.join(words[1:]).replace(' | ', '|')
            rules[name] = rest
        else:
            cases.append(cleaned_line)

def get_regex(rule_number, depth=0):
    # print(f"rule number={rule_number}")
    # print(f"get regex for={rules[rule_number]}")
    if rule_number == '8':
        return r8
    elif rule_number == '11':
        return r11
    return build_regex(rules[rule_number],depth)

def build_regex(rule, depth):
    # print('')
    # print('='*40)
    # print('depth=',depth)
    # print(f"rule={rule}")

    if '|' in rule:
        # print("pipe rule")
        left,right = rule.split('|')
        left_regexes = [get_regex(n,depth+1) for n in left.split(' ')]
        right_regexes = [get_regex(n,depth+1) for n in right.split(' ')]

        left_regex = '(' + ')('.join(left_regexes) + ')'
        right_regex = '(' + ')('.join(right_regexes) + ')'

        return f'({left_regex}|{right_regex})'
    elif '"' in rule:
        # print("literal", rule[1:-1])
        return rule[1:-1]
    else:
        # print("flat rule")
        regexes = [get_regex(n,depth+1) for n in rule.split(' ')]
        return '(' + ')('.join(regexes) + ')'

def matches(seq, rule_number):
    regex = get_regex(rule_number)
    # print(regex)
    return re.fullmatch(regex, seq) != None

r42 = get_regex('42')
r31 = get_regex('31')

r8 = f'({r42})+'

r11s =[]
for n in range(1, 20):
    r11s.append(f"({r42}){{{n}}}({r31}){{{n}}}")
r11 = "(" + ")|(".join([i for i in r11s]) + ")"

ans = 0
for case in cases:
    if matches(case, '0'):
        ans += 1

print(ans)


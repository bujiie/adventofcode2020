#!/usr/bin/env python3

import sys

filename=sys.argv[1]

E = []
with open(filename) as fp:
    for index, line in enumerate(fp):
         E.append(list(line.strip().replace(' ','')))

def exp(e):
    s = []
    i = 0
    while i < len(e):
        if e[i] == '(':
            (v, di) = exp(e[i+1:])
            s.append(v)
            i += di+1
        elif e[i] == ')':
            return (s, i+1)
        else:
            s.append(e[i])
            i += 1
    return (s, i)

def solve(e):
    ans = 0
    e.insert(0, '+')

    while len(e) > 0:

        [op, val] = e[:2]
        e = e[2:]
        if type(val) is list:
            val = solve(val)
        if op == '+':
            ans += int(val)
        elif op == '*':
            ans *= int(val)
    return ans


a = 0
for _,e in enumerate(E):
    (s, _) = exp(e)
    a += solve(s)

print(a)




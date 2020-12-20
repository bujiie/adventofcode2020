#!/usr/bin/env python3

import sys
from copy import deepcopy
from functools import reduce

filename=sys.argv[1]

equations = []
with open(filename) as fp:
    for index, line in enumerate(fp):
        equations.append(list(line.strip().replace(' ','')))

def term(eq, i):
    if eq[i] == '(':
        v, i_end = mul(eq, i+1)
        return (v, i_end+1)
    else:
        return(int(eq[i]), i+1)

def mul(eq, i):
    t, i_next = add(eq, i)
    ans = t

    while True:
        if i_next == len(eq) or eq[i_next] == ')':
            return ans, i_next
        else:
            t_next, i_more = add(eq, i_next+1)
            ans *= t_next
            i_next = i_more

def add(eq, i):
    t, i_next = term(eq, i)
    ans = t

    while True:
        if i_next == len(eq) or eq[i_next] == ')' or eq[i_next] == '*':
            return ans, i_next
        else:
            t_next, i_more = term(eq, i_next+1)
            ans += t_next
            i_next = i_more

def expr(eq, i):
    # get first term of expr
    t, i_next = term(eq, i)
    ans = t

    while True:
        if i_next == len(eq) or t == ')':
            return ans, i_next
        else:
            # i_next should put us at the operator
            t_next, i_more = term(eq, i_next+1)
            ans = evaluate(ans, t_next, eq[i_next])
            i_next = i_more

def evaluate(left, right, op):
    if op == '+':
        return left + right
    else:
        return left * right

def solve(eq):
    return mul(eq, 0)


ans = 0

for eq in equations:
    v, _ = solve(eq)
    ans += v

print(ans)





#!/usr/bin/env python3

from functools import reduce
import sys
import math


filename=sys.argv[1]

s=[]
with open(filename) as fp:
    for index, line in enumerate(fp):
        s=list(map(lambda n: 0 if n=='x' else int(n), line.strip().split(',')))

n=[]
a=[]
for k,v in enumerate(s):
    if v!=0:
        n.append(v)
        a.append(-k)

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod



def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


r=1
for x in n:
    r*=x

print(n,a,r,chinese_remainder(n,a))


#!/usr/bin/env python3

import sys
import re
import math
import itertools

filename=sys.argv[1]

def dec_to_bin(n):
    return bin(n).replace('0b','').zfill(36)

def bin_to_dec(n):
    return int(n,2)

p=[]
with open(filename) as fp:
    for index, line in enumerate(fp):
        if line.startswith('mask'):
            (_,mask)=list(map(lambda v: v.strip(),line.split('=')))
            p.append({'m':mask,'i':[]})
        else:
            matches = re.search(r'^mem\[(\d+)\]\s=\s(\d+)$',line.strip())
            (addr, dec) = matches.groups()
            dec=int(dec)
            o=[]
            x=[]
            for i,d in enumerate(p[-1]['m']):
                if d=='X':
                    x.append(i)
                elif d=='1':
                    o.append(i)
            b=list(dec_to_bin(int(addr)))
            for k,c in enumerate(b):
                if k in o:
                    b[k]=1
                if k in x:
                    b[k]='X'
            addrs=[]

            c=list(itertools.product([0,1],repeat=len(x)))
            addrs=[]
            for i in c:
                bc=b.copy()
                for j in range(0,len(x)):
                    bc[x[j]]=i[j]
                w=''.join(list(map(lambda c: str(c), bc)))
                addrs.append(w)
            p[-1]['i'].append({'addrs':addrs,'v':dec})

r={}
for s in p:
    for i in s['i']:
        for j in i['addrs']:
            if j not in r:
                r[j]=0
            r[j]=i['v']

a=0
for i in r:
    a+=r[i]
print(a)
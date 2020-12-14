#!/usr/bin/env python3

import sys
import re

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
            p[-1]['i'].append({'addr':addr,'dec':dec, 'bin': dec_to_bin(dec)})

r={}
for s in p:
    o=[]
    z=[]
    for i,d in enumerate(s['m']):
        if d=='0':
            z.append(i)
        elif d=='1':
            o.append(i)

    for i in s['i']:
        b=list(i['bin'])
        for k,c in enumerate(b):
            if k in o:
                b[k]=1
            elif k in z:
                b[k]=0
        w=''.join(list(map(lambda n: str(n), b)))
        r[i['addr']]=bin_to_dec(w)

a=0
for v in r.values():
    a+=v
print(a)

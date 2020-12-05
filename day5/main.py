#!/usr/bin/env python3

import sys

filename = sys.argv[1]
boarding_passes = []

with open(filename) as fp:
    boarding_passes = [bp.strip() for bp in fp.readlines()]    

print(boarding_passes)

        


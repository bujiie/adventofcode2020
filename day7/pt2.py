#!/usr/bin/env python3

import sys
import re
import functools

filename=sys.argv[1]

bags = {}
bags_cnt = {}

with open(filename) as fp:
    for index, line in enumerate(fp):
        clean_line = line.replace('.', '').strip()
        (outer_bag, inner_bags) = clean_line.split('contain')
        color = outer_bag.replace('bags', '').strip()
        bags[color] = {'total': 0, 'bags': []}

        # move to next rule if no bags can be placed inside
        if inner_bags.strip() == 'no other bags':
            continue

        for content in inner_bags.split(','):
            matches = re.search('^(\d+)(.*)$', content.strip())
            qty = int(matches[1].strip())
            bag_color = re.sub(r'bags?', '', matches[2].strip()).strip()

            bags[color]['bags'].append({'color': bag_color, 'qty': qty})
            bags[color]['total'] += qty


target = 'shiny gold'
queue = [{'color': target, 'qty': 1}]
count = 0
while queue:
    node = queue.pop(0)
    count = count + node['qty'] * bags[node['color']]['total']

    for inner_bag in bags[node['color']]['bags']:
        queue.append({'color': inner_bag['color'], 'qty':  node['qty'] * inner_bag['qty']})

print(count)

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

        (carrier, contents) = clean_line.split('contain')
        color = carrier.replace('bags', '').strip()
        bags[color] = []
        bags_cnt[color] = 0

        # move to next rule if no bags can be placed inside
        if contents.strip() != 'no other bags':
            for content in contents.split(','):
                results = re.search('^(\d+)(.*)$', content.strip())
                qty = results[1].strip()
                bag_color = re.sub(r'bags?', '', results[2].strip()).strip()
                bags[color].append({'color': bag_color, 'qty': int(qty)})
                bags_cnt[color] = bags_cnt[color] + int(qty)

target = 'shiny gold'


queue = [{'color': target, 'qty': 1}]
count = 0

while queue:
    node = queue.pop(0)
    count = count + node['qty'] * bags_cnt[node['color']]

    for inner_bag in bags[node['color']]:
        queue.append({'color': inner_bag['color'], 'qty':  node['qty'] * inner_bag['qty']})

print(count)

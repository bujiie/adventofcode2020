#!/usr/bin/env python3

import sys
import re

filename=sys.argv[1]

bags = {}
inner_bags = {}

def parse_bag_color(description):
    return description.replace('bags', '').strip()

with open(filename) as fp:
    for index, line in enumerate(fp):
        clean_line = line.replace('.', '').strip()

        (carrier, contents) = clean_line.split('contain')
        color = carrier.replace('bags', '').strip()
        bags[color] = []

        # move to next rule if no bags can be placed inside
        if contents.strip() != 'no other bags':
            for content in contents.split(','):
                results = re.search('^(\d+)(.*)$', content.strip())
                qty = results[1].strip()
                bag_color = re.sub(r'bags?', '', results[2].strip()).strip()
                bags[color].append(bag_color)

                if bag_color not in inner_bags:
                    inner_bags[bag_color] = []

                inner_bags[bag_color].append(color)

target = 'shiny gold'


options = set()

queue = [target]
visited = [target]
results = set()

while queue:
    node = queue.pop(0)

    for color in bags:
        bag_contents = bags[color]

        if node in bag_contents:
            results.add(color)

            if color not in visited:
                visited.append(color)
                queue.append(color)

print(len(results))

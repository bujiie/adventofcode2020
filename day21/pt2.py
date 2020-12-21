#!/usr/bin/env python3

import sys
import re
from copy import deepcopy

filename=sys.argv[1]

M = []
A = set()
I = set()

with open(filename) as fp:
    for index, line in enumerate(fp):
        matches = re.search(r'^([a-zz\s]+)(?:\(contains\s([a-z\s,]+)\))?', line.strip())
        i, a = matches.groups()

        ingredients = [n.strip() for n in i.split(' ') if len(n) > 0]
        allergens = [n.strip() for n in a.split(',') if len(n) > 0]

        A.update(set(allergens))
        I.update(set(ingredients))
        M.append((set(ingredients), set(allergens)))

AI = {}

res = {}
while len(res) < len(A):
    for allergen in A:
        for m_item in M:
            ingredients, allergens = m_item
            if allergen in allergens:
                if allergen not in AI:
                    AI[allergen] = ingredients
                else:
                    AI[allergen] = AI[allergen].intersection(ingredients)

            if allergen in AI:
                for ingredient in AI[allergen]:
                    if ingredient in res:
                        allergen_copy = deepcopy(AI[allergen])
                        allergen_copy.remove(ingredient)
                        AI[allergen] = allergen_copy

                if len(AI[allergen]) == 1:
                    e = next(iter(AI[allergen]))
                    res[e] = allergen

non_allergen_ingredients = I.difference(set(res.keys()))

ans = 0
for item in M:
    ingredients, _ = item

    for nai in non_allergen_ingredients:
        if nai in ingredients:
            ans += 1

inverse_res = {}
for ingredient in res:
    inverse_res[res[ingredient]] = ingredient

ans = []
for allergen in sorted(A):
    ans.append(inverse_res[allergen])

print(','.join(ans))


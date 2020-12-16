#!/usr/bin/env python3

import sys
import re

filename=sys.argv[1]

def search(string):
    matches = re.search(r'^(.*)\:\s(\d+)-(\d+)\sor\s(\d+)-(\d+)', string)
    if matches:
        return matches.groups()
    return None

rules={}
my_ticket_next = False
my_ticket = []
nearby_tickets_next = False
nearby_tickets = []
fields = []
with open(filename) as fp:
    for index, line in enumerate(fp):
        cleaned_line=line.strip()

        matches_rules = search(cleaned_line)
        if matches_rules:
            results = matches_rules
            l = list(range(int(results[1]), int(results[2])+1))
            k = list(range(int(results[3]), int(results[4])+1))
            rules[results[0]] = {'allowed': l+k}
            fields.append(results[0])

        matches_my_ticket = re.search(r'^your\sticket', cleaned_line)

        if my_ticket_next:
            my_ticket = list(map(lambda n: int(n.strip()), cleaned_line.split(',')))
            my_ticket_next = False
        if matches_my_ticket:
            my_ticket_next = True

        matches_nearby_tickets = re.search(r'^nearby\stickets', cleaned_line)
        if nearby_tickets_next:
            nearby_tickets.append(list(map(lambda n: int(n.strip()), cleaned_line.split(','))))
        if matches_nearby_tickets:
            nearby_tickets_next = True

allowed = set()
for i in rules:
    allowed.update(rules[i]['allowed'])

valid_tickets = []
for ticket in nearby_tickets:
    valid = True
    for n in ticket:
        if n not in allowed:
            valid = False
    if valid:
        valid_tickets.append(ticket)

cols=[]
for i in range(0, len(my_ticket)):
    cols.append([])

for ticket in valid_tickets:
    for i,n in enumerate(ticket):
        cols[i].append(n)

col_choices = {}
for i,col in enumerate(cols):
    if i not in col_choices:
        col_choices[i] = set(fields.copy())

    for num in col:
        for field in rules:
            if num not in rules[field]['allowed']:
                if field in col_choices[i]:
                    col_choices[i].remove(field)

choice_tuples = []
for i in col_choices:
    choice_tuples.append((i, len(col_choices[i]), col_choices[i]))

# (col, len, choices)
sorted_choice_tuples = sorted(choice_tuples, key=lambda c: c[1])

def set_difference(s1, s2):
    return s1.difference(s2)

field_tuples = []
locked_fields = set()
for s in sorted_choice_tuples:
    if len(s[2]) == 1:
        field = next(iter(s[2]))
    else:
        field = next(iter((s[2] - locked_fields)))
    locked_fields.add(field)
    field_tuples.append((s[0], field))

idx = []
for f in field_tuples:
    if f[1].startswith('departure'):
        idx.append(f)

r=1
for i in idx:
    r*=my_ticket[i[0]]

print(r)

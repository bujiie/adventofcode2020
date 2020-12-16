#!/usr/bin/env python3

import sys
import re

filename=sys.argv[1]

def search(str):
    matches = re.search(r'^(.*)\:\s(\d+)-(\d+)\sor\s(\d+)-(\d+)', str)
    return matches.groups()

rules={}
my_ticket_next = False
my_ticket = []
nearby_tickets_next = False
nearby_tickets = []
with open(filename) as fp:
    for index, line in enumerate(fp):
        cleaned_line=line.strip()

        matches_rules = re.search(r'^(class|row|seat)', cleaned_line)
        if matches_rules:
            results = search(cleaned_line)
            l = list(range(int(results[1]), int(results[2])+1))
            k = list(range(int(results[3]), int(results[4])+1))
            rules[results[0]] = {'allowed': l+k}

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

allowed = rules['class']['allowed'] + rules['row']['allowed'] + rules['seat']['allowed']
all_tickets = [my_ticket, *nearby_tickets]

err = []
for t in all_tickets:
    for n in t:
        if n not in allowed:
            err.append(n)

print(sum(err))


#!/usr/bin/env python3

import sys
from copy import deepcopy

filename=sys.argv[1]

p1 = []
p2 = []
p = []
with open(filename) as fp:
    for index, line in enumerate(fp):
        line = line.strip()
        if line.startswith('Player 1'):
            p = p1
            continue
        elif line.startswith('Player 2'):
            p = p2
            continue
        elif len(line) == 0:
            continue

        p.append(int(line))


def match_round(deck, round_history = {}):
    if len(deck) == 0:
        # end of the deck should also mean the end of the tree (empty object/no keys)
        return len(round_history.keys()) == 0

    top = deck[0]
    if top in round_history:
        return match_round(deck[1:], round_history[top])
    return False

def update_history(deck, history = {}):
    if len(deck) == 0:
        return history

    top = deck[0]
    if top in history:
        history[top] = update_history(deck[1:], history[top])
    else:
        history[top] = update_history(deck[1:], {})
    return history

def play(deck1, deck2, deck1_history = {}, deck2_history = {}, game=1):
    winner = None
    round_count = 1
    while len(deck1) > 0 and len(deck2) > 0:
        if match_round(deck1, deck1_history) or match_round(deck2, deck2_history):
            winner = 1
            break
        update_history(deck1, deck1_history)
        update_history(deck2, deck2_history)

        c1 = deck1.pop(0)
        c2 = deck2.pop(0)

        if len(deck1) >= c1 and len(deck2) >= c2:
            winner, _, _ = play(deepcopy(deck1[:c1]), deepcopy(deck2[:c2]), {}, {}, game+1)
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)

        round_count += 1
    return (winner, deck1, deck2)

play(p1, p2, {}, {})


# should still calculate the results for part2
p = p1 if len(p1) > 0 else p2
ans = 0
for i,c in enumerate(reversed(p)):
    ans += (c*(i+1))

print(ans)



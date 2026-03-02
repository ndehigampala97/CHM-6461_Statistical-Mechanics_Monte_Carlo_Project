#!/usr/bin/env python3

import math

def initial_straight_chain(N):
    return [(i, 0) for i in range(N)]


def is_neighbor(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def check_connectivity(coords):
    return all(is_neighbor(coords[i], coords[i+1]) for i in range(len(coords)-1))


def check_self_avoiding(coords):
   return len(coords) == len(set(coords))


def end_to_end_distance(coords):
    x0, y0 = coords[0]
    x1, y1 = coords[-1]
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)


if __name__ == "__main__":
    N = 6
    coords = initial_straight_chain(N)
    print("coords:", coords)
    print("Connectivity:", check_connectivity(coords))
    print("Self-avoiding:", check_self_avoiding(coords))
    print("R:", end_to_end_distance(coords))


def initial_straight_chain(N):

    coords = [(i, 0) for i in range(N)]
    occupied = {pos: i for i, pos in enumerate(coords)}
    return coords, occupied

def can_place(pos, occupied):
    return pos not in occupied


if __name__ == "__main__":
    N = 6
    coords, occupied = initial_straight_chain(N)
    print("coords:", coords)
    print("occupied keys:", list(occupied.keys()))


    test_pos = (2, 0)
    print("Can place at (2,0)?", can_place(test_pos, occupied))

    test_pos2 = (2, 1)
    print("Can place at (2,1)?", can_place(test_pos2, occupied))


import random

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def neighbors(p):
    x, y = p
    return [(x+dx, y+dy) for dx,dy in DIRS]


def initial_straight_chain(N):
    coords = [(i, 0) for i in range(N)]
    occupied = {pos:i for i,pos in enumerate(coords)}
    return coords, occupied

def propose_end_move(coords, occupied):
    N = len(coords)
    end_idx = 0 if random.random() < 0.5 else N-1
    anchor_idx = 1 if end_idx == 0 else N-2
    anchor = coords[anchor_idx]
    old_end = coords[end_idx]
    cands = [p for p in neighbors(anchor) if p != old_end and p not in occupied]

    if not cands:

        return None


    new_end = random.choice(cands)
    new_coords = coords.copy()
    new_coords[end_idx] = new_end
    new_occupied = occupied.copy()
    del new_occupied[old_end]
    new_occupied[new_end] = end_idx
    return new_coords, new_occupied


if __name__ == "__main__":
    random.seed(0)
    coords, occupied = initial_straight_chain(6)
    print("start:", coords)
    for k in range(10):

        prop = propose_end_move(coords, occupied)

        if prop is not None:

            coords, occupied = prop
        print(k, coords)

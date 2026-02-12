#!/usr/bin/env python3

import random

import math

from typing import Dict, List, Tuple, Optional



Pos = Tuple[int, int]

Coords = List[Pos]

Occupied = Dict[Pos, int]  # (x,y) -> bead index



DIRS: List[Pos] = [(1,0), (-1,0), (0,1), (0,-1)]





# ------------------------

# Basic lattice helpers

# ------------------------

def neighbors(p: Pos) -> List[Pos]:

    x, y = p

    return [(x + dx, y + dy) for dx, dy in DIRS]



def is_neighbor(a: Pos, b: Pos) -> bool:

    return abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1





# ------------------------

# State init (no boundaries)

# ------------------------

def initial_straight_chain(N: int) -> Tuple[Coords, Occupied]:

    coords = [(i, 0) for i in range(N)]

    occupied = {pos: i for i, pos in enumerate(coords)}

    return coords, occupied





# ------------------------

# Global validity checks (debug)

# ------------------------

def check_connectivity(coords: Coords) -> bool:

    for i in range(len(coords)-1):

        if not is_neighbor(coords[i], coords[i+1]):

            return False

    return True



def check_self_avoiding(coords: Coords) -> bool:

    return len(coords) == len(set(coords))





# ------------------------

# Observables (optional, good for debugging)

# ------------------------

def end_to_end_distance(coords: Coords) -> float:

    x0, y0 = coords[0]

    x1, y1 = coords[-1]

    dx, dy = x1-x0, y1-y0

    return math.sqrt(dx*dx + dy*dy)



def radius_of_gyration(coords: Coords) -> float:

    N = len(coords)

    xs = [x for x, _ in coords]

    ys = [y for _, y in coords]

    xcm = sum(xs)/N

    ycm = sum(ys)/N

    rg2 = sum((x-xcm)**2 + (y-ycm)**2 for x, y in coords)/N

    return math.sqrt(rg2)





# ------------------------

# Move proposals (SAW: accept any viable move)

# Each returns (new_coords, new_occupied) or None

# ------------------------

def propose_end_move(coords: Coords, occupied: Occupied) -> Optional[Tuple[Coords, Occupied]]:

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





def propose_corner_flip(coords: Coords, occupied: Occupied) -> Optional[Tuple[Coords, Occupied]]:

    N = len(coords)

    if N < 3:

        return None



    i = random.randrange(1, N-1)  # internal bead

    prev_p = coords[i-1]

    cur_p  = coords[i]

    next_p = coords[i+1]



    # must be connected already

    if not (is_neighbor(prev_p, cur_p) and is_neighbor(cur_p, next_p)):

        return None



    # reject straight line (prev-cur-next colinear)

    if (prev_p[0] == cur_p[0] == next_p[0]) or (prev_p[1] == cur_p[1] == next_p[1]):

        return None



    # flip position: the "other corner" of the rectangle

    new_p = (prev_p[0] + next_p[0] - cur_p[0], prev_p[1] + next_p[1] - cur_p[1])



    if new_p in occupied:

        return None



    new_coords = coords.copy()

    new_coords[i] = new_p



    new_occupied = occupied.copy()

    del new_occupied[cur_p]

    new_occupied[new_p] = i



    return new_coords, new_occupied





def propose_crankshaft(coords: Coords, occupied: Occupied) -> Optional[Tuple[Coords, Occupied]]:

    """

    2D crankshaft: flip a 2-bead segment (i, i+1) when endpoints (i-1) and (i+2) are neighbors.

    """

    N = len(coords)

    if N < 4:

        return None



    i = random.randrange(1, N-2)  # ensures i+2 exists

    a = coords[i-1]

    b = coords[i]

    c = coords[i+1]

    d = coords[i+2]



    if not is_neighbor(a, d):

        return None



    # 180-degree flip around midpoint of endpoints:

    new_b = (a[0] + d[0] - b[0], a[1] + d[1] - b[1])

    new_c = (a[0] + d[0] - c[0], a[1] + d[1] - c[1])



    # must keep bonds

    if not (is_neighbor(a, new_b) and is_neighbor(new_b, new_c) and is_neighbor(new_c, d)):

        return None



    # overlap check: allow moving beads to vacate their spots

    temp_occ = set(occupied.keys())

    temp_occ.discard(b)

    temp_occ.discard(c)



    if new_b in temp_occ or new_c in temp_occ:

        return None

    if new_b == new_c:

        return None



    new_coords = coords.copy()

    new_coords[i] = new_b

    new_coords[i+1] = new_c



    new_occupied = occupied.copy()

    del new_occupied[b]

    del new_occupied[c]

    new_occupied[new_b] = i

    new_occupied[new_c] = i+1



    return new_coords, new_occupied





# ------------------------

# Main Monte Carlo (SAW)

# ------------------------

def run_mc_saw(

    N: int = 6,

    n_steps: int = 20000,

    sample_every: int = 50,

    print_every: int = 1000,

    seed: int = 123,

    p_end: float = 0.4,

    p_corner: float = 0.4,

    p_crank: float = 0.2,

    debug_check_every: int = 2000,

):

    random.seed(seed)



    coords, occupied = initial_straight_chain(N)



    accepted = 0

    attempted = 0



    # store a few time series values (optional)

    steps, R_series, Rg_series = [], [], []



    def pick_move():

        r = random.random()

        if r < p_end:

            return propose_end_move

        elif r < p_end + p_corner:

            return propose_corner_flip

        else:

            return propose_crankshaft



    for step in range(1, n_steps + 1):

        move = pick_move()

        proposal = move(coords, occupied)

        if proposal is None:

            continue



        attempted += 1



        # SAW: energy = 0, so accept any viable move

        coords, occupied = proposal

        accepted += 1



        # sample observables

        if step % sample_every == 0:

            steps.append(step)

            R_series.append(end_to_end_distance(coords))

            Rg_series.append(radius_of_gyration(coords))



        # periodic printing

        if step % print_every == 0:

            acc = accepted / attempted if attempted else 0.0

            print(f"step {step:>6} | acc {acc:>6.3f} | R {end_to_end_distance(coords):.3f} | Rg {radius_of_gyration(coords):.3f}")

            print("coords:", coords)



        # debug checks (global)

        if debug_check_every and (step % debug_check_every == 0):

            if not check_connectivity(coords):

                raise RuntimeError("Connectivity violated (bug in move logic).")

            if not check_self_avoiding(coords):

                raise RuntimeError("Overlap detected (bug in occupancy checks).")



    print("\nDONE")

    print("Final coords:", coords)

    print("Connectivity:", check_connectivity(coords))

    print("Self-avoiding:", check_self_avoiding(coords))

    print("Acceptance ratio:", accepted / attempted if attempted else 0.0)



    return steps, R_series, Rg_series





if __name__ == "__main__":

    # Start small: 6 beads (recommended)

    run_mc_saw(

        N=6,

        n_steps=20000,

        sample_every=50,

        print_every=1000,

        seed=123

    )


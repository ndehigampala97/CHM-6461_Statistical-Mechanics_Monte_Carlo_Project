#!/usr/bin/env python3

"""

polymer6.py — 2D lattice polymer Monte Carlo (NO boundaries / infinite lattice)

SAW model (energy = 0) with move set:

  - end move

  - corner flip

  - crankshaft



Includes VMD visualization output:

  - writes traj.xyz (multi-frame XYZ)

  - recenters each frame so the polymer stays near the origin



Run:

  python3 polymer6.py



Visualize (on your local machine with VMD):

  vmd traj.xyz

Then in VMD console (optional):

  mol bondsrecalc top

"""



import random

import math

from typing import Dict, List, Tuple, Optional



Pos = Tuple[int, int]

Coords = List[Pos]

Occupied = Dict[Pos, int]  # (x,y) -> bead index



DIRS: List[Pos] = [(1, 0), (-1, 0), (0, 1), (0, -1)]





# ------------------------

# Basic lattice helpers

# ------------------------

def neighbors(p: Pos) -> List[Pos]:

    x, y = p

    return [(x + dx, y + dy) for dx, dy in DIRS]





def is_neighbor(a: Pos, b: Pos) -> bool:

    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1





# ------------------------

# Initialization (no boundaries)

# ------------------------

def initial_straight_chain(N: int) -> Tuple[Coords, Occupied]:

    coords = [(i, 0) for i in range(N)]

    occupied = {pos: i for i, pos in enumerate(coords)}

    return coords, occupied





# ------------------------

# Global validity checks (debug)

# ------------------------

def check_connectivity(coords: Coords) -> bool:

    for i in range(len(coords) - 1):

        if not is_neighbor(coords[i], coords[i + 1]):

            return False

    return True





def check_self_avoiding(coords: Coords) -> bool:

    return len(coords) == len(set(coords))





# ------------------------

# Observables

# ------------------------

def end_to_end_distance(coords: Coords) -> float:

    x0, y0 = coords[0]

    x1, y1 = coords[-1]

    dx, dy = x1 - x0, y1 - y0

    return math.sqrt(dx * dx + dy * dy)





def radius_of_gyration(coords: Coords) -> float:

    N = len(coords)

    xs = [x for x, _ in coords]

    ys = [y for _, y in coords]

    xcm = sum(xs) / N

    ycm = sum(ys) / N

    rg2 = sum((x - xcm) ** 2 + (y - ycm) ** 2 for x, y in coords) / N

    return math.sqrt(rg2)

def count_contacts(coords, occupied):

    """

    Count nonbonded nearest-neighbor contacts (i<j, |i-j|>1).

    """

    N = len(coords)

    contacts = 0

    seen = set()

    for i in range(N):

        x, y = coords[i]

        for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:

            j = occupied.get((nx, ny))

            if j is None:

                continue

            if j <= i:

                continue

            if abs(i - j) <= 1:

                continue

            pair = (i, j)

            if pair not in seen:

                seen.add(pair)

                contacts += 1

    return contacts





# ------------------------

# VMD output helpers

# ------------------------

def recenter(coords: Coords) -> Coords:

    """Shift polymer near (0,0) for visualization (does not affect physics)."""

    N = len(coords)

    xcm = sum(x for x, y in coords) / N

    ycm = sum(y for x, y in coords) / N

    sx = int(round(xcm))

    sy = int(round(ycm))

    return [(x - sx, y - sy) for x, y in coords]





def write_xyz_frame(fh, coords: Coords, frame_number: int):

    """Write one XYZ frame for VMD (2D coords are written with z=0)."""

    N = len(coords)

    fh.write(f"{N}\n")

    fh.write(f"Frame {frame_number}\n")

    for x, y in coords:

        fh.write(f"C {x:.3f} {y:.3f} 0.000\n")





# ------------------------

# Move proposals (return (new_coords, new_occupied) or None)

# ------------------------

def propose_end_move(coords: Coords, occupied: Occupied) -> Optional[Tuple[Coords, Occupied]]:

    N = len(coords)

    end_idx = 0 if random.random() < 0.5 else N - 1

    anchor_idx = 1 if end_idx == 0 else N - 2



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



    i = random.randrange(1, N - 1)  # internal bead

    prev_p = coords[i - 1]

    cur_p = coords[i]

    next_p = coords[i + 1]



    # must already be connected to neighbors

    if not (is_neighbor(prev_p, cur_p) and is_neighbor(cur_p, next_p)):

        return None



    # reject straight line

    if (prev_p[0] == cur_p[0] == next_p[0]) or (prev_p[1] == cur_p[1] == next_p[1]):

        return None



    # other corner of the rectangle

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

    2D crankshaft: flip a 2-bead segment (i, i+1) if endpoints (i-1) and (i+2) are neighbors.

    """

    N = len(coords)

    if N < 4:

        return None



    i = random.randrange(1, N - 2)  # ensures i+2 exists

    a = coords[i - 1]

    b = coords[i]

    c = coords[i + 1]

    d = coords[i + 2]



    if not is_neighbor(a, d):

        return None



    new_b = (a[0] + d[0] - b[0], a[1] + d[1] - b[1])

    new_c = (a[0] + d[0] - c[0], a[1] + d[1] - c[1])



    # bonds must remain valid

    if not (is_neighbor(a, new_b) and is_neighbor(new_b, new_c) and is_neighbor(new_c, d)):

        return None



    # overlap check: allow the two moved beads to vacate their positions

    temp_occ = set(occupied.keys())

    temp_occ.discard(b)

    temp_occ.discard(c)



    if new_b in temp_occ or new_c in temp_occ:

        return None

    if new_b == new_c:

        return None



    new_coords = coords.copy()

    new_coords[i] = new_b

    new_coords[i + 1] = new_c



    new_occupied = occupied.copy()

    del new_occupied[b]

    del new_occupied[c]

    new_occupied[new_b] = i

    new_occupied[new_c] = i + 1



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

    traj_path: str = "traj.xyz",

):

    random.seed(seed)



    coords, occupied = initial_straight_chain(N)



    accepted = 0

    attempted_total = 0      # every time we try to propose a move

    valid_proposals = 0      # proposals that return a valid new state



    # Open XYZ trajectory for VMD

    xyz = open(traj_path, "w")



    def pick_move():

        r = random.random()

        if r < p_end:

            return propose_end_move

        elif r < p_end + p_corner:

            return propose_corner_flip

        else:

            return propose_crankshaft



    for step in range(1, n_steps + 1):

        attempted_total += 1

        move = pick_move()

        proposal = move(coords, occupied)

        if proposal is None:

            continue



        valid_proposals += 1



        # SAW: energy = 0, so accept any viable move

        coords, occupied = proposal

        accepted += 1



        # write trajectory frames

        if step % sample_every == 0:

            vis_coords = recenter(coords)

            write_xyz_frame(xyz, vis_coords, step)



        # print progress

        if step % print_every == 0:

            valid_frac = valid_proposals / attempted_total if attempted_total else 0.0

            acc_given_valid = accepted / valid_proposals if valid_proposals else 0.0  # will be 1.0 for SAW

            print(

                f"step {step:>6} | valid {valid_frac:>6.3f} | acc(valid) {acc_given_valid:>6.3f} "

                f"| R {end_to_end_distance(coords):.3f} | Rg {radius_of_gyration(coords):.3f}"

            )

            print("coords:", coords)



        # occasional global checks

        if debug_check_every and (step % debug_check_every == 0):

            if not check_connectivity(coords):

                xyz.close()

                raise RuntimeError("Connectivity violated (bug in move logic).")

            if not check_self_avoiding(coords):

                xyz.close()

                raise RuntimeError("Overlap detected (bug in occupancy checks).")



    xyz.close()



    print("\nDONE")

    print("Final coords:", coords)

    print("Connectivity:", check_connectivity(coords))

    print("Self-avoiding:", check_self_avoiding(coords))

    print(f"Trajectory written to: {traj_path}")

    print(f"Open in VMD (local): vmd {traj_path}")

    return coords





if __name__ == "__main__":

    run_mc_saw(

        N=6,

        n_steps=20000,

        sample_every=50,     # write every 50 steps to traj.xyz

        print_every=1000,

        seed=123,

        traj_path="traj.xyz"

    )


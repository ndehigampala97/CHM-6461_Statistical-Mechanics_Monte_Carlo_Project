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

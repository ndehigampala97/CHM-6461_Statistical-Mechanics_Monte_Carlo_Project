from collections import Counter
import math
Epsilon = 1
kT = 0.6

"""
Analysis routines for HP lattice model.

Includes:
- energy calculation
- partition function
- entropy
- end-to-end distance

These functions are used by both enumeration and MC scripts.
"""

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def hp_contacts(path, sequence, Epsilon):
    """
    Returns the HP energy of a path.
    Each nonbonded H-H contact contributes -Epsilon.
    """
    E = 0
    n = len(path)

    for i in range(n):
        for j in range(i + 2, n):
            if sequence[i] == "H" and sequence[j] == "H":
                if manhattan(path[i], path[j]) == 1:
                    E -= Epsilon

    return E

def partition_function(all_paths, sequence, kT, Epsilon):
    Z = 0
    for path in all_paths:
        Z += math.exp(-hp_contacts(path, sequence, Epsilon)/kT)
    return Z

def probability(path, sequence, Z, kT, Epsilon):
    return math.exp(-hp_contacts(path, sequence, Epsilon)/kT) / Z

def cartesian_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def end_to_end(path):
    first_bead = path[0]
    last_bead = path[-1]
    return cartesian_distance(first_bead, last_bead)

def calculate_radius_of_gyration(path):
    n = len(path)
    x_cm = sum(p[0] for p in path) / n
    y_cm = sum(p[1] for p in path) / n

    rg2 = 0.0
    for x, y in path:
        rg2 += (x - x_cm) ** 2 + (y - y_cm) ** 2

    return math.sqrt(rg2 / n)
    
def radius_of_gyration(path):
    return calculate_radius_of_gyration(path)

def average_rg(paths, sequence, Epsilon, kT):
    Z = 0.0
    weighted = 0.0

    for path in paths:
        E = hp_contacts(path, sequence, Epsilon)
        rg = calculate_radius_of_gyration(path)

        w = math.exp(-E/kT)
        Z += w
        weighted += rg * w

    return weighted / Z

def entropy_term(path, sequence, Z, kT, Epsilon):
    """
    Returns p ln p for one microstate.
    """
    p = probability(path, sequence, Z, kT, Epsilon)
    return p * math.log(p)

def entropy_from_definition(expected_energy, Z, kT):
    """
    S =  <E>/kT + ln Z
    """
    return expected_energy/kT + math.log(Z)

def energies_of_paths(all_paths, sequence, Epsilon):
    energies = []
    for path in all_paths:
        energies.append(hp_contacts(path, sequence, Epsilon))
    return energies

def macrostates(all_paths, sequence, Epsilon):
    """
    Returns a Counter of energy degeneracies.
    """
    return Counter(energies_of_paths(all_paths, sequence, Epsilon))

def lowest_energy_microstates(paths, sequence, Epsilon):
    """
    Return:
        min_energy: lowest energy found
        lowest_paths: all microstates having that lowest energy
    """
    energies = []

    for path in paths:
        E = hp_contacts(path, sequence, Epsilon)
        energies.append((E, path))

    min_energy = min(E for E, path in energies)
    lowest_paths = [path for E, path in energies if E == min_energy]

    return min_energy, lowest_paths

def analyze_paths(all_paths, sequence, kT, Epsilon):
    """
    Run the same analysis from class and return the results in a dictionary.
    """
    Z = partition_function(all_paths, sequence, kT, Epsilon)

    sum_end2end = 0
    sum_rg = 0
    average_end2end = 0
    average_energy = 0
    entropy1 = 0
    energies = []

    for path in all_paths:
        e = hp_contacts(path, sequence, Epsilon)
        p = probability(path, sequence, Z, kT, Epsilon)
        r = end_to_end(path)
        rg = radius_of_gyration(path)

        sum_end2end += r
        sum_rg += rg
        average_end2end += p * r
        average_energy += p * e
        entropy1 -= entropy_term(path, sequence, Z, kT, Epsilon)
        energies.append(e)

    macro = Counter(energies)

    results = {
        "Z": Z,
        "n_paths": len(all_paths),
        "avg_end2end": sum_end2end / len(all_paths),
        "avg_rg": sum_rg / len(all_paths),
        "average_end2end": average_end2end,
        "average_energy": average_energy,
        "S1": entropy1,
        "S2": entropy_from_definition(average_energy, Z, kT),
        "macrostates": macro
    }

    return results

def read_trajectory(filename):
    """
    Read a trajectory written by mc.py.

    Returns
    -------
    trajectory : list of paths
        Each path is a list of (x,y) tuples
    energies : list of float
        Energy at each step
    """
    trajectory = []
    energies = []

    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split()

            step = int(parts[0])   # not used, but good to read explicitly
            energy = float(parts[1])

            path = []
            for item in parts[2:]:
                x, y = item.split(",")
                path.append((int(x), int(y)))

            trajectory.append(path)
            energies.append(energy)

    return trajectory, energies


def analyze_mc_trajectory(trajectory, energies):
    """
    Compute simple averages from a Monte Carlo trajectory.
    """
    sum_end2end = 0
    for path in trajectory:
        sum_end2end += end_to_end(path)

    avg_end2end = sum_end2end / len(trajectory)
    avg_energy = sum(energies) / len(energies)

    macro = Counter(energies)

    results = {
        "n_frames": len(trajectory),
        "avg_end2end": avg_end2end,
        "avg_energy": avg_energy,
        "macrostates": macro
    }

    return results

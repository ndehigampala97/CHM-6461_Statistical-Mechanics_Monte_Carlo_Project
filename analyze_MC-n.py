import sys

kT = 0.6
Epsilon = 1

from analysis import read_trajectory, analyze_mc_trajectory, analyze_paths
from enumeration import enumerate_paths

def canonical(path):
    """
    Shift the path so the first bead is at (0,0).
    This removes translation only.
    Rotations and reflections are kept distinct.
    """
    x0, y0 = path[0]
    return tuple((x - x0, y - y0) for (x, y) in path)

def first_coverage_step(sequence, trajectory):
    """
    Find the first MC step where all exact enumerated states
    have been sampled at least once.
    """
    exact_paths = enumerate_paths(sequence)
    exact_set = set(canonical(path) for path in exact_paths)

    visited = set()
    coverage_step = None

    for step, path in enumerate(trajectory):
        state = canonical(path)

        if state in exact_set:
            visited.add(state)

        if len(visited) == len(exact_set):
            coverage_step = step
            break

    return len(exact_set), len(visited), coverage_step, len(trajectory) - 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 analyze_and_cover_MC.py <sequence> <trajectory_file>")
        sys.exit()

    sequence = sys.argv[1]
    trajectory_file = sys.argv[2]

    print("Sequence:", sequence)
    print("Trajectory file:", trajectory_file)

    # Read MC trajectory
    trajectory, energies = read_trajectory(trajectory_file)

    # ----- MC sampled results -----
    mc_results = analyze_mc_trajectory(trajectory, energies)

    print("\nMC results")
    print("Frames:", mc_results["n_frames"])
    print("Average energy:", mc_results["avg_energy"])
    print("Average end2end:", mc_results["avg_end2end"])
    print("Sampled macrostates:", mc_results["macrostates"])

    # ----- Exact enumeration results -----
    possible_paths = enumerate_paths(sequence)
    exact_results = analyze_paths(possible_paths, sequence, kT, Epsilon)

    print("\nExact enumeration results")
    print("Number of exact paths:", exact_results["n_paths"])
    print("Average energy:", exact_results["average_energy"])
    print("Average end2end:", exact_results["average_end2end"])
    print("Exact macrostates:", exact_results["macrostates"])

    # ----- Coverage analysis -----
    n_exact, n_visited, coverage_step, total_steps = first_coverage_step(sequence, trajectory)

    print("\nCoverage analysis")
    print("Total exact states:", n_exact)
    print("Visited states:", n_visited)

    if coverage_step is None:
        print("All states found = False")
        print("Steps used =", total_steps)
    else:
        print("All states found = True")
        print("Steps used =", coverage_step)
import random
import math
import sys

from analysis import hp_contacts

moves = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

def add_vector(a, b):
    """
    Add two 2D vectors represented as tuples.
    """
    return (a[0] + b[0], a[1] + b[1])

def reptation_move(path):
    """
    Propose a reptation move.

    With probability 1/2:
        remove the last bead and grow a new bead at the head

    With probability 1/2:
        remove the first bead and grow a new bead at the tail

    A trial direction is chosen uniformly from R, L, U, D.
    If the new position overlaps with the shortened chain, the move is invalid.

    Returns
    -------
    trial_path : list of tuples
        Proposed new path if valid, otherwise the original path.
    valid_move : bool
        True if the proposed move is self-avoiding, False otherwise.
    """
    if random.random() < 0.5:
        # remove tail, grow at head
        shortened_path = path[:-1]
        growth_end = shortened_path[0]
        add_to_front = True
    else:
        # remove head, grow at tail
        shortened_path = path[1:]
        growth_end = shortened_path[-1]
        add_to_front = False

    move = random.choice(["R", "L", "U", "D"])
    step = moves[move]
    new_position = add_vector(growth_end, step)

    if new_position in shortened_path:
	#Here we overlap, so return the original and say that did not accept
        return path.copy(), False

    if add_to_front:
        trial_path = [new_position] + shortened_path
    else:
        trial_path = shortened_path + [new_position]

    return trial_path, True

def mc_step(path, sequence, Beta, Epsilon):
    """
    Perform one Monte Carlo step using reptation and Metropolis acceptance.

    Returns
    -------
    new_path : list of tuples
        Updated path after accept/reject.
    accepted : bool
        True if the move was accepted.
    valid_move : bool
        True if the proposed move was geometrically valid.
    """
    old_energy = hp_contacts(path, sequence, Epsilon)

    trial_path, valid_move = reptation_move(path)

    if not valid_move:
        return path, False, False

    new_energy = hp_contacts(trial_path, sequence, Epsilon)
    deltaE = new_energy - old_energy

    if deltaE <= 0:
        return trial_path, True, True

    if random.random() < math.exp(-Beta * deltaE):
        return trial_path, True, True

    return path, False, True

def run_mc(sequence, initial_path, n_steps, Beta, Epsilon):
    """
    Run a Monte Carlo simulation for an HP lattice polymer.

    Parameters
    ----------
    sequence : str
        HP sequence
    initial_path : list of tuples
        Starting conformation
    n_steps : int
        Number of Monte Carlo steps
    Beta : float
        Inverse temperature
    Epsilon : float
        H-H contact strength

    Returns
    -------
    trajectory : list
        List of sampled paths
    energies : list
        Energy at each step
    accepted_moves : int
        Number of accepted moves
    invalid_moves : int
        Number of invalid proposals
    """
    path = initial_path.copy()

    trajectory = [path.copy()]
    energies = [hp_contacts(path, sequence, Epsilon)]

    accepted_moves = 0
    invalid_moves = 0

    for step in range(n_steps):
        path, accepted, valid_move = mc_step(path, sequence, Beta, Epsilon)

        if accepted:
            accepted_moves += 1
        if not valid_move:
            invalid_moves += 1

        trajectory.append(path.copy())
        energies.append(hp_contacts(path, sequence, Epsilon))

    return trajectory, energies, accepted_moves, invalid_moves

def straight_path(sequence):
    """
    Build a simple straight initial conformation along x.
    """
    path = []
    for i in range(len(sequence)):
        path.append((i, 0))
    return path

def write_trajectory(trajectory, energies, filename="trajectory.txt"):
    """
    Write the Monte Carlo trajectory to a text file.

    Each line contains:
    step | energy | x0,y0 x1,y1 x2,y2 ...

    This format is easy to read back later for analysis.
    """
    with open(filename, "w") as f:
        for step, (path, energy) in enumerate(zip(trajectory, energies)):
            coords = " ".join(f"{x},{y}" for (x, y) in path)
            f.write(f"{step} {energy} {coords}\n")

if __name__ == "__main__":
    #If this script is the driver then execute the following
    Beta = 10.0 / 6.0
    Epsilon = 1

    sequence = sys.argv[1]
    n_steps = int(sys.argv[2])

    initial_path = straight_path(sequence)

    trajectory, energies, accepted_moves, invalid_moves = run_mc(
        sequence,
        initial_path,
        n_steps,
        Beta,
        Epsilon
    )

    write_trajectory(trajectory, energies)

    print("Sequence:", sequence)
    print("Initial path:", initial_path)
    print("Final path:", trajectory[-1])
    print("Final energy:", energies[-1])
    print("Accepted moves:", accepted_moves)
    print("Invalid moves:", invalid_moves)
    print("Acceptance ratio:", accepted_moves / n_steps)

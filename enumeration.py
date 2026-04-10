moves = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

def add_vector(a, b):
    return (a[0] + b[0], a[1] + b[1])

def enumerate_paths(sequence):
    """
    Exhaustively enumerate all self-avoiding walks for a sequence on a 2D lattice.

    To remove some symmetries:
    - first bead is fixed at (0,0)
    - second bead is fixed at (1,0)
    - the first turn is only allowed to be upward

    This means:
        start_path = [(0,0), (1,0)]

    We also exclude conformations with overlaps by tracking visited sites.
    """

    n = len(sequence)
    all_paths = []

    # For n = 1, just return the single bead at the origin
    if n == 1:
        return [[(0, 0)]]

    start_path = [(0, 0), (1, 0)]
    visited = {(0, 0), (1, 0)}
    first_turn_done = False

    def backtrack(path, visited, first_turn_done):
        if len(path) == n:
            all_paths.append(path.copy())
            return

        head = path[-1]

        if not first_turn_done:
            candidate_moves = ["R", "U"]
        else:
            candidate_moves = ["R", "L", "U", "D"]

        for move in candidate_moves:
            step = moves[move]
            new_position = add_vector(head, step)

            # Check overlap
            if new_position in visited:
                continue

            visited.add(new_position)
            path.append(new_position)

            if not first_turn_done and move == "U":
                backtrack(path, visited, True)
            else:
                backtrack(path, visited, first_turn_done)

            path.pop()
            visited.remove(new_position)

    backtrack(start_path, visited, first_turn_done)

    return all_paths

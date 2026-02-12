import numpy as np



def create_grid(L):

    """Create an LxL grid initialized to -1 (empty)."""

    return -1 * np.ones((L, L), dtype=int)



def place_straight_polymer(grid, N):

    """

    Place a straight polymer of length N in the middle row.

    Returns coords list of length N.

    """

    L = grid.shape[0]

    cy, cx = L // 2, L // 2  # center



    coords = []

    for i in range(N):

        x, y = cx + i, cy

        if grid[y, x] != -1:

            raise ValueError("Site already occupied — increase grid size.")

        grid[y, x] = i

        coords.append((x, y))



    return coords



def check_connectivity(coords):

    """Check consecutive monomers are nearest neighbors on lattice."""

    for i in range(len(coords) - 1):

        x1, y1 = coords[i]

        x2, y2 = coords[i+1]

        if abs(x1 - x2) + abs(y1 - y2) != 1:

            return False

    return True



def check_self_avoiding(coords):

    """No repeated lattice sites."""

    return len(coords) == len(set(coords))



# --- Example run ---

L = 60   # grid size

N = 20   # polymer length



grid = create_grid(L)

coords = place_straight_polymer(grid, N)



print("Connectivity:", check_connectivity(coords))

print("Self-avoiding:", check_self_avoiding(coords))

print("First few coords:", coords[:5])


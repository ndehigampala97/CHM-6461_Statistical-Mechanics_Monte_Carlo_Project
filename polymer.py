# 1. Define functions FIRST



def initialize_polymer(N):

    return [(i, 0) for i in range(N)]





def is_valid_polymer(polymer):

    # Rule 1: self-avoidance

    if len(set(polymer)) != len(polymer):

        return False



    # Rule 2: connectivity

    for i in range(len(polymer) - 1):

        x1, y1 = polymer[i]

        x2, y2 = polymer[i+1]

        if abs(x1 - x2) + abs(y1 - y2) != 1:

            return False



    return True





# 2. USE the functions AFTER they are defined



polymer = [(0, 0), (1, 0), (1, 1), (2, 1)]

print(polymer)

print(is_valid_polymer(polymer))

import enumeration
import analysis
import restrained_analysis
import sys

sequence = sys.argv[1]
Epsilon = 1
kT = 0.6
k_values = [0.1, 0.5, 1.0]

# Choose two beads far apart in sequence
# Python indexing starts from 0
# For length 8, bead_i=1 and bead_j=7 means bead 2 and bead 8
bead_i = 1
bead_j = 7

all_paths = enumeration.enumerate_paths(sequence)

# -----------------------------
# Unrestrained systems
# -----------------------------
results = analysis.analyze_paths(all_paths, sequence, kT, Epsilon)
avg_rg = analysis.average_rg(all_paths, sequence, Epsilon, kT)
min_energy, lowest_paths = analysis.lowest_energy_microstates(all_paths, sequence, Epsilon)

print("==================================================")
print("UNRESTRAINED SYSTEM")
print("==================================================")
print("Sequence =", sequence)
print("Number of conformations =", results["n_paths"])
print("Partition function =", results["Z"])
print("Average end-to-end distance =", results["avg_end2end"])
print("Average radius of gyration =", avg_rg)
print("Average end-to-end distance =", results["average_end2end"])
print("Average energy =", results["average_energy"])
print("Entropy S1 =", results["S1"])
print("Entropy S2 =", results["S2"])

print("\nMacrostates (Energy : Degeneracy)")
for energy in sorted(results["macrostates"]):
    print(f"{energy} : {results['macrostates'][energy]}")

print("Lowest energy =", min_energy)
print("Number of lowest-energy microstates =", len(lowest_paths))

for i in range(len(lowest_paths)):
    print("State", i + 1, "=", lowest_paths[i])

with open("trajectory_unrestrained.txt", "w") as f:
    for i, path in enumerate(all_paths, 1):
        energy = analysis.hp_contacts(path, sequence, Epsilon)
        f.write(f"Path {i}: {path} Energy = {energy}\n")
        
for k_force in k_values:
    restrained_results = restrained_analysis.analyze_paths_with_restraint(all_paths, sequence, kT, Epsilon, bead_i, bead_j, k_force)
    min_energy_r, lowest_paths_r, degeneracy_r = restrained_analysis.lowest_energy_microstates_with_restraint(all_paths, sequence, Epsilon, bead_i, bead_j, k_force)

    print("\n==================================================")
    print(f"RESTRAINED SYSTEM  (k = {k_force})")
    print("==================================================")
    print("Restrained beads (0-based indices) =", bead_i, bead_j)
    print("Restrained beads (human numbering) =", bead_i + 1, bead_j + 1)

    print("Partition function Z =", restrained_results["Z"])
    print("Average end-to-end distance =", restrained_results["avg_end2end"])
    print("Average radius of gyration =", restrained_results["average_rg"])
    print("Average end-to-end distance =", restrained_results["average_end2end"])
    print("Average energy =", restrained_results["average_energy"])
    print("Entropy S1 =", restrained_results["S1"])
    print("Entropy S2 =", restrained_results["S2"])

    if restrained_results["Z"] > results["Z"]:
        print("Comparison with unrestrained: Z increased")
    elif restrained_results["Z"] < results["Z"]:
        print("Comparison with unrestrained: Z decreased")
    else:
        print("Comparison with unrestrained: Z unchanged")

    print("\nRestrained macrostates (Energy : Degeneracy)")
    for energy in sorted(restrained_results["macrostates"]):
        print(f"{energy} : {restrained_results['macrostates'][energy]}")

    print("Lowest restrained energy =", min_energy_r)
    print("Degeneracy of lowest restrained energy =", degeneracy_r)
    print("Number of lowest-energy restrained microstates =", len(lowest_paths_r))
    for i in range(len(lowest_paths_r)):
        print("State", i + 1, "=", lowest_paths_r[i])

    print()
    

    all_paths = enumeration.enumerate_paths(sequence)

    with open("trajectory_all_k.txt", "w") as f:
         for k_force in k_values:
             f.write(f"\n===== k_force = {k_force} =====\n\n")

             for step, path in enumerate(all_paths, 1):
                 restraint_energy = restrained_analysis.calculate_energy_with_restraint(sequence, path, Epsilon, bead_i, bead_j, k_force)
                 f.write(f"Path {i}: {path} Energy = {restraint_energy}\n")

import math
import matplotlib.pyplot as plt
import enumeration
import analysis
import sys

Epsilon = 1
sequence = sys.argv[1]

temperatures = [0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0]

def calculate_Cv(paths, sequence, Epsilon, kT):
    Z = 0.0
    avg_E = 0.0
    avg_E2 = 0.0

    for path in paths:
        energy = analysis.hp_contacts(path, sequence, Epsilon)
        weight = math.exp(-energy / kT)

        Z += weight
        avg_E += energy * weight
        avg_E2 += energy * energy * weight

    avg_E /= Z
    avg_E2 /= Z

    Cv = (avg_E2 - avg_E * avg_E) / (kT * kT)
    return Cv

paths = enumeration.enumerate_paths(sequence)

T_values = []
Rg_values = []
Cv_values = []

for kT in temperatures:
    avg_rg = analysis.average_rg(paths, sequence, Epsilon, kT)
    Cv = calculate_Cv(paths, sequence, Epsilon, kT)

    T_values.append(kT)
    Rg_values.append(avg_rg)
    Cv_values.append(Cv)

print("Sequence =", sequence)
print()
print("Temperature    Average_Rg    Cv")

for i in range(len(T_values)):
    print(T_values[i], "   ", Rg_values[i], "   ", Cv_values[i])

print()

plt.figure()
plt.plot(T_values, Rg_values, marker='o')
plt.xlabel("Temperature (kT)")
plt.ylabel("Average Radius of Gyration")
plt.title("Average Rg vs Temperature for " + sequence)
plt.grid(True)
plt.savefig(sequence + "_Rg_vs_T.png")
plt.close()

plt.figure()
plt.plot(T_values, Cv_values, marker='o')
plt.xlabel("Temperature (kT)")
plt.ylabel("Cv")
plt.title("Cv vs Temperature for " + sequence)
plt.grid(True)
plt.savefig(sequence + "_Cv_vs_T.png")
plt.close()

print("Saved:", sequence + "_Rg_vs_T.png")
print("Saved:", sequence + "_Cv_vs_T.png")
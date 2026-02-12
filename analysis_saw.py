import csv

import matplotlib.pyplot as plt



steps = []

R = []

Rg = []

C = []



with open("saw_observables.csv", "r") as f:

    reader = csv.DictReader(f)

    for row in reader:

        steps.append(int(row["step"]))

        R.append(float(row["R"]))

        Rg.append(float(row["Rg"]))

        C.append(float(row["contacts"]))



# Burn-in removal (20%)

burn = int(0.2 * len(R))



R_avg = sum(R[burn:]) / len(R[burn:])

Rg_avg = sum(Rg[burn:]) / len(Rg[burn:])

C_avg = sum(C[burn:]) / len(C[burn:])



print("Final SAW averages (from CSV):")

print(f"<R>  = {R_avg:.4f}")

print(f"<Rg> = {Rg_avg:.4f}")

print(f"<contacts> = {C_avg:.4f}")



# Plot time series

plt.figure()

plt.plot(steps, R)

plt.xlabel("MC Step")

plt.ylabel("End-to-End Distance R")

plt.title("SAW: R vs MC step")

plt.show()



plt.figure()

plt.plot(steps, Rg)

plt.xlabel("MC Step")

plt.ylabel("Radius of Gyration Rg")

plt.title("SAW: Rg vs MC step")

plt.show()



plt.figure()

plt.plot(steps, C)

plt.xlabel("MC Step")

plt.ylabel("Contacts")

plt.title("SAW: Contacts vs MC step")

plt.show()


import csv

import numpy as np

import matplotlib.pyplot as plt



CSV_FILE = "saw_observables.csv"

BURN_FRAC = 0.2  # discard first 20% samples



# --- Load data ---

steps, R, Rg, C = [], [], [], []

with open(CSV_FILE, "r") as f:

    reader = csv.DictReader(f)

    for row in reader:

        steps.append(int(row["step"]))

        R.append(float(row["R"]))

        Rg.append(float(row["Rg"]))

        C.append(float(row["contacts"]))



steps = np.array(steps)

R = np.array(R)

Rg = np.array(Rg)

C = np.array(C)



burn = int(BURN_FRAC * len(steps))

steps_p = steps[burn:]

R_p = R[burn:]

Rg_p = Rg[burn:]

C_p = C[burn:]



print(f"Loaded {len(steps)} samples. Burn-in removed: {burn} samples. Production: {len(steps_p)} samples.")

print(f"<R>  = {R_p.mean():.4f}")

print(f"<Rg> = {Rg_p.mean():.4f}")

print(f"<C>  = {C_p.mean():.4f}")



# --- Helper: running mean ---

def running_mean(x):

    return np.cumsum(x) / np.arange(1, len(x)+1)



# --- Plot 1: R vs step ---

plt.figure()

plt.plot(steps, R)

plt.axvline(steps[burn], linestyle="--")

plt.xlabel("MC step")

plt.ylabel("End-to-end distance R")

plt.title("SAW: R vs MC step")

plt.tight_layout()

plt.savefig("SAW_R_vs_step.png", dpi=200)



# --- Plot 2: Rg vs step ---

plt.figure()

plt.plot(steps, Rg)

plt.axvline(steps[burn], linestyle="--")

plt.xlabel("MC step")

plt.ylabel("Radius of gyration Rg")

plt.title("SAW: Rg vs MC step")

plt.tight_layout()

plt.savefig("SAW_Rg_vs_step.png", dpi=200)



# --- Plot 3: Contacts vs step ---

plt.figure()

plt.plot(steps, C)

plt.axvline(steps[burn], linestyle="--")

plt.xlabel("MC step")

plt.ylabel("Nonbonded contacts")

plt.title("SAW: contacts vs MC step")

plt.tight_layout()

plt.savefig("SAW_contacts_vs_step.png", dpi=200)



# --- Plot 4: Histogram of R (production only) ---

plt.figure()

plt.hist(R_p, bins=20)

plt.xlabel("R")

plt.ylabel("Count")

plt.title("SAW: Histogram of R (production)")

plt.tight_layout()

plt.savefig("SAW_hist_R.png", dpi=200)



# --- Plot 5: Histogram of Rg (production only) ---

plt.figure()

plt.hist(Rg_p, bins=20)

plt.xlabel("Rg")

plt.ylabel("Count")

plt.title("SAW: Histogram of Rg (production)")

plt.tight_layout()

plt.savefig("SAW_hist_Rg.png", dpi=200)



# --- Plot 6: Running mean (convergence) ---

plt.figure()

plt.plot(steps, running_mean(R))

plt.axvline(steps[burn], linestyle="--")

plt.xlabel("MC step")

plt.ylabel("Running mean of R")

plt.title("SAW: Running mean of R (convergence)")

plt.tight_layout()

plt.savefig("SAW_runningmean_R.png", dpi=200)



plt.figure()

plt.plot(steps, running_mean(Rg))

plt.axvline(steps[burn], linestyle="--")

plt.xlabel("MC step")

plt.ylabel("Running mean of Rg")

plt.title("SAW: Running mean of Rg (convergence)")

plt.tight_layout()

plt.savefig("SAW_runningmean_Rg.png", dpi=200)



print("\nSaved plot files:")

print("  SAW_R_vs_step.png")

print("  SAW_Rg_vs_step.png")

print("  SAW_contacts_vs_step.png")

print("  SAW_hist_R.png")

print("  SAW_hist_Rg.png")

print("  SAW_runningmean_R.png")

print("  SAW_runningmean_Rg.png")


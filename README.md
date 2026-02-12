# CHM 6461 – Statistical Mechanics Monte Carlo Project
## 2D Lattice Polymer Simulation (Work in Progress)
  
Course: CHM 6461 – Statistical Mechanics  
Model: 2D Lattice Polymer (SAW + HP Model)

---

##  Project Overview

This project implements a 2D lattice polymer Monte Carlo simulation to study:

- Self-Avoiding Walk (SAW) model
- HP lattice protein model (hydrophobic–polar model)
- Polymer conformational statistics
- Thermodynamic properties via Monte Carlo sampling

The simulation uses local Monte Carlo moves and samples polymer conformations on an infinite 2D lattice.

---

## Current Progress

### Implemented: SAW Model

- 2D square lattice representation
- Self-avoiding constraint (no bead overlap)
- Move set:
  - End move
  - Corner flip
  - Crankshaft move
- Observables:
  - End-to-end distance (R)
  - Radius of gyration (Rg)
  - Non-bonded contact count
- Trajectory output in XYZ format for VMD visualization
- CSV export for statistical analysis


## Monte Carlo Algorithm

Each Monte Carlo step:

1. Select a move type (end / corner / crankshaft)
2. Generate a proposed configuration
3. Check viability (no overlap, connectivity preserved)
4. Accept valid configuration (SAW stage)
5. Sample observables at fixed frequency


##  Observables

- End-to-end distance:
- Radius of gyration:
- Nonbonded contacts (|i − j| > 1)

---

## Files

- `polymer6.py` – Main SAW Monte Carlo implementation
- `analysis_saw.py` – Observable analysis script
- `plot_saw.py` – Plot generation
- `traj.xyz` – VMD trajectory output (not tracked)
- `saw_observables.csv` – Simulation data (not tracked)

---

##  Next Steps

- Implement HP model energy:
- Add Metropolis acceptance criterion
- Perform temperature sweep
- Compute heat capacity:
- Compare SAW vs HP behavior
- Analyze folding transition

---

## Visualization

Trajectory can be visualized using VMD:




---
id: SIM-2026-007
title: CAV-02 eigenmode sweep, rod 0–180°
type: simulation
access: public
created: 2026-10-09
authors: ["[[Michael Sekatchev]]"]
project: "[[Cavity R&D]]"
apparatus: "[[CAV-02 Tunable copper cavity]]"
cad_revision: "[[CAD-CAV02-001 Cavity barrel]] rev C + [[CAD-CAV02-002 Tuning rod]] rev A"
software: CST Studio Suite 2025 SP2
solver: Eigenmode (AKS), 10 modes
mesh: tetrahedral, curved elements order 2, ~180k tets, adaptive 4 passes (Δf < 0.1 MHz)
boundaries: copper surface impedance σ = 5.8e7 S/m, symmetry plane off
sweep: rod angle 0–180° in 4° steps
storage_path: groupstore://cavity/sim/SIM-2026-007/CAV-02_revC_sweep.cst
files:
  - "[[SIM-2026-007_CAV-02_eigenmode_th000-180deg_results.csv]]"
  - "[[SIM-2026-007_CAV-02_eigenmode_th000-180deg.png]]"
status: complete
synthetic: true
tags: [simulation, CST, CAV-02]
---

# SIM-2026-007 CAV-02 eigenmode sweep

![[SIM-2026-007_CAV-02_eigenmode_th000-180deg.png]]

## Result
- Reproduces the avoided crossing seen in [[MEAS-2026-013 CAV-02 mode map]], in the same place (112°).
- The **form factor C010 falls from about 0.62 to 0.16 at the crossing**. That bin is effectively lost for an axion search unless the intruder mode is moved.
- Frequencies run about 4 MHz below measurement, see [[ANA-2026-004 Sim vs measured tuning curve]].

## Reproducing
The CST project file (≈ 2 GB including results) is on group storage at the `storage_path` shown to group members. The results CSV in this record holds everything needed to make the plots.

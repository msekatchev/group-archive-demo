---
id: MEAS-2026-015
title: CAV-02 bead-pull, TM010 at rod angle 112°
type: measurement
method: bead-pull
access: public
created: 2026-10-07
authors: ["[[Michael Sekatchev]]"]
project: "[[Cavity R&D]]"
apparatus: "[[CAV-02 Tunable copper cavity]]"
instrument: "[[VNA-01 Vector network analyzer]]"
rig: "[[BPR-01 Bead-pull rig]]"
procedure: "[[PROC-001 Bead-pull measurement]]"
cad_revision: "[[CAD-CAV02-001 Cavity barrel]] rev C"
date: 2026-10-07
operator: "[[Michael Sekatchev]]"
mode: TM010-like (upper hybrid branch)
rod_angle_deg: 112
frequency_GHz: 5.5698
temperature_K: 295
atmosphere: lab air, 1 atm, RH 40%
bead: B-PTFE-3 (PTFE sphere, Ø3.18 mm)
bead_path: on axis (r = 0), z = 0 → 254 mm, 201 steps
vna_power_dBm: 0
vna_ifbw_Hz: 1000
files:
  - "[[MEAS-2026-015_CAV-02_beadpull_th112deg.png]]"
  - "[[MEAS-2026-015_CAV-02_beadpull_th112deg_proc.csv]]"
raw_data:
  location: groupstore://cavity/raw/2026/MEAS-2026-015/MEAS-2026-015_CAV-02_beadpull_th112deg_raw.csv
  sha256: 6af5ab4d6491cd8b949c8d4e86c2d309dce44f5ddc82edf7efe7f16435ae91bc
  size: 4.6 kB
status: complete
synthetic: true
tags: [measurement, bead-pull, CAV-02]
---

# MEAS-2026-015 CAV-02 bead-pull at 112°

**Purpose:** field profile at the avoided crossing seen in [[MEAS-2026-013 CAV-02 mode map]].

![[MEAS-2026-015_CAV-02_beadpull_th112deg.png]]

## Result
The field is **strongly tilted**: E² is maximal at the z = 0 end cap and almost zero beyond z ≈ 160 mm. This fits a roughly 50/50 mix of TM010 with a mode that varies along z, and it means the form factor collapses at this angle. Quantified in [[SIM-2026-007 CAV-02 eigenmode sweep]] and discussed in [[TM-2026-003 Mode mixing near 112 deg in CAV-02]].

> [!tip] Why the metadata matters
> Without `rod_angle_deg`, `bead`, `cad_revision` and `frequency_GHz`, this plot could not be told apart from a broken bead line. The validator refuses to accept a bead-pull record that lacks those fields.

---
id: MEAS-2026-014
title: CAV-02 bead-pull, TM010 at rod angle 60°
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
mode: TM010-like
rod_angle_deg: 60
frequency_GHz: 5.1295
temperature_K: 295
atmosphere: lab air, 1 atm, RH 40%
bead: B-PTFE-3 (PTFE sphere, Ø3.18 mm)
bead_path: on axis (r = 0), z = 0 → 254 mm, 201 steps
vna_power_dBm: 0
vna_ifbw_Hz: 1000
files:
  - "[[MEAS-2026-014_CAV-02_beadpull_th060deg.png]]"
  - "[[MEAS-2026-014_CAV-02_beadpull_th060deg_proc.csv]]"
raw_data:
  location: groupstore://cavity/raw/2026/MEAS-2026-014/MEAS-2026-014_CAV-02_beadpull_th060deg_raw.csv
  sha256: 7ce31365dff93d3149a4a75a1ca122aabad2a7b53b08a47bc17a58b1656c83b4
  size: 4.6 kB
status: complete
synthetic: true
tags: [measurement, bead-pull, CAV-02]
---

# MEAS-2026-014 CAV-02 bead-pull at 60°

**Purpose:** reference field profile on the low side of the 112° crossing seen in [[MEAS-2026-013 CAV-02 mode map]].

![[MEAS-2026-014_CAV-02_beadpull_th060deg.png]]

## Result
The on-axis E² profile is **flat to within about 2%** over the full length: a clean TM010 mode. Peak shift is −42 kHz, consistent with the 2026-01 empty-cavity calibration of bead B-PTFE-3.

Compare with [[MEAS-2026-015 CAV-02 bead-pull at 112 deg]].

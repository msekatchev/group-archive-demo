---
id: MEAS-2026-013
title: CAV-02 mode map, rod 0–180°
type: measurement
method: mode-map
access: public
created: 2026-10-06
authors: ["[[Michael Sekatchev]]"]
project: "[[Cavity R&D]]"
apparatus: "[[CAV-02 Tunable copper cavity]]"
instrument: "[[VNA-01 Vector network analyzer]]"
procedure: "[[PROC-002 Mode map acquisition]]"
cad_revision: "[[CAD-CAV02-001 Cavity barrel]] rev C"
date: 2026-10-06
operator: "[[Michael Sekatchev]]"
rod_angle_range_deg: 0–180
rod_angle_step_deg: 1
freq_range_GHz: 4.80–6.10
temperature_K: 295
atmosphere: lab air, 1 atm, RH 41%
vna_power_dBm: 0
vna_ifbw_Hz: 1000
vna_points: 2601
vna_calibration: "2026-09-15 SOLT (see [[VNA-01 Vector network analyzer]])"
files:
  - "[[MEAS-2026-013_CAV-02_modemap_th000-180deg.png]]"
  - "[[MEAS-2026-013_CAV-02_modemap_th000-180deg_peaks.csv]]"
raw_data:
  location: groupstore://cavity/raw/2026/MEAS-2026-013/MEAS-2026-013_CAV-02_modemap_th000-180deg_raw.npz
  sha256: 5f519fd225b52d6e3a7266bca8b9e91ff376764f0fc1b0b0802d05476cfb9023
  size: 1.5 MB
  public_copy: "[[DATA-2026-001 CAV-02 tuning characterization]]"
status: complete
synthetic: true
tags: [measurement, mode-map, CAV-02]
---

# MEAS-2026-013 CAV-02 mode map

**Purpose:** baseline tuning curve of CAV-02 after the barrel was swapped for rev C, and a search for mode crossings in the tuning range.

![[MEAS-2026-013_CAV-02_modemap_th000-180deg.png]]

## Observations
- The TM010-like mode tunes from 4.950 GHz (0°) to 5.902 GHz (180°), with loaded Q ≈ 11 000 at room temperature.
- **Avoided crossing at about 112°** with a weakly coupled, nearly flat TE-like mode at 5.556 GHz. The minimum splitting is about 28 MHz, and at that point the two branches share the TM010 character roughly 50/50.
- A TM011-like mode runs about 420 MHz above TM010 across the whole range, and a second TE-like line slopes down from 5.93 GHz. Neither interacts with TM010.

## Follow-up
- Bead-pulls on either side of the crossing: [[MEAS-2026-014 CAV-02 bead-pull at 60 deg]] and [[MEAS-2026-015 CAV-02 bead-pull at 112 deg]]
- Compared with simulation in [[ANA-2026-004 Sim vs measured tuning curve]]

## Files
- `…_peaks.csv`: output of peak-finder v1.2, with columns `rod_angle_deg, mode_label, f_GHz, Q_loaded, S21_peak_dB`
- The raw |S21|(f, θ) grid (1.5 MB) is on group storage (location and checksum in the metadata above), with a public copy in [[DATA-2026-001 CAV-02 tuning characterization]].

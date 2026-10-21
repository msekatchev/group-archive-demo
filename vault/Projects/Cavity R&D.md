---
id: PRJ-CAVITY
title: Cavity R&D
type: project
access: public
created: 2026-10-21
authors: ["[[Karl]]"]
lead: "[[Karl]]"
status: active
funding: "DOE award DE-SC00XXXXX (placeholder)"
tags: [project, cavity]
---

# Cavity R&D

Development and characterization of tunable microwave cavities for haloscope searches.

## Hardware
- [[CAV-02 Tunable copper cavity]]: single off-axis copper tuning rod, about 4.95–5.90 GHz
- [[BPR-01 Bead-pull rig]]
- [[VNA-01 Vector network analyzer]]

## Current thread: the 112° mode crossing
1. Mode map [[MEAS-2026-013 CAV-02 mode map]] shows an avoided crossing near 112°.
2. Bead-pulls at 60° ([[MEAS-2026-014 CAV-02 bead-pull at 60 deg]]) and 112° ([[MEAS-2026-015 CAV-02 bead-pull at 112 deg]]) show the TM010 field going from flat to strongly tilted.
3. Simulation [[SIM-2026-007 CAV-02 eigenmode sweep]] reproduces the crossing, and the form factor drops to about 0.16 there.
4. Comparison [[ANA-2026-004 Sim vs measured tuning curve]] finds a +4.1 MHz offset between measurement and simulation.
5. Write-up: [[TM-2026-003 Mode mixing near 112 deg in CAV-02]] → [[PUB-2026-001 Mode-crossing mitigation in a tunable copper cavity]]
6. Public data release: [[DATA-2026-001 CAV-02 tuning characterization]]

## Older work
- [[PBG-01 Photonic band gap cavity]] and [[LEGACY-2019-002 PBG-01 mode map (recovered)]]

---
id: TM-2026-003
title: Mode mixing near 112° in CAV-02
type: memo
access: collaboration
created: 2026-10-14
authors: ["[[Michael Sekatchev]]"]
reviewed_by: "[[Karl]]"
project: "[[Cavity R&D]]"
status: final
tags: [memo, CAV-02]
---

# TM-2026-003 Mode mixing near 112° in CAV-02

**Summary.** The TM010-like mode of CAV-02 has an avoided crossing with a TE-like intruder at 5.556 GHz (rod angle ≈ 112°). The two hybridize, the on-axis field tilts strongly and C010 drops to about 0.16 over a band of roughly ±3°. We recommend a dielectric shim near the z = 254 mm end cap to push the intruder up by about 40 MHz. To be tested.

## Evidence
1. Mode map: [[MEAS-2026-013 CAV-02 mode map]]
2. Bead-pulls: [[MEAS-2026-014 CAV-02 bead-pull at 60 deg]] (flat) vs [[MEAS-2026-015 CAV-02 bead-pull at 112 deg]] (tilted)
3. Simulation: [[SIM-2026-007 CAV-02 eigenmode sweep]]
4. Systematic offset: [[ANA-2026-004 Sim vs measured tuning curve]]

## Next steps
- [ ] Simulate shim positions (SIM-2026-008)
- [ ] Repeat the mode map after the shim is installed
- [ ] Fold into the paper draft [[PUB-2026-001 Mode-crossing mitigation in a tunable copper cavity]]

First shown at [[MTG-2026-10-08 Group meeting]].

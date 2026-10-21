---
id: PROC-001
title: Bead-pull measurement
type: procedure
access: public
created: 2025-12-01
authors: ["[[Michael Sekatchev]]"]
version: 1.2 (2026-09-20)
applies_to: ["[[BPR-01 Bead-pull rig]]", "[[CAV-02 Tunable copper cavity]]"]
tags: [procedure, bead-pull]
---

# PROC-001 Bead-pull measurement (v1.2)

1. Let the cavity and VNA warm up for 30 min. Log temperature and humidity.
2. Check the VNA calibration date ([[VNA-01 Vector network analyzer]]). Recalibrate if it is older than 30 days.
3. Set the rod angle. Find the mode, and record `frequency_GHz` and the loaded Q with the bead parked outside the cavity.
4. Settings: 0 dBm, IF bandwidth 1 kHz, span 5× linewidth, 201 points.
5. Thread the bead (default B-PTFE-3) and zero it at z = 0, the port-1 end cap.
6. Run `beadpull.py --steps 201 --length 254`. It writes `<ID>_..._raw.csv`.
7. Park the bead outside again and re-measure f0. Drift must be under 5 kHz; otherwise repeat.
8. Create the record from the **Measurement (bead-pull)** template.

## Changes
| Version | Date | Change |
| --- | --- | --- |
| 1.2 | 2026-09-20 | Added drift check (step 7) |
| 1.1 | 2026-02-10 | Humidity logging |
| 1.0 | 2025-12-01 | First version |

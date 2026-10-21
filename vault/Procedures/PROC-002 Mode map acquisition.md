---
id: PROC-002
title: Mode map acquisition
type: procedure
access: public
created: 2026-01-15
authors: ["[[Michael Sekatchev]]"]
version: 1.0 (2026-01-15)
applies_to: ["[[CAV-02 Tunable copper cavity]]", "[[VNA-01 Vector network analyzer]]"]
tags: [procedure, mode-map]
---

# PROC-002 Mode map acquisition (v1.0)

1. Warm up and check calibration as in [[PROC-001 Bead-pull measurement]], steps 1–2.
2. Settings: 0 dBm, IF bandwidth 1 kHz, 2601 points over the full tuning range.
3. Home the rod stage at 0°. Step in 1° increments with a 2 s settle time.
4. Save the full |S21| grid as `<ID>_<apparatus>_modemap_<range>_raw.npz` on group storage.
5. Run `peakfind.py` to get the peak table and figure, and attach them to the record.

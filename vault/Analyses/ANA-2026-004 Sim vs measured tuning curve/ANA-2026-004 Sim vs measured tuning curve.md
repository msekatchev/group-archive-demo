---
id: ANA-2026-004
title: CAV-02 tuning, simulation vs measurement
type: analysis
access: public
created: 2026-10-12
authors: ["[[Michael Sekatchev]]"]
reviewed_by: "[[Karl]]"
project: "[[Cavity R&D]]"
inputs:
  - "[[MEAS-2026-013 CAV-02 mode map]]"
  - "[[SIM-2026-007 CAV-02 eigenmode sweep]]"
code: "[[ANA-2026-004_compare_sim_meas.py]]"
files:
  - "[[ANA-2026-004_CAV-02_tuning_sim-vs-meas.png]]"
status: complete
synthetic: true
tags: [analysis, CAV-02]
---

# ANA-2026-004 Sim vs measured tuning curve

![[ANA-2026-004_CAV-02_tuning_sim-vs-meas.png]]

## Result
Measured frequencies sit **+4.1 MHz above simulation** with a slight angle dependence (a 0.9 MHz spread). That fits a bore about 0.03 mm smaller than nominal, which is within the rev C tolerance. No sign of a mis-modelled rod position.

## Reproduce it
The script reads only the CSVs in the two input records:

```bash
python "vault/Analyses/ANA-2026-004 Sim vs measured tuning curve/ANA-2026-004_compare_sim_meas.py"
```

Because the code, inputs and figure sit together under one ID, the plot in a paper can always be traced back to the exact data and code that made it.

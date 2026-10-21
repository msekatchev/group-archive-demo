---
id: BPR-01
title: BPR-01 Bead-pull rig
type: apparatus
access: public
created: 2025-12-01
authors: ["[[Michael Sekatchev]]"]
project: "[[Cavity R&D]]"
location: Cavity lab, bench 2
responsible: "[[Michael Sekatchev]]"
status: in service
tags: [apparatus, bead-pull]
---

# BPR-01 Bead-pull rig

A stepper-driven fishing-line stage that pulls a dielectric bead along the cavity axis while the [[VNA-01 Vector network analyzer]] tracks the resonant frequency. Operating procedure: [[PROC-001 Bead-pull measurement]].

```mermaid
flowchart LR
    M[Stepper motor<br/>0.1 mm/step] -->|nylon line, 0.2 mm| B((PTFE bead<br/>Ø3.18 mm))
    B --> C[CAV-02 bore]
    C -->|port 1| V[VNA-01]
    C -->|port 2| V
    V -->|f_res per step| P[DAQ laptop<br/>beadpull.py v2.1]
    P --> M
```

## Bead inventory

| Bead | Material | Diameter | Use |
| --- | --- | --- | --- |
| B-PTFE-3 | PTFE | 3.18 mm | E-field, default |
| B-AL-3 | aluminum | 3.18 mm | E + H field |
| B-PTFE-6 | PTFE | 6.35 mm | low-signal modes |

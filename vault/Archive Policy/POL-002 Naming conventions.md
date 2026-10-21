---
id: POL-002
title: Naming conventions
type: policy
access: public
created: 2026-10-21
authors: ["[[Megan]]", "[[Michael Sekatchev]]"]
owner: "[[Megan]]"
version: 0.1 (proposal)
tags: [policy]
---

# POL-002 Naming conventions

## One rule
> **Every file starts with the ID of the record that describes it.**

A CSV that turns up on a laptop in five years, named `MEAS-2026-015_CAV-02_beadpull_th112deg_proc.csv`, tells you which record to look up. That record says who took it, when, with which bead, rod angle, CAD revision and VNA settings.

## Record IDs

| Record | ID format | Example |
| --- | --- | --- |
| Measurement | `MEAS-YYYY-NNN` | `MEAS-2026-015` |
| Recovered legacy data | `LEGACY-YYYY-NNN` | `LEGACY-2019-002` |
| Simulation | `SIM-YYYY-NNN` | `SIM-2026-007` |
| Analysis | `ANA-YYYY-NNN` | `ANA-2026-004` |
| CAD part | `CAD-<ASSY>-NNN` | `CAD-CAV02-001` |
| Apparatus | `<TYPE>-NN` | `CAV-02`, `VNA-01`, `BPR-01` |
| Tech memo | `TM-YYYY-NNN` | `TM-2026-003` |
| Meeting | `MTG-YYYY-MM-DD` | `MTG-2026-10-08` |
| Publication | `PUB-YYYY-NNN` | `PUB-2026-001` |
| Public dataset | `DATA-YYYY-NNN` | `DATA-2026-001` |
| Procedure | `PROC-NNN` | `PROC-001` |

Numbers are issued in order. The [[Catalog]] shows the last one used.

## File names

```
<RecordID>_<Apparatus>_<kind>_<conditions>[_<stage>].<ext>
MEAS-2026-015_CAV-02_beadpull_th112deg_proc.csv
MEAS-2026-013_CAV-02_modemap_th000-180deg_peaks.csv
SIM-2026-007_CAV-02_eigenmode_th000-180deg_results.csv
CAD-CAV02-001_barrel_revC.stl
MTG-2026-10-08_viewgraphs_cavity-update_MS.pdf
```

- Letters, digits, `-` and `_` only. No spaces. Lowercase extensions.
- `stage` is one of `raw`, `proc` or `results`, or a short word such as `peaks`.
- **CAD:** released revisions carry `revA`, `revB`, … and are never overwritten. Work in progress between releases is tracked by Git.
- **Photos:** `MEAS-2026-015_CAV-02_photo_bead-line_01.jpg`, attached to the record they document.

## Enforced, not just encouraged
`tools/validate.py` runs on every push. An attachment that doesn't start with its record's ID fails the check, and the change can't be merged until it's fixed.

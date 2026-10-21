---
id: POL-005
title: Where files live
type: policy
access: public
created: 2026-10-21
authors: ["[[Michael Sekatchev]]"]
owner: "[[Megan]]"
version: 0.1 (proposal)
tags: [policy, storage]
---

# POL-005 Where files live

Git is excellent for text and small files, but not for multi-gigabyte data. So the archive is a **catalog that points to bulk storage**, not a dump of everything.

| What | Size | Lives in | Versioned by |
| --- | --- | --- | --- |
| Notes, metadata, memos, procedures | KB | Git repo | Git |
| Processed data (CSV), plots, scripts, STL/STEP exports, drawings (PDF), viewgraphs | KB–MB | Git repo, next to the record | Git |
| Native CAD (`.sldprt`, `.sldasm`), simulation projects (`.cst`, `.mph`, `.aedt`) | 10 MB–GB | Git LFS, or group storage if large | Git LFS / revision letter |
| Raw data (VNA sweeps, DAQ streams, HDF5) | MB–TB | Group storage (department or campus) | SHA-256 checksum in the record |
| Data underlying publications | any | Zenodo / Dryad | DOI with version |

## Rules
- Raw data are **write-once**: never edited, only superseded by a new record.
- The record holds the storage location and a **SHA-256 checksum**. `shasum -a 256 <file>` checks a copy.
- GitHub limits: 100 MB per file, and repositories should stay well under a few GB. `.gitattributes` sends CAD and simulation formats to Git LFS automatically.
- Nothing lives only on a personal laptop or drive. A file is archived when its record has been merged.

## Costs to confirm
- GitHub: free organization plan through GitHub Education, or Team. Git LFS storage beyond the free quota is paid.
- Group storage: department / campus storage or cloud. **To be decided.**
- Zenodo: free (up to 50 GB per record). Dryad: check whether the university's membership covers deposit fees.

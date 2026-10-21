---
id: POL-006
title: How to add a record
type: policy
access: public
created: 2026-10-21
authors: ["[[Michael Sekatchev]]"]
owner: "[[Megan]]"
version: 0.1 (proposal)
tags: [policy, howto]
---

# POL-006 How to add a record

## One-time setup (≈ 10 minutes)
1. Install [Obsidian](https://obsidian.md) (free) and [GitHub Desktop](https://desktop.github.com) or `git`.
2. Clone the archive repo and **open the `vault/` folder as an Obsidian vault**.
3. Enable the bundled **Git** community plugin when Obsidian asks. It pulls on start-up and commits and pushes your changes every 10 minutes.

## Adding a measurement
1. Create a folder: `Measurements/2026/MEAS-2026-0NN <short description>/`.
2. Create a note with the same name, and insert the template **Measurement (bead-pull)** or **Measurement (mode-map)** (Ctrl/Cmd-P → "Insert template").
3. Fill in the Properties. Every blank required field will be flagged.
4. Drop the processed files and plots into the folder, named `MEAS-2026-0NN_…` ([[POL-002 Naming conventions]]).
5. Copy the raw data to group storage. Put its path and `shasum -a 256` checksum into `raw_data`.
6. Link the record from where it belongs, such as the memo, the meeting or the apparatus logbook.
7. Let the Git plugin push (or push yourself). GitHub runs the validator. ✅ means archived. ❌ means read the message and fix it.

## Rescuing old data
Archive old files **as found**. Create a `LEGACY-` record with `method: recovered`, the original path in `provenance`, and `status: incomplete`. Then write down everything you *don't* know. See [[LEGACY-2019-002 PBG-01 mode map (recovered)]].

## Not technical?
Email the files and a few sentences to the archive coordinator ([[Megan]]). The goal is that **nothing is lost**, not that everyone learns Git.

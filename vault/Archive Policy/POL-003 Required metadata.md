---
id: POL-003
title: Required metadata
type: policy
access: public
created: 2026-10-21
authors: ["[[Megan]]", "[[Michael Sekatchev]]"]
owner: "[[Megan]]"
version: 0.1 (proposal)
tags: [policy]
---

# POL-003 Required metadata

The required fields for every record type are defined in one file, `schema/record-types.yaml`, at the root of the repository. The validator enforces it on every push.

## Every record
`id`, `title`, `type`, `access`, `created`, `authors`

## Measurements: the "under what conditions?" fields

| Method | Required beyond the basics |
| --- | --- |
| **bead-pull** | `mode`, `rod_angle_deg`, `frequency_GHz`, `temperature_K`, `atmosphere`, `bead`, `bead_path`, `vna_power_dBm`, `vna_ifbw_Hz`, `procedure`, `cad_revision` |
| **mode-map** | `rod_angle_range_deg`, `rod_angle_step_deg`, `freq_range_GHz`, `temperature_K`, `atmosphere`, `vna_power_dBm`, `vna_ifbw_Hz`, `vna_points`, `procedure`, `cad_revision` |
| **recovered** (legacy) | `provenance`, `recovered_by` |

Every measurement also needs `project`, `apparatus`, `date`, `operator`, `files` and `raw_data`, which records **where the raw data is stored and its SHA-256 checksum**, so we can always verify we have the right file.

## Other record types
- **CAD part:** `assembly`, `revision`, `material`, `cad_tool`, `native_file`, `status`
- **Simulation:** `software` (with version), `solver`, `cad_revision`, `files`
- **Analysis:** `inputs` (links to records), `code`, `status`
- **Publication:** `datasets`, `data_availability` statement
- **Public dataset:** `records`, `license`, `doi`, `repository`, `funding`

## Changing the schema
Changing the schema is a group decision, made by pull request and reviewed by [[Megan]]. Adding a field is cheap. Forgetting one costs us the whole dataset.

---
id: POL-004
title: Data management and sharing
type: policy
access: public
created: 2026-10-21
authors: ["[[Megan]]", "[[Michael Sekatchev]]"]
owner: "[[Karl]]"
version: 0.1 (proposal — to be checked against each award's terms)
tags: [policy, compliance]
---

# POL-004 Data management and sharing

> [!warning] Not legal advice
> A summary to start the discussion. Check the terms of each award and the funder's current public-access policy. The campus research-data-management office can help.

## What the funders expect (in short)
- The 2022 White House OSTP public-access memo directed federal agencies to make **peer-reviewed publications and the scientific data underlying them** publicly available, **without embargo**, under updated agency policies due to take effect by the end of 2025.
- Agency plans (DOE, NSF, …) require a **Data Management and Sharing Plan** in proposals, and expect shared data to have **persistent identifiers (DOIs)** and enough **metadata** to be reusable.
- Papers carry a **data availability statement** pointing to where the data can be found.

## How this archive meets it

| Requirement | Mechanism |
| --- | --- |
| Data are preserved | Records + checksummed raw data on group storage ([[POL-005 Where files live]]) |
| Data are findable and described | Required metadata ([[POL-003 Required metadata]]), [[Catalog]] |
| Data underlying papers are public | A `DATA-` record per paper, deposited to Zenodo/Dryad with a DOI, e.g. [[DATA-2026-001 CAV-02 tuning characterization]] |
| Papers state availability | `data_availability` is required on `PUB-` records |
| Proposals describe access | Reuse the language below |

## Draft language for proposals
> Data generated under this award will be catalogued in the group's version-controlled archive, which records each measurement's conditions, operator, apparatus revision and the checksum of the raw data. Data underlying publications will be deposited in a public repository (Zenodo or Dryad) under a CC-BY-4.0 license with a DOI, no later than the date of publication, and cited in the publication's data availability statement.

## Release workflow
1. Create a `DATA-YYYY-NNN` record that lists the records it contains.
2. Mark those records `access: public` (the validator flags any internal links that will be hidden).
3. [[Karl]] approves.
4. Tag a GitHub release. Zenodo archives it and mints a versioned DOI.
5. Paste the DOI into the `DATA-` and `PUB-` records.

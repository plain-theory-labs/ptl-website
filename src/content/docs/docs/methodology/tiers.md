---
title: Certification Tiers
description: The PTL certification tier system — FRONTIER through PENDING.
---

PTL certification tiers are shorthand for where a composite PTL Score lands. The score is primary. The tier is the communication label.

## Tier table

| Tier | Requirements | Composite |
|---|---|---|
| FRONTIER | All 5 scored engines | ≥ 0.85 |
| OPTIMIZED | 4 or more engines | ≥ 0.70 |
| CAPABLE | 3 or more engines | ≥ 0.60 |
| DEVELOPING | 2 or more engines including ACE | ≥ 0.45 |
| BASELINE | ACE only — first scored assessment | — |
| PENDING | No engines complete | — |

Scored engines are ACE, COOL, FLUX, PACE, and CORE. PROFILE is not scored. GRADE and ATLAS are not scored — they are the certification and recommendation layers.

## Why tiers require multiple engines

A single-engine score does not characterize an organization's infrastructure comprehensively. ACE alone measures GPU utilization. An organization with excellent GPU utilization but a PUE of 1.8 and no carbon accounting is not FRONTIER. The tier system rewards organizations that allow measurement across multiple dimensions.

BASELINE is the exception: it recognizes that the first assessment often begins with `sacct` data alone, before facility data is available. BASELINE is a meaningful starting point, not a penalty.

## Partial certification

Organizations that have not yet provided data for all engines receive certification on the engines they have. A cluster assessed on ACE, PACE, and GRADE with a composite of 0.68 is CAPABLE, not penalized for missing COOL and FLUX. The certification report discloses which engines were included.

This design rewards organizations that start the process rather than waiting until they can provide complete data.

## Tier in certification records

The tier appears in the cert ID: `PTL-YYYYMMDD-ORGSLUG-TIER`. The cert ID is tamper-evident — paired with a SHA256 hash of all certification fields. PTL can verify any cert ID on request.

## The score is the truth

Two FRONTIER organizations — one scoring 0.851, one scoring 0.973 — are both FRONTIER. They are not the same. Buyers, funders, and regulators who want precision should ask for the PTL Score, not the tier. PTL always reports both.

## Longitudinal record

An organization that improves from BASELINE (0.42) to DEVELOPING (0.58) to CAPABLE (0.67) across three annual assessments has a record that tells a story. The tier sequence communicates the direction. The score sequence communicates the magnitude of improvement. Both matter.

---
title: COOL — Cooling Operations Optimization Layer
description: COOL grades cooling system efficiency using PUE relative to benchmark targets.
---

The Cooling Operations Optimization Layer (COOL) measures how efficiently your facility converts incoming power into useful compute — the fraction lost to cooling overhead. COOL uses Power Usage Effectiveness (PUE) as its primary input and scores against continuous linear benchmarks derived from operational data.

## Primary metric

`cool_efficiency_score` — a number from 0.0 to 1.0 derived from your reported or measured PUE.

The scoring is continuous and linear. The benchmark anchor is PUE 1.20 (excellent liquid cooling or free cooling), which scores 1.00. PUE 1.60 scores 0.00. There is no step function — every tenth of a PUE point matters.

| PUE | Score |
|---|---|
| 1.20 | 1.00 |
| 1.25 | 0.84 |
| 1.35 | 0.60 |
| 1.40 | 0.46 |
| 1.50 | 0.23 |
| 1.60 | 0.00 |

## Confidence levels

COOL scores carry confidence labels based on how PUE was measured:

- `high` — annual average from metered utility data
- `medium` — spot measurements or facility-reported estimates
- `low` — single-point measurement or vendor specification

A COOL score of 0.60 with `high` confidence means something different than 0.60 with `low` confidence. Confidence is disclosed in the certification report.

## What COOL does not score

COOL does not assess cooling system type directly — whether you use air, chilled water, direct liquid cooling, or free cooling is not the variable. PUE is. A facility with air cooling operating at PUE 1.28 scores higher than one with liquid cooling operating at PUE 1.45. The measurement, not the technology, determines the score.

## COOL Level 2 (planned)

COOL v0.1.0 operates on single-point or annual-average PUE. A planned Level 2 extension will ingest BMS (Building Management System) timeseries data to produce seasonal efficiency curves and identify operational windows where PUE degrades. This extension is not yet available.

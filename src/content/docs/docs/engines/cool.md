---
title: COOL — Cooling Operations Optimization Layer
description: COOL grades cooling system efficiency using PUE relative to benchmark targets.
---

The Cooling Operations Optimization Layer (COOL) measures how efficiently your facility converts incoming power into useful compute — the fraction lost to cooling overhead. COOL uses Power Usage Effectiveness (PUE) as its primary input and scores against continuous linear benchmarks derived from operational data.

:::note[Version]
COOL v0.1.0 · Released 2026-03-16
:::

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

## Formula

The cool_efficiency_score is a continuous linear function of PUE:

```
cool_efficiency_score = max(0, (PUE_max - PUE) / (PUE_max - PUE_min))

where:
  PUE_max = 1.60  (score = 0.00 at this value)
  PUE_min = 1.20  (score = 1.00 at this value)
  PUE     = your reported or measured PUE
```

This is a strictly linear interpolation. There is no step function — every tenth of a PUE point matters. PUE values below 1.20 score 1.00 (capped). PUE values above 1.60 score 0.00 (floored).

## Worked example

**Input:** Facility reports PUE = 1.35

**Calculation:**

```
cool_efficiency_score = (1.60 - 1.35) / (1.60 - 1.20)
                      = 0.25 / 0.40
                      = 0.625
```

**Result:** COOL score 0.625.

**Comparison to the scoring table:**

| PUE | Formula result | Table value |
|-----|----------------|-------------|
| 1.20 | (1.60-1.20)/(0.40) = 1.000 | 1.00 |
| 1.25 | (1.60-1.25)/(0.40) = 0.875 | 0.84 (rounded) |
| 1.35 | (1.60-1.35)/(0.40) = 0.625 | 0.60 (rounded) |
| 1.40 | (1.60-1.40)/(0.40) = 0.500 | 0.46 (rounded) |
| 1.60 | (1.60-1.60)/(0.40) = 0.000 | 0.00 |

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

## Input schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| pue | float | yes | Power Usage Effectiveness (≥ 1.00) |
| measurement_type | string | yes | annual_average, spot, or vendor_spec |
| cooling_type | string | no | air, chilled_water, dlc, free_cooling, immersion |
| climate_zone | string | no | Used for peer benchmarking in future versions |
| reporting_period | string | no | ISO8601 date range for the PUE measurement |

## CLI usage

```bash
# Score from a single PUE value
cool analyze --pue 1.35 --measurement-type annual_average

# Score with full facility context
cool analyze --pue 1.35 --cooling-type dlc --climate-zone mild

# Output to JSON
cool analyze --pue 1.35 --output cool_result.json
```

## Source

- [View COOL source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/cool)
- [COOL methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/cool_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

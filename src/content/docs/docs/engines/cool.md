---
title: COOL — Cooling Operations Optimization Layer
description: COOL grades facility cooling efficiency by comparing reported PUE against climate-adjusted benchmarks calibrated to cooling technology and facility age. It identifies whether cooling infrastructure is the binding constraint on energy efficiency.
---

The Cooling Operations Optimization Layer (COOL) answers one question: given a facility's cooling technology, age, and climate, how does its Power Usage Effectiveness compare with the documented benchmark? A PUE of 1.45 can be reasonable for an older air-cooled building in a hot climate and weak for a newer liquid-cooled building in a cooler climate. COOL provides that context through a benchmark matrix derived from public survey data, adjusted for ASHRAE climate zone, and produces a letter grade (A-F) plus a continuous efficiency score consumed by GRADE for assessment scoring.

:::note[Version]
<span class="ptl-badge-row"><span class="ptl-badge ptl-badge--version">engine v0.1.0</span><span class="ptl-badge ptl-badge--release">public release 2026-05-11</span><span class="ptl-badge ptl-badge--license">MIT</span><span class="ptl-badge ptl-badge--checks">checks passing</span></span>
:::

## Primary metric

`cool_efficiency_score` — a continuous 0.0–1.0 score derived from the gap between your reported PUE and the climate-adjusted efficient benchmark for your facility type.

```
delta = annual_pue - climate_adjusted_benchmark_pue

cool_efficiency_score:
  delta ≤ -0.05  → 1.0   (outperforming benchmark by 5%+)
  delta =  0.00  → 0.857 (exactly at benchmark)
  delta ≥  0.30  → 0.0   (failing threshold)
```

The score is a linear interpolation of delta across the interval [-0.05, +0.30]. Values outside that interval are clamped. Every hundredth of a PUE point matters.

## Letter grade

COOL assigns a letter grade based on the same delta:

| Grade | Condition | Label |
|---|---|---|
| A | delta ≤ -0.05 | Excellent |
| B | -0.05 < delta ≤ 0.05 | Good |
| C | 0.05 < delta ≤ 0.15 | Adequate |
| D | 0.15 < delta ≤ 0.30 | Poor |
| F | delta > 0.30 | Failing |

## Benchmark methodology

The benchmark varies by three dimensions: cooling type, facility age band, and ASHRAE climate zone.

**Cooling types:** `air`, `water`, `liquid_to_chip`, `hybrid`

**Age bands:**

| Band | Years |
|---|---|
| `pre_2010` | Built or last substantially renovated before 2010 |
| `2010_2018` | 2010–2018 |
| `post_2018` | After 2018 |

Each combination has a `typical` benchmark (published survey median) and an `efficient` benchmark (top quartile). COOL grades against the `efficient` benchmark — the bar is set by what the best-performing facilities of the same type report, not the average.

**Example benchmarks (efficient, pre-climate-adjustment):**

| Cooling type | pre_2010 | 2010_2018 | post_2018 |
|---|---|---|---|
| air | 1.55 | 1.40 | 1.30 |
| water | 1.45 | 1.30 | 1.20 |
| liquid_to_chip | 1.35 | 1.20 | 1.10 |
| hybrid | 1.45 | 1.28 | 1.15 |

Sources: Uptime Institute Global Data Center Survey 2023, Green Grid Data Center Efficiency Metrics 2022, DOE Data Center Optimization Initiative 2022.

## Climate adjustment

Facilities in hotter climates face a larger cooling burden. COOL adjusts the efficient benchmark by an additive offset derived from the facility's ASHRAE climate zone before comparing against reported PUE.

```
climate_adjusted_benchmark = efficient_benchmark + climate_adjustment
```

Positive adjustment = benchmark relaxed (hotter climate, more cooling load).
Negative adjustment = benchmark tightened (colder climate, free cooling available).

| ASHRAE Zone | Name | Adjustment | Examples |
|---|---|---|---|
| 1A | Very Hot Humid | +0.10 | Miami FL, Houston TX |
| 2A | Hot Humid | +0.07 | Atlanta GA, Dallas TX |
| 2B | Hot Dry | +0.05 | Phoenix AZ |
| 3A | Warm Humid | +0.04 | Charlotte NC |
| 3B | Warm Dry | +0.02 | Los Angeles CA |
| 3C/4A | Warm Marine / Mixed Humid | 0.00 | San Francisco CA, Baltimore MD |
| 4C | Mixed Marine | -0.03 | Seattle WA, Portland OR |
| 5A | Cool Humid | -0.04 | Chicago IL, Detroit MI |
| 5B | Cool Dry | -0.05 | Denver CO, Salt Lake City UT |
| 6A | Cold Humid | -0.07 | Burlington VT, Duluth MN |
| 6B | Cold Dry | -0.08 | Helena MT |
| 7 | Very Cold | -0.10 | International Falls MN |
| 8 | Subarctic/Arctic | -0.12 | Anchorage AK |

Source: ASHRAE Thermal Guidelines for Data Processing Environments, 5th Edition.

For US facilities, COOL maps the state abbreviation to the predominant ASHRAE zone for that state. For international facilities, supply the ASHRAE zone code directly — ASHRAE zones are globally defined.

## Worked example

**Facility:** Air-cooled, built 2008, Minneapolis MN, annual PUE 1.72

```
cooling_type: air
age_band:     pre_2010  (built 2008)
location:     MN → ASHRAE zone 6A (Cold Humid) → adjustment -0.07

efficient_benchmark:          1.55  (air, pre_2010)
climate_adjusted_benchmark:   1.55 + (-0.07) = 1.48

delta = 1.72 - 1.48 = +0.24

Grade: D (Poor)  — 0.15 < delta ≤ 0.30
cool_efficiency_score: (0.30 - 0.24) / 0.35 = 0.171
```

Despite operating in a cold climate (which tightens the benchmark), the facility's old air cooling is pulling it down to D.

**Contrast — Liquid-cooled, built 2021, Houston TX, annual PUE 1.08**

```
cooling_type: liquid_to_chip
age_band:     post_2018  (built 2021)
location:     TX → zone 2A (Hot Humid) → adjustment +0.07

efficient_benchmark:          1.10  (liquid_to_chip, post_2018)
climate_adjusted_benchmark:   1.10 + 0.07 = 1.17

delta = 1.08 - 1.17 = -0.09

Grade: A (Excellent)  — delta ≤ -0.05
cool_efficiency_score: 1.0  (clamped)
```

Modern liquid cooling in a hot climate, outperforming an already-relaxed benchmark.

## International support

For facilities outside the US, provide the ASHRAE zone code directly in the input. ASHRAE climate zones are globally defined:

| Location | ASHRAE Zone |
|---|---|
| Netherlands | 5A |
| Singapore | 1A |
| Norway | 7 |
| China (Beijing) | 5A |
| China (Shenzhen) | 2A |

## Findings exported to GRADE

| Metric | Description |
|---|---|
| `cool_efficiency_score` | Continuous 0.0–1.0 score — GRADE input |
| `pue_reported` | Organization self-reported annual average PUE |
| `pue_benchmark` | Climate-adjusted efficient benchmark |
| `pue_gap` | `pue_reported` minus `pue_benchmark` (the delta) |
| `cooling_grade` | Letter grade as 0–4 integer (A=4, B=3, C=2, D=1, F=0) |
| `climate_adjustment_applied` | Additive ASHRAE zone offset applied to benchmark |

All findings carry `confidence: medium` for self-reported Level 1 input. Computed values (benchmark, climate adjustment) carry `confidence: high`.

## Confidence and self-reporting

PUE at Level 1 is self-reported. PTL does not independently verify the value. The grade reflects what the organization reports, so the assessment is only as reliable as the input.

Level 2 (BMS timeseries from a Building Management System) is specified but not yet implemented. When available, it will enable seasonal variance analysis and higher-confidence findings.

## Known limits

- Climate zone lookup is state-level for US facilities. Organizations in large, climatically varied states (California, Texas) may be assigned a zone that does not reflect their specific location. International facilities should supply the zone code directly.
- Benchmarks reflect public survey data through 2023 and will be reviewed annually.
- COOL v0.1.0 does not adjust for compute density. A high-density GPU cluster has higher heat rejection requirements than a traditional HPC cluster at the same PUE — this is not yet captured.

## Input schema

| Field | Type | Required | Description |
|---|---|---|---|
| `organization` | string | yes | Organization name |
| `period` | string | yes | Reporting year (YYYY) |
| `cooling_type` | string | yes | `air`, `water`, `liquid_to_chip`, or `hybrid` |
| `facility_age` | int | yes | Year built or last substantially renovated |
| `location_city` | string | yes | City name (for display) |
| `location_state` | string | yes | 2-letter US state abbreviation, or `""` for international |
| `annual_pue` | float | yes | Annual average Power Usage Effectiveness |
| `ashrae_zone` | string | no | Direct ASHRAE zone override — required for international facilities |

## CLI usage

```bash
# Score a single facility from a cool_input_v1.json file
cool analyze \
  --input cool_input.json \
  --output cool_output.json

# Run all five synthetic organizations and print summary table
cool demo

# Validate a ptl_output_v1.json file against the PTL schema
cool validate --input cool_output.json
```

**Example `cool_input.json`:**

```json
{
  "organization": "Midwest University HPC Center",
  "period": "2026",
  "cooling_type": "air",
  "facility_age": 2008,
  "location_city": "Minneapolis",
  "location_state": "MN",
  "annual_pue": 1.72
}
```

**International facility:**

```json
{
  "organization": "Netherlands AI Institute",
  "period": "2026",
  "cooling_type": "water",
  "facility_age": 2019,
  "location_city": "Amsterdam",
  "location_state": "",
  "annual_pue": 1.25,
  "ashrae_zone": "5A"
}
```

## Source

- [View COOL source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/cool)
- [COOL methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/cool_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

---
title: CORE — Capital and Operations Resource Evaluator
description: CORE grades hardware-workload fit, fleet age, and embodied carbon efficiency across your GPU fleet. It identifies whether hardware capital decisions are the binding constraint on infrastructure efficiency.
---

The Capital and Operations Resource Evaluator (CORE) grades the hardware layer of your AI infrastructure — whether the GPUs you operate are the right hardware for the workloads you run, how old the fleet is relative to the GPU refresh cycle, and how efficiently embodied carbon is amortized across the compute capacity those GPUs deliver. CORE identifies whether hardware decisions are creating a structural ceiling on what ACE and PACE can achieve.

:::note[Version]
<span class="ptl-badge-row"><span class="ptl-badge ptl-badge--version">engine v0.1.0</span><span class="ptl-badge ptl-badge--method">fit matrix update 2026-05-09</span><span class="ptl-badge ptl-badge--license">MIT</span><span class="ptl-badge ptl-badge--checks">checks passing</span></span>
:::

## Primary metric

`core_efficiency_score` — a number from 0.0 to 1.0 composed of three fleet-weighted components:

- **Hardware fit** (40%) — how well each GPU model matches the declared primary workload type
- **Fleet age** (35%) — GPU age in years, anchored to published refresh-cycle references
- **Embodied carbon** (25%) — carbon efficiency normalized by compute capacity delivered (kg CO₂e per TFLOP/s)

## Formula

```
core_efficiency_score =
  hardware_fit_score    × 0.40 +
  fleet_age_score       × 0.35 +
  embodied_carbon_score × 0.25
```

All three component scores are GPU-count-weighted fleet averages. A fleet with 800 H100s and 200 A100s weights H100 at 80% and A100 at 20%.

## Hardware-workload fit

Scores how well each GPU model suits the declared primary workload. Derived from MLPerf Training v3.1 and MLPerf Inference v4.0 benchmark results (mlcommons.org/results), normalized so the best available result per workload = 1.00. AMD and Intel scores from their respective MLPerf submissions.

**Selected fit scores:**

| GPU | training_large | training_small | inference | mixed |
|---|---|---|---|---|
| B200 | 1.00 | 0.92 | 0.95 | 0.97 |
| GB200 | 1.00 | 0.90 | 0.95 | 0.97 |
| B100 | 0.95 | 0.90 | 0.92 | 0.93 |
| H200 | 0.90 | 0.89 | 0.93 | 0.91 |
| H100 | 0.88 | 0.88 | 0.90 | 0.89 |
| MI300X | 0.85 | 0.88 | 0.90 | 0.87 |
| Gaudi3 | 0.72 | 0.75 | 0.78 | 0.75 |
| A100 | 0.52 | 0.72 | 0.60 | 0.62 |
| L40S | 0.42 | 0.72 | 0.83 | 0.68 |
| Gaudi2 | 0.55 | 0.62 | 0.60 | 0.58 |
| A40 | 0.38 | 0.70 | 0.75 | 0.60 |
| RTX Pro 6000 | 0.40 | 0.72 | 0.88 | 0.65 |
| RTX 4090 | 0.28 | 0.58 | 0.72 | 0.50 |
| V100 | 0.22 | 0.42 | 0.38 | 0.32 |
| unknown | 0.40 | 0.40 | 0.40 | 0.40 |

Consumer GPUs (RTX 4090, RTX 3090) have no MLPerf Datacenter submission — their scores are extrapolated from published FLOP/s ratios and carry higher uncertainty.

### MIG utilization multiplier

When MIG partitioning is enabled on a GPU record, the fit score is multiplied by `active_instances / total_instances`. Idle MIG partitions represent configured but unused compute capacity.

```
mig_multiplier = mig_instances_active / mig_instance_count
fit_score_effective = fit_score × mig_multiplier
```

## Fleet age scoring

Age is computed from `assessment_year − purchase_year` per GPU record, then weighted by GPU count across the fleet. Scoring is anchored to published GPU hardware refresh-cycle references.

| Age (years) | Score | Rationale |
|---|---|---|
| ≤ 2 | 1.00 | Current generation, full performance, full software support |
| ≤ 4 | 0.80 | One generation behind, still widely supported |
| ≤ 6 | 0.60 | Two generations behind, approaching EOL driver support |
| ≤ 8 | 0.35 | EOL or near-EOL, limited workload support |
| > 8 | 0.15 | Legacy, significant efficiency penalty |

Sources: public hyperscaler sustainability reports; GPU generation cadence references; DOE ESIF hardware lifecycle documentation.

## Embodied carbon scoring

Embodied carbon is normalized by compute capacity delivered — kg CO₂e per TFLOP/s — rather than absolute carbon per GPU. This correctly reflects that a high-performance GPU with higher embodied carbon may be more carbon-efficient per unit of useful compute than a legacy GPU with lower absolute carbon.

```
kg_per_tflops = embodied_carbon_kg / tflops_per_gpu
score = 1 − (kg_per_tflops / 2.24)   [clamped 0.0 – 1.0]
```

Reference baseline: A100 at 700 kg CO₂e / 312 TFLOP/s = 2.24 kg/TFLOP/s → score 0.0.
GPUs with better compute-per-carbon score above 0.0. GPUs below A100 density also score 0.0 (clamped).

**Selected embodied carbon values and scores:**

| GPU | TFLOP/s (FP16) | CO₂e (kg) | kg/TFLOP/s | Score |
|---|---|---|---|---|
| B200 | 4,500 | 1,200 | 0.267 | 0.881 |
| H100 | 1,979 | 700 | 0.354 | 0.842 |
| MI300X | 2,614 | 950 | 0.364 | 0.838 |
| H200 | 1,979 | 950 | 0.480 | 0.786 |
| Gaudi3 | 1,835 | 900 | 0.490 | 0.781 |
| L40S | 733 | 420 | 0.573 | 0.744 |
| A100 | 312 | 700 | 2.244 | 0.0 (reference) |
| V100 | 125 | 500 | 4.000 | 0.0 (clamped) |

Sources: NVIDIA Product Carbon Footprint reports; Dell/HPE lifecycle data; Gupta et al. 2021; Patterson et al. 2022. Blackwell values extrapolated from die-size scaling.

## Worked example

**Fleet:** 512 H100s purchased 2023, 256 A100s purchased 2021. Primary use: `training_large`. Assessment year: 2026.

```
H100 record (512 GPUs, age = 3 years):
  fit_score       = 0.88  (H100 × training_large)
  age_score       = 0.80  (age 3 ≤ 4)
  embodied_score  = 0.842 (700 kg / 1979 TFLOP/s = 0.354 kg/TFLOP/s)

A100 record (256 GPUs, age = 5 years):
  fit_score       = 0.52  (A100 × training_large)
  age_score       = 0.60  (age 5 ≤ 6)
  embodied_score  = 0.00  (reference baseline — clamped)

Fleet-weighted averages (512 H100 + 256 A100 = 768 total):
  hardware_fit_score    = (512×0.88 + 256×0.52) / 768 = (450.6 + 133.1) / 768 = 0.760
  fleet_age_score       = (512×0.80 + 256×0.60) / 768 = (409.6 + 153.6) / 768 = 0.733
  embodied_carbon_score = (512×0.842 + 256×0.00) / 768 = 431.1 / 768 = 0.562

core_efficiency_score =
  0.760 × 0.40 +
  0.733 × 0.35 +
  0.562 × 0.25
= 0.304 + 0.257 + 0.141
= 0.702  → Grade B (Good)
```

The A100s drag down all three components. Refreshing the 256 A100s to H100s would push composite to ~0.85 (Grade A).

## Letter grade

| Grade | Condition | Label |
|---|---|---|
| A | score ≥ 0.80 | Excellent |
| B | score ≥ 0.65 | Good |
| C | score ≥ 0.50 | Adequate |
| D | score ≥ 0.35 | Poor |
| F | score < 0.35 | Failing |

## Findings exported to GRADE

| Metric | Unit | Description |
|---|---|---|
| `core_efficiency_score` | score_0_to_1 | Weighted composite — GRADE input |
| `hardware_fit_score` | score_0_to_1 | Fleet-weighted fit for declared primary workload |
| `fleet_age_score` | score_0_to_1 | Fleet-weighted age band score |
| `embodied_carbon_score` | score_0_to_1 | Fleet-weighted kg CO₂e per TFLOP/s score |
| `fleet_age_years_weighted` | years | GPU-count-weighted mean fleet age |
| `hardware_efficiency_grade` | grade_points_0_to_4 | A=4, B=3, C=2, D=1, F=0 |

## ACE cross-reference

CORE reads `gpu_efficiency_score` from an ACE output when `ace_report_path` is provided. This is informational — it does not affect the CORE composite formula in v0.1, but it appears in the GRADE report alongside CORE findings to give context on whether a hardware fit gap is being exposed by actual workloads.

## Input schema

CORE takes a JSON file with a hardware fleet list and a workload profile. The fleet is a list of `HardwareRecord` objects — one per distinct GPU model and purchase cohort.

| Field | Type | Required | Description |
|---|---|---|---|
| `organization` | string | yes | Organization name |
| `period` | string | yes | Assessment year (YYYY) |
| `scheduler` | string | yes | `slurm`, `kubernetes`, or `unknown` |
| `hardware_fleet` | list | yes | List of hardware records (see below) |
| `workload_profile` | object | yes | Workload characteristics |
| `ace_report_path` | string | no | Path to ACE ptl_output for cross-reference |

**Hardware record fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `gpu_model` | string | yes | `h100`, `a100`, `b200`, `mi300x`, `v100`, etc. |
| `gpu_count` | int | yes | Number of GPUs in this record |
| `purchase_year` | int | yes | Year purchased or last substantially upgraded |
| `tdp_watts` | int | yes | GPU TDP in watts |
| `embodied_carbon_kg` | float | no | Total embodied CO₂e for record; uses default if absent |
| `mig_enabled` | bool | no | Whether MIG partitioning is active |
| `mig_instance_count` | int | no | Total MIG instances configured |
| `mig_instances_active` | int | no | MIG instances currently in use |

**Workload profile fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `primary_use` | string | yes | `training_large`, `training_small`, `inference`, `mixed`, or `unknown` |
| `avg_gpu_utilization` | float | yes | Average GPU utilization (0.0–1.0) |
| `avg_job_duration_minutes` | float | yes | Average job duration in minutes |

## CLI usage

```bash
# Score a single organization from a core_input JSON file
core analyze \
  --input core_input.json \
  --output core_output.json

# Run all synthetic hardware fleets and print grades
core demo

# Validate a ptl_output_v1.json export against the PTL schema
core validate --input core_output.json
```

**Example `core_input.json`:**

```json
{
  "organization": "National AI Research Center",
  "period": "2026",
  "scheduler": "slurm",
  "hardware_fleet": [
    {
      "gpu_model": "h100",
      "gpu_count": 512,
      "purchase_year": 2023,
      "tdp_watts": 700
    },
    {
      "gpu_model": "a100",
      "gpu_count": 256,
      "purchase_year": 2021,
      "tdp_watts": 400
    }
  ],
  "workload_profile": {
    "primary_use": "training_large",
    "avg_gpu_utilization": 0.72,
    "avg_job_duration_minutes": 240
  }
}
```

## Source

- [View CORE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/core)
- [CORE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/core_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

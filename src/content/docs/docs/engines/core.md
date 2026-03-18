---
title: CORE — Capital and Operations Resource Evaluator
description: CORE evaluates hardware-workload fit, fleet age, and embodied carbon.
---

The Capital and Operations Resource Evaluator (CORE) grades your hardware against your workloads — whether the GPUs you are operating are the right hardware for the jobs you are running, how old the fleet is, and what the embodied carbon cost of that hardware represents.

:::note[Version]
CORE v2.0.0 · Released 2026-03-11
:::

## Primary metric

`core_efficiency_score` — a number from 0.0 to 1.0 composed of three components:

- **Hardware fit** (40%) — how well your GPU fleet matches your primary workload category
- **Fleet age** (35%) — weighted average age of your GPU fleet
- **Embodied carbon** (25%) — carbon cost of manufacturing your hardware relative to expected useful life

## Formula

```
core_efficiency_score =
  hardware_fit_score × 0.40 +
  fleet_age_score    × 0.35 +
  embodied_score     × 0.25

where:
  hardware_fit_score = f(gpu_model, primary_workload)
    See hardware-workload fit matrix below.

  fleet_age_score = f(gpu_generation, deployment_year)
    Current gen (Blackwell) → 1.00
    Previous gen (Hopper)   → 0.90
    Two gens back (Ampere)  → 0.70
    Three+ gens back        → 0.40

  embodied_score = f(embodied_co2_kg, utilization)
    Higher utilization amortizes embodied carbon.
    Score = min(1.0, utilization_rate / 0.80) × generation_factor
```

### Hardware-workload fit matrix

| GPU | Training (large) | Inference | Mixed | Embodied CO2 |
|-----|-----------------|-----------|-------|--------------|
| B200 | 1.00 | 0.90 | 0.95 | 1,200 kg |
| H200 | 0.90 | 0.85 | 0.88 | 950 kg |
| H100 | 0.82 | 0.75 | 0.80 | 700 kg |
| RTX Pro 6000 | 0.45 | 1.00 | 0.70 | 400 kg |
| A100 | 0.70 | 0.65 | 0.68 | 700 kg |
| V100 | 0.40 | 0.45 | 0.42 | 500 kg |

RTX Pro 6000 scores 1.00 for inference workloads — it is the right tool for single-GPU inference at 3x lower cost than H100.

## Worked example

**Input:**

```
gpu_model        = H100 SXM5
primary_workload = inference
deployment_year  = 2024
gpu_utilization  = 0.86
```

**Calculation:**

```
hardware_fit_score = 0.75  (H100 x inference from matrix)

fleet_age_score = 0.90  (Hopper generation, 2024 deployment)

embodied_score = min(1.0, 0.86 / 0.80) × 0.90
              = min(1.0, 1.075) × 0.90
              = 1.00 × 0.90
              = 0.90

core_efficiency_score =
  (0.75 × 0.40) + (0.90 × 0.35) + (0.90 × 0.25)
= 0.300 + 0.315 + 0.225
= 0.840
```

**Result:** CORE score 0.840. The hardware-workload fit gap (H100 scores 0.75 for inference vs 1.00 for RTX Pro 6000) is the primary finding. For a pure inference cluster, RTX Pro 6000 would score higher and cost significantly less per GPU.

## Hardware fit scoring

CORE uses a hardware fit matrix that maps GPU model to workload category. The matrix reflects the architectural strengths of each GPU generation for specific workload types — large-scale training, inference, and scientific simulation.

Selected fit scores:

| GPU | Workload | Score |
|---|---|---|
| B200 | Training (large) | 1.00 |
| H100 | Training (large) | 0.82 |
| A100 | Training (large) | 0.70 |
| RTX Pro 6000 | Inference | 1.00 |
| H100 | Inference | 0.75 |
| A100 | Inference | 0.65 |

Running A100s on large-model training where H100s or B200s would be architecturally superior reduces your CORE score. Running V100s on inference workloads that would benefit from dedicated inference hardware reduces it further.

## MIG scoring

When PROFILE detects MIG (Multi-Instance GPU) configuration, CORE applies a MIG utilization multiplier. MIG allows a single GPU to serve multiple smaller workloads efficiently. If MIG instances are underutilized relative to the number configured, the fit score is adjusted downward.

## Fleet age

Older hardware scores lower on fleet age not as a depreciation metric but as an efficiency signal. Modern GPU generations deliver substantially more compute per watt than older ones. An A100 delivers roughly 3x the energy efficiency of a V100 on the same workload type. Fleet age scoring rewards organizations that have maintained infrastructure investment.

## Embodied carbon

Manufacturing large GPU systems produces substantial carbon. CORE tracks estimated embodied carbon in kg CO2e per GPU and weights it against expected useful life. A B200 (approximately 1,200 kg CO2e) operated for 5+ years at high utilization has a very different lifecycle profile than the same GPU retired after two years at 25% utilization.

Embodied carbon is disclosed as a finding, not a penalty. It appears in the GRADE report alongside utilization data so procurement decisions can be made with the full picture.

## Input schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| gpu_model | string | yes | GPU model identifier (h100, a100, v100, b200, rtx_pro_6000, etc.) |
| primary_workload | string | yes | training_large, training_small, inference, or mixed |
| deployment_year | int | yes | Year the GPU fleet was deployed |
| gpu_utilization | float | yes | Average GPU utilization rate (0.0–1.0) from ACE |
| gpu_count | int | no | Total number of GPUs in fleet |
| mig_enabled | boolean | no | Whether MIG partitioning is active |
| mig_instances_active | int | no | Active MIG instances (if mig_enabled) |

## CLI usage

```bash
# Score a specific hardware configuration
core analyze \
  --gpu-model h100 \
  --workload inference \
  --deployment-year 2024 \
  --utilization 0.86

# Score with MIG configuration
core analyze \
  --gpu-model h100 \
  --workload inference \
  --deployment-year 2024 \
  --utilization 0.86 \
  --mig-enabled true \
  --mig-instances-active 4

# Output to JSON
core analyze --input core_config.json --output core_result.json
```

## Source

- [View CORE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/core)
- [CORE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/core_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

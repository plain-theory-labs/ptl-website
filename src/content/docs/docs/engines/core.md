---
title: CORE — Capital and Operations Resource Evaluator
description: CORE evaluates hardware-workload fit, fleet age, and embodied carbon.
---

The Capital and Operations Resource Evaluator (CORE) grades your hardware against your workloads — whether the GPUs you are operating are the right hardware for the jobs you are running, how old the fleet is, and what the embodied carbon cost of that hardware represents.

## Primary metric

`core_efficiency_score` — a number from 0.0 to 1.0 composed of three components:

- **Hardware fit** (40%) — how well your GPU fleet matches your primary workload category
- **Fleet age** (35%) — weighted average age of your GPU fleet
- **Embodied carbon** (25%) — carbon cost of manufacturing your hardware relative to expected useful life

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

Manufacturing large GPU systems produces substantial carbon. CORE tracks estimated embodied carbon in kg CO₂e per GPU and weights it against expected useful life. A B200 (approximately 1,200 kg CO₂e) operated for 5+ years at high utilization has a very different lifecycle profile than the same GPU retired after two years at 25% utilization.

Embodied carbon is disclosed as a finding, not a penalty. It appears in the GRADE report alongside utilization data so procurement decisions can be made with the full picture.

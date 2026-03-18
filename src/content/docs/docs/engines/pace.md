---
title: PACE — Predictive Allocation and Cluster Efficiency
description: PACE measures scheduler efficiency — how well your cluster allocates resources across competing workloads.
---

Predictive Allocation and Cluster Efficiency (PACE) measures how well your cluster scheduler allocates resources across competing workloads. GPU efficiency (ACE) tells you whether jobs use what they request. PACE tells you whether the scheduler is giving resources to the right jobs at the right time.

:::note[Version]
PACE v2.0.0 · Released 2026-03-11
:::

## Primary metric

`pace_composite_score` — a number from 0.0 to 1.0 composed of three components:

- **Request accuracy** (50%) — how well job resource requests match actual usage
- **Queue incentive** (30%) — whether the scheduler configuration rewards efficient behavior
- **Fragmentation** (20%) — GPU node fragmentation from poorly-matched job sizes

## Formula

### Slurm path

```
pace_composite_score =
  request_accuracy   × 0.50 +
  queue_incentive    × 0.30 +
  fragmentation      × 0.20

where:
  request_accuracy = gpu_hours_used / gpu_hours_requested

  queue_incentive  = base_queue_score × short_job_multiplier
    base_queue_score = f(preemption, QOS policies, fairshare config)
    short_job_multiplier = 1.0 - max(0, (short_job_pct - 0.25) × 2.0)
    (penalty activates when >25% of jobs run under 5 minutes)

  fragmentation    = 1.0 - (fragmented_node_pct)
    fragmented_node_pct = nodes with mixed job sizes / total nodes
```

### Kubernetes path

```
pace_composite_score =
  resource_accuracy    × 0.50 +
  scheduling_quality   × 0.30 +
  coverage             × 0.20

where:
  resource_accuracy  = actual_gpu / requested_gpu (across pods)

  scheduling_quality = f(avg_pod_pending_minutes):
    < 5 min   → 1.00
    < 15 min  → 0.80
    < 30 min  → 0.60
    < 60 min  → 0.40
    ≥ 60 min  → 0.20

  coverage           = quota_utilized / quota_granted
```

## Worked example

**Input** (Slurm cluster):

```
gpu_hours_requested = 1,200,000
gpu_hours_used      = 864,000
short_job_pct       = 0.411   (41.1% of jobs < 5 min)
preemption_enabled  = false
qos_policies        = none
fragmented_node_pct = 0.12
```

**Calculation:**

```
request_accuracy = 864,000 / 1,200,000 = 0.720

base_queue_score = 0.50  (no preemption, no QOS)
short_job_multiplier = 1.0 - max(0, (0.411 - 0.25) × 2.0)
                     = 1.0 - (0.161 × 2.0)
                     = 1.0 - 0.322
                     = 0.678
queue_incentive = 0.50 × 0.678 = 0.339

fragmentation = 1.0 - 0.12 = 0.880

pace_composite_score =
  (0.720 × 0.50) + (0.339 × 0.30) + (0.880 × 0.20)
= 0.360 + 0.102 + 0.176
= 0.638
```

**Result:** PACE score 0.638. The short-job penalty reduced queue incentive from 0.50 to 0.339. This matches the MIT Supercloud PACE score of 0.475 (which had additional queue configuration gaps).

## Slurm scoring

In Slurm mode, PACE analyzes `sacct` exports. Request accuracy is the ratio of used GPU-hours to requested GPU-hours. Queue incentive is scored from Slurm configuration — whether preemption is enabled, whether QOS policies exist, whether short-job penalties are in place.

The queue incentive component includes a short-job penalty: if more than 25% of jobs run for under 5 minutes, the queue incentive score is reduced proportionally. Short jobs indicate scheduling overhead problems, and schedulers that tolerate high short-job fractions are not directing compute efficiently.

For MIT Supercloud (41.1% short jobs), the short-job penalty reduced queue incentive by 8.2 percentage points, contributing to a PACE score of 0.475.

## Kubernetes scoring

In Kubernetes mode, PACE uses a different formula with different components:

- **Resource accuracy** (50%) — ratio of actual to requested GPU resources across pods
- **Scheduling quality** (30%) — average pod pending time in bands (0–5 min → 1.0, >60 min → 0.0)
- **Coverage** (20%) — GPU quota utilization across namespaces

PROFILE sets the input path. If your cluster runs Kubernetes, PACE runs the Kubernetes scoring path automatically.

## Input schema

### Slurm path

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| gpu_hours_requested | float | yes | Total GPU-hours requested across all jobs |
| gpu_hours_used | float | yes | Total GPU-hours actually consumed |
| short_job_pct | float | yes | Fraction of jobs running under 5 minutes (0.0–1.0) |
| preemption_enabled | boolean | yes | Whether Slurm preemption is configured |
| qos_policies_count | int | no | Number of active QOS policies |
| fairshare_enabled | boolean | no | Whether fairshare scheduling is active |
| fragmented_node_pct | float | no | Fraction of nodes with fragmented GPU allocation |

### Kubernetes path

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource_request_ratio | float | yes | Mean(actual_gpu / requested_gpu) across pods |
| avg_pod_pending_minutes | float | yes | Average time pods wait before scheduling |
| quota_utilization | float | yes | GPU quota used / GPU quota granted (0.0–1.0) |

## What low PACE scores mean

Low request accuracy indicates jobs are requesting resources they do not use — a different measurement than ACE's utilization score. Low queue incentive often indicates a scheduler with no preemption configured and no policies to reward GPU-efficient behavior. ATLAS receives the PACE findings and generates specific Slurm configuration recommendations: the exact `slurm.conf` parameters to add, with expected impact ranges.

## CLI usage

```bash
# Analyze a Slurm cluster
pace analyze \
  --gpu-hours-requested 1200000 \
  --gpu-hours-used 864000 \
  --short-job-pct 0.41 \
  --preemption-enabled false

# Analyze a Kubernetes cluster
pace analyze \
  --input-path kubernetes \
  --resource-request-ratio 0.91 \
  --avg-pod-pending-minutes 3.2 \
  --quota-utilization 0.87

# Output to JSON
pace analyze --input slurm_data.json --output pace_result.json
```

## Source

- [View PACE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/pace)
- [PACE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/pace_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

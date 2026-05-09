---
title: PACE — Predictive Allocation and Cluster Efficiency
description: PACE measures scheduler efficiency — how well your cluster allocates resources and schedules jobs.
---

Predictive Allocation and Cluster Efficiency (PACE) measures how well your cluster scheduler allocates resources across competing workloads. GPU efficiency (ACE) tells you whether jobs use what they request. PACE tells you whether the scheduler is giving resources to the right jobs at the right time — and whether users have any incentive to ask for only what they need.

:::note[Version]
PACE v2.0.0 · Released 2026-03-16 · Queue incentive redesigned v0.2 2026-05-09
:::

## Primary metric

`pace_composite_score` — a number from 0.0 to 1.0 composed of three components:

- **Request accuracy** (50%) — how well job resource requests match actual usage
- **Queue incentive** (30%) — whether the scheduler produces efficient scheduling outcomes, measured from job traces
- **Fragmentation** (20%) — GPU allocation waste from poorly-matched job sizes

## Formula

### Slurm path — when ACE output is present

Fragmentation weight is dropped and given to queue incentive. Fragmentation
uses the same aggregate GPU ratio as ACE — carrying it would count GPU
utilization a third time in GRADE. Queue incentive captures the scheduling
dynamics that ACE cannot see.

```
pace_composite_score =
  request_accuracy   × 0.40 +   ← job calibration rate (different from ACE)
  queue_incentive    × 0.60     ← wait-time scheduling signals (independent)
```

### Slurm path — when ACE output is absent

Standard three-way split. Overlap with ACE is absent since ACE is not
running, and the data quality output labels this clearly.

```
pace_composite_score =
  request_accuracy   × 0.50 +
  queue_incentive    × 0.30 +
  fragmentation      × 0.20

where:
  request_accuracy = (gpu_accuracy_score + cpu_accuracy_score) / 2
    gpu_accuracy_score = f(total_gpu_used / total_gpu_requested)
    cpu_accuracy_score = f(total_cpu_used / total_cpu_requested)

  queue_incentive = data-driven composite from job traces:
    scheduling_pressure_score × 0.40
    + small_job_advantage_score × 0.35
    + wait_spread_score × 0.25

  fragmentation = 1.0 - fragmentation_penalty
    fragmentation_penalty = f(gpu_waste_pct)
```

### Queue incentive signals (computed from job traces)

Queue incentive measures scheduling outcomes, not feature flags. All three signals
are computed from job submit_time, start_time, end_time, and GPU count — the same
fields present in sacct exports, Alibaba Helios traces, and Microsoft Philly logs.

### Request accuracy — job calibration rate (from ACE output)

When ACE has been run, PACE request accuracy uses **job calibration rate**
rather than the aggregate GPU ratio — avoiding double-counting with ACE
in the GRADE composite.

```
job_calibration_rate = 1.0 - flagged_jobs_pct   (from ACE output)
```

ACE answers: how hard did GPUs work on average?
PACE calibration answers: what fraction of jobs were appropriately sized?

These diverge meaningfully. A cluster where all jobs use exactly 55% of GPUs
has ACE = 0.55 but calibration rate = 1.00 (none flagged). A cluster where
half the jobs use 0% and half use 100% has ACE = 0.50 but calibration rate = 0.50.

| Calibration rate | Score |
|------------------|-------|
| ≥ 0.80 | 1.00 |
| ≥ 0.60 | 0.75 |
| ≥ 0.40 | 0.50 |
| ≥ 0.20 | 0.25 |
| < 0.20 | 0.00 |

When ACE output is not available, PACE falls back to the aggregate GPU ratio
(`total_gpu_used / total_gpu_requested`). This fallback measures the same
signal as ACE and the overlap is documented in the GRADE data quality output.

**Signal 1 — Scheduling pressure ratio (40% of queue incentive)**

```
scheduling_pressure_ratio = median(queue_wait_hours) / median(job_duration_hours)
```

Measures how long jobs wait relative to how long they run. Backfill, preemption,
and priority decay all reduce this ratio — the score captures their combined effect
without requiring the operator to report which features are configured.

| Ratio  | Score | What it means |
|--------|-------|---------------|
| < 0.10 | 1.00  | Jobs wait less than 10% of their runtime |
| < 0.25 | 0.85  | |
| < 0.50 | 0.70  | |
| < 1.00 | 0.50  | Jobs wait as long as they run |
| < 2.00 | 0.30  | |
| ≥ 2.00 | 0.10  | Jobs wait more than twice their runtime |

Calibration: NERSC Perlmutter median wait ~15 min / median job ~4 hrs → ratio ~0.06.
University HPC average: ratio ~2.0. Source: NERSC Annual Reports 2022–2023.

**Signal 2 — Small-job wait advantage (35% of queue incentive)**

```
small_job_wait_ratio = median_wait(jobs ≤ 2 GPUs) / median_wait(jobs ≥ 8 GPUs)
```

Backfill's measurable signature: small jobs fill scheduling gaps and start faster
than large jobs. Ratio < 1.0 indicates backfill is producing its intended effect.

| Ratio  | Score |
|--------|-------|
| < 0.40 | 1.00  |
| < 0.60 | 0.85  |
| < 0.80 | 0.65  |
| < 1.00 | 0.45  |
| ≥ 1.00 | 0.20  |

**Signal 3 — Wait time spread (25% of queue incentive)**

```
wait_spread_ratio = p90(queue_wait_hours) / p10(queue_wait_hours)
```

Fairshare and priority decay narrow the spread of wait times across users and jobs.
Low ratio = relatively uniform access. High ratio = structural unfairness.

| Ratio   | Score |
|---------|-------|
| < 3.0   | 1.00  |
| < 5.0   | 0.80  |
| < 10.0  | 0.55  |
| < 20.0  | 0.30  |
| ≥ 20.0  | 0.10  |

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

## Computing queue metrics from a job trace

Use `pace.queue_metrics.compute_queue_metrics()` to compute all three signals
from any job trace CSV with submit_time, start_time, end_time, and GPU count columns:

```python
from pace.queue_metrics import compute_queue_metrics

metrics = compute_queue_metrics(
    "sacct_export.csv",
    submit_col="submit",
    start_col="start",
    end_col="end",
    gpu_col="allocgres",
)

# metrics.scheduling_pressure_ratio → float
# metrics.small_job_wait_ratio      → float
# metrics.wait_spread_ratio         → float
# metrics.short_job_pct             → float
# metrics.jobs_analyzed             → int
# metrics.confidence                → "high" | "medium" | "low"
```

The helper accepts column name overrides so it works with sacct, Alibaba Helios,
Microsoft Philly, and SURFsara trace formats.

## Worked example

**Input** (Slurm cluster, computed from job traces):

```
total_gpu_requested    = 1,200,000 GPU-hours
total_gpu_used         = 864,000 GPU-hours
→ gpu_accuracy_ratio   = 0.720 → score 0.65 (Good band)

scheduling_pressure_ratio = 1.8  (jobs wait 1.8x their runtime)
→ scheduling_pressure_score = 0.30

small_job_wait_ratio      = 0.95 (small jobs barely faster)
→ small_job_advantage_score = 0.45

wait_spread_ratio          = 12.0 (p90 wait = 12x p10 wait)
→ wait_spread_score         = 0.30

queue_incentive = 0.30×0.40 + 0.45×0.35 + 0.30×0.25
               = 0.120 + 0.158 + 0.075
               = 0.353

fragmentation (gpu_waste_pct = 28%):
→ fragmentation_score = 0.90 (Moderate band, penalty 0.10)
```

**Calculation:**

```
pace_composite_score =
  (0.650 × 0.50) + (0.353 × 0.30) + (0.900 × 0.20)
= 0.325 + 0.106 + 0.180
= 0.611
```

## ACE cross-engine correlation

Low ACE + Low PACE → systemic. The scheduler is producing the underutilization.
Fix the scheduler first — configuration changes, zero downtime.

Low ACE + High PACE → workload. The scheduler is well-configured but the work
is inherently variable. Remediation: workload profiling and job right-sizing.

High ACE + Low PACE → fragile. The cluster performs today but the scheduling
structure is weak. A change in workload mix will expose it.

## Input schema

### Slurm path

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| total_gpu_requested | float | yes | Total GPU-hours requested across all jobs |
| total_gpu_used | float | yes | Total GPU-hours actually consumed |
| total_cpu_requested | float | yes | Total CPU-hours requested |
| total_cpu_used | float | yes | Total CPU-hours consumed |
| scheduling_pressure_ratio | float | no | median_wait / median_duration — from job traces |
| small_job_wait_ratio | float | no | wait(small jobs) / wait(large jobs) — from job traces |
| wait_spread_ratio | float | no | p90_wait / p10_wait — from job traces |
| short_job_pct | float | no | Fraction of jobs running under 1 minute |

When scheduling_pressure_ratio, small_job_wait_ratio, and wait_spread_ratio are
all provided, the data-driven queue incentive is used. Otherwise falls back to
the deprecated self-reported feature flag path.

### Kubernetes path

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| k8s_resource_request_ratio | float | yes | Mean(actual_gpu / requested_gpu) across pods |
| k8s_avg_pod_pending_minutes | float | yes | Average time pods wait before scheduling |
| k8s_quota_utilization | float | yes | GPU quota used / GPU quota granted (0.0–1.0) |

## CLI usage

```bash
# Analyze a Slurm cluster with data-driven queue metrics
pace analyze \
  --gpu-hours-requested 1200000 \
  --gpu-hours-used 864000 \
  --scheduling-pressure-ratio 1.8 \
  --small-job-wait-ratio 0.95 \
  --wait-spread-ratio 12.0

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

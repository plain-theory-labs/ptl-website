---
title: ACE — Adaptive Compute Efficiency Engine
description: ACE measures GPU utilization across Slurm, Kubernetes, and DCGM telemetry sources.
---

The Adaptive Compute Efficiency Engine (ACE) measures GPU utilization — the fraction of allocated GPU compute that jobs actually use. ACE is the highest-weighted engine in the PTL composite and the most direct measure of whether a cluster is doing the work it claims to do.

:::note[Version]
ACE v2.0.0 · Released 2026-03-16
:::

## Primary metric

`gpu_efficiency_rate` — GPU-hours weighted efficiency. Of all the GPU-hours allocated across all jobs, what fraction did useful compute work? This is the metric GRADE uses in the composite score.

```
gpu_efficiency_rate = gpu_hours_used / gpu_hours_requested
                    = Σ(used_gpus_i × duration_i) / Σ(requested_gpus_i × duration_i)
```

Large, long jobs contribute proportionally more than small, short jobs. This correctly reflects infrastructure efficiency: wasted GPU-hours equal wasted energy. A cluster running a few large wasteful jobs cannot hide behind many small efficient ones.

## Secondary metric

`gpu_efficiency_score` — per-job mean utilization. Equal weight per job regardless of size or duration.

```
gpu_efficiency_score = (1/N) × Σ(used_gpus_i / requested_gpus_i)
```

This is useful for scheduler analysis — it captures how many scheduling decisions produced poorly-calibrated jobs. PACE uses `flagged_jobs_pct` (derived from this threshold) for its calibration rate calculation.

## Why two metrics

A cluster running 1,000 small efficient jobs (0.9 utilization) and 10 large wasteful jobs (0.1 utilization, 100× the GPU-hours) scores:
- `gpu_efficiency_score`: 0.89 (looks good — most jobs are efficient)
- `gpu_efficiency_rate`: 0.11 (tells the truth — large jobs dominate resources)

GRADE uses `gpu_efficiency_rate`. Both are reported in ACE findings.

## Worked example

**Input** (three jobs from a Slurm sacct export):

| Job ID | GPUs requested | Duration (hrs) | GPUs used | Utilization |
|--------|----------------|----------------|-----------|-------------|
| 1041   | 8              | 10.0           | 7.2       | 0.900       |
| 1042   | 4              | 0.5            | 0.8       | 0.200       |
| 1043   | 8              | 8.0            | 6.4       | 0.800       |

**Calculation:**

```
gpu_hours_requested = (8×10) + (4×0.5) + (8×8) = 80 + 2 + 64 = 146
gpu_hours_used      = (7.2×10) + (0.8×0.5) + (6.4×8) = 72 + 0.4 + 51.2 = 123.6

gpu_efficiency_rate  = 123.6 / 146 = 0.847   ← GRADE primary
gpu_efficiency_score = (0.9 + 0.2 + 0.8) / 3 = 0.633  ← secondary
```

Job 1042 is small and short — it barely moves `gpu_efficiency_rate` but is flagged for right-sizing by the per-job threshold.

**Validated against:** MIT Supercloud HPCA22 dataset — 73,367 production jobs.
- `gpu_efficiency_rate`: 0.339 (GRADE primary)
- `gpu_efficiency_score`: 0.257 (per-job mean, secondary)

## Input paths

ACE supports four input paths, selected based on PROFILE's routing manifest:

- `claw` — CLAW telemetry (highest fidelity, process-level GPU activity)
- `dcgm` — NVIDIA DCGM metrics (`DCGM_FI_DEV_GPU_UTIL`)
- `k8s_metrics` — Kubernetes pod GPU metrics
- `sacct` — Slurm scheduler accounting (standard; used when nothing else is available)

PROFILE sets the priority order. If DCGM metrics are available alongside `sacct`, ACE uses DCGM.

## Findings ACE produces

| Field | Description |
|---|---|
| `gpu_efficiency_score` | Primary score (0.0–1.0) |
| `jobs_analyzed` | Number of jobs in the assessment window |
| `avg_job_gpu_utilization` | Mean GPU utilization across all jobs |
| `gpu_hours_requested` | Total GPU-hours requested by jobs |
| `gpu_hours_used` | Total GPU-hours actually utilized |
| `flagged_jobs_count` | Jobs below the 40% utilization threshold |
| `near_zero_jobs_pct` | Jobs below 5% utilization (likely walltime padding) |
| `short_jobs_pct` | Jobs under 5 minutes (scheduling overhead concern) |
| `jobs_flagged_for_rightsizing` | Jobs where right-sizing could improve score |

## Input schema

ACE accepts a JSON or CSV input depending on the input path. For the sacct path:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| job_id | string | yes | Slurm job identifier |
| requested_gpus | float | yes | GPUs allocated by scheduler |
| used_gpus | float | yes | GPUs actually utilized |
| duration_minutes | float | yes | Actual job runtime |
| state | string | yes | Job final state (COMPLETED, FAILED, etc.) |
| submit_time | ISO8601 | no | Job submission timestamp |
| user | string | no | Submitting user (for per-user findings) |

For the DCGM path, ACE accepts `DCGM_FI_DEV_GPU_UTIL` metric streams. For the Kubernetes path, ACE accepts pod GPU metric exports from kubectl top or metrics-server.

## What low ACE scores mean

An ACE score below 0.40 typically indicates one of three patterns: walltime padding (jobs request 24 hours, run for 4), GPU over-requesting (scripts request 8 GPUs for workloads that saturate 2), or idle job proliferation (misconfigured scripts that acquire GPUs and stall).

ATLAS receives the ACE findings and generates specific remediation text. For MIT Supercloud (score 0.257), ATLAS recommended auditing the top 10 job scripts by GPU-hours wasted and enabling `--gpu-bind=closest` in Slurm defaults.

## CLI usage

```bash
# Analyze a Slurm sacct export
ace analyze --input jobs.csv --input-path sacct

# Analyze with DCGM telemetry
ace analyze --input dcgm_metrics.json --input-path dcgm

# Analyze a Kubernetes cluster
ace analyze --input k8s_pod_metrics.json --input-path k8s_metrics

# Analyze with CLAW agent output
ace analyze --input claw_package.json --input-path claw

# Output to JSON
ace analyze --input jobs.csv --output ace_result.json
```

## Source

- [View ACE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/ace)
- [ACE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/ace_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

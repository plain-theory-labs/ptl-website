---
title: ACE — Adaptive Compute Efficiency Engine
description: ACE measures GPU utilization across Slurm, Kubernetes, and DCGM telemetry sources.
---

The Adaptive Compute Efficiency Engine (ACE) measures GPU utilization — the fraction of allocated GPU compute that jobs actually use. ACE is the highest-weighted engine in the PTL composite and the most direct measure of whether a cluster is doing the work it claims to do.

## Primary metric

`gpu_efficiency_score` — a number from 0.0 to 1.0. The formula is the mean of per-job GPU utilization across all analyzed jobs.

The score is linear and direct: 25.7% average GPU utilization produces a score of 0.257. There is no curve and no adjustment for workload type. A cluster where jobs request eight GPUs and use two earns a 0.25.

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

## What low ACE scores mean

An ACE score below 0.40 typically indicates one of three patterns: walltime padding (jobs request 24 hours, run for 4), GPU over-requesting (scripts request 8 GPUs for workloads that saturate 2), or idle job proliferation (misconfigured scripts that acquire GPUs and stall).

ATLAS receives the ACE findings and generates specific remediation text. For MIT Supercloud (score 0.257), ATLAS recommended auditing the top 10 job scripts by GPU-hours wasted and enabling `--gpu-bind=closest` in Slurm defaults.

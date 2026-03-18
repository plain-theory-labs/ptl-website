---
title: ACE — Adaptive Compute Efficiency Engine
description: ACE measures GPU utilization across Slurm, Kubernetes, and DCGM telemetry sources.
---

The Adaptive Compute Efficiency Engine (ACE) measures GPU utilization — the fraction of allocated GPU compute that jobs actually use. ACE is the highest-weighted engine in the PTL composite and the most direct measure of whether a cluster is doing the work it claims to do.

:::note[Version]
ACE v2.0.0 · Released 2026-03-16
:::

## Primary metric

`gpu_efficiency_score` — a number from 0.0 to 1.0. The formula is the mean of per-job GPU utilization across all analyzed jobs.

The score is linear and direct: 25.7% average GPU utilization produces a score of 0.257. There is no curve and no adjustment for workload type. A cluster where jobs request eight GPUs and use two earns a 0.25.

## Formula

The gpu_efficiency_score is the mean of per-job GPU utilization across all jobs in the assessment window:

```
gpu_efficiency_score = (1/N) × Σ(used_gpus_i / requested_gpus_i)

where:
  N                  = number of jobs analyzed
  used_gpus_i        = actual GPU utilization for job i
  requested_gpus_i   = GPUs requested by job i
```

The score is linear and direct. No curve, no adjustment for workload type. A job that requests 8 GPUs and uses 2 contributes 0.25 to the mean.

## Worked example

**Input** (three jobs from a Slurm sacct export):

| Job ID | GPUs requested | GPUs used | Utilization |
|--------|----------------|-----------|-------------|
| 1041   | 8              | 7.2       | 0.900       |
| 1042   | 4              | 0.8       | 0.200       |
| 1043   | 8              | 6.4       | 0.800       |

**Calculation:**

```
gpu_efficiency_score = (0.900 + 0.200 + 0.800) / 3
                     = 1.900 / 3
                     = 0.633
```

**Result:** ACE score 0.633 — Capable range. Job 1042 is flagged for right-sizing: it requested 4 GPUs and used 0.8, contributing a 0.200 to the mean. ATLAS would identify this job by script and recommend reducing its GPU request to 1.

**Validated against:** MIT Supercloud HPCA22 dataset — 73,367 production jobs, gpu_efficiency_score = 0.257.

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

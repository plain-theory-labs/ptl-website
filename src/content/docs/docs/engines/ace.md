---
title: ACE — Adaptive Compute Efficiency Engine
description: ACE measures GPU utilization across Slurm, PBS, LSF, XDMoD, Kubernetes, and DCGM telemetry sources. It is the highest-weighted engine in the PTL composite and the most direct measure of whether a cluster is doing the work it claims to do.
---

The Adaptive Compute Efficiency Engine (ACE) answers one question: of all the GPU compute your cluster allocated, how much of it did useful work? ACE ingests job accounting data from every major HPC scheduler — Slurm, PBS Pro, LSF, and XDMoD-aggregated multi-scheduler environments — alongside live hardware telemetry from NVIDIA DCGM and Kubernetes pod metrics. It scores each job against a documented efficiency methodology, identifies the exact scripts and workload types driving waste, blocks right-sizing recommendations it cannot defend (memory-bound jobs, healthy repeat scripts, multi-GPU topology constraints), and produces a structured export consumed by GRADE for certification scoring. The result is the single most actionable signal in a PTL certification: a GPU-hours-weighted efficiency rate that tells the truth about physical resource consumption rather than masking large wasteful jobs behind a count of small efficient ones.

:::note[Version]
ACE v0.3.0 · Released 2026-05-09
:::

## Primary metric

`gpu_efficiency_rate` — GPU-hours weighted efficiency. Of all the GPU-hours allocated across all jobs in the assessment period, what fraction did useful compute work?

```
gpu_efficiency_rate = gpu_hours_used / gpu_hours_requested
                    = Σ(used_gpus_i × duration_i) / Σ(requested_gpus_i × duration_i)
```

Large, long jobs count proportionally more than small, short jobs. A cluster running 1,000 small efficient jobs and 10 large wasteful jobs (100× the GPU-hours) cannot hide behind the small ones. This is the metric GRADE uses in the certification composite.

## Secondary metric

`gpu_efficiency_score` — per-job mean utilization. Equal weight per job regardless of size or duration. Used by ATLAS for human-readable display ("current utilization: 25.7%") and by PACE for job calibration rate computation.

## Why two metrics

MIT Supercloud (73,367 real Slurm jobs, HPCA22 dataset):

| Metric | Value | What it says |
|---|---|---|
| `gpu_efficiency_score` | 0.257 | Most jobs underutilize GPUs |
| `gpu_efficiency_rate` | 0.339 | Large jobs are relatively better utilized |

GRADE uses `gpu_efficiency_rate`. Both are reported in ACE findings.

## Worked example

| Job | GPUs requested | Duration (hrs) | Utilization |
|---|---|---|---|
| 1041 | 8 | 10.0 | 90% |
| 1042 | 4 | 0.5 | 20% |
| 1043 | 8 | 8.0 | 80% |

```
gpu_hours_requested = (8×10) + (4×0.5) + (8×8) = 146
gpu_hours_used      = (7.2×10) + (0.8×0.5) + (6.4×8) = 123.6

gpu_efficiency_rate  = 123.6 / 146 = 0.847   ← GRADE primary
gpu_efficiency_score = (0.9 + 0.2 + 0.8) / 3 = 0.633  ← secondary
```

Job 1042 is small and short — it barely moves `gpu_efficiency_rate` but is
flagged for right-sizing by the per-job threshold.

## Input paths

ACE selects the highest-fidelity source available based on PROFILE's routing manifest:

| Source | Command | What it measures |
|---|---|---|
| `sacct` | `ace ingest --source slurm-sacct` | Slurm scheduler accounting — job-level GPU requests, elapsed, state |
| `pbs-accounting` | `ace ingest --source pbs-accounting` | PBS Pro / OpenPBS / TORQUE accounting log |
| `xdmod` | `ace ingest --source xdmod` | Open XDMoD CSV export — normalizes Slurm, PBS, SGE through one interface |
| `lsf-bacct` | `ace ingest --source lsf-bacct` | IBM LSF `bacct -csv` output |
| `dcgm` | `ace analyze input --input-path dcgm` | NVIDIA DCGM hardware telemetry (highest confidence) |
| `k8s_metrics` | `ace analyze input --input-path k8s_metrics` | Kubernetes pod GPU metrics |
| `claw` | CLAW agent | Live collection agent — routes to sacct or canonical path |

All four scheduler paths produce an identical canonical CSV format so all downstream analysis and GRADE export paths work without modification.

## Job health tracking

ACE counts all submitted GPU jobs regardless of completion state. Silently dropping failed jobs was the previous behaviour — it understated waste.

| Finding | Definition |
|---|---|
| `job_failure_rate` | FAILED + OOM + BOOT_FAIL / submitted GPU jobs |
| `node_fail_rate` | NODE_FAIL / submitted — hardware-induced failures |
| `job_cancel_rate` | CANCELLED + PREEMPTED / submitted |
| `job_timeout_rate` | Jobs that hit their walltime limit / submitted |
| `early_fail_rate` | Jobs that failed within 5 minutes of start / submitted |

PBS and LSF walltime-exceeded kills are detected by exit code (default: 137, 271) and by a heuristic: if elapsed ≥ 95% of requested walltime and the job failed, it is classified as timeout.

## Walltime efficiency

When the scheduler export includes a requested walltime field (`Timelimit` in Slurm, `Resource_List.walltime` in PBS, `requested_walltime` in XDMoD, `RUN_LIMIT` in LSF):

| Finding | Definition |
|---|---|
| `walltime_efficiency_rate` | mean(elapsed / timelimit) across completed jobs |
| `walltime_overrequest_pct` | fraction of jobs that used < 50% of their requested walltime |

A cluster where 60% of jobs use less than half their requested walltime is holding queue slots open longer than necessary — different waste from GPU underutilization, and invisible without this signal.

## Memory bandwidth and capacity

When DCGM telemetry is available:

- **Memory bandwidth** (`DCGM_FI_DEV_MEM_COPY_UTIL`): effective utilization per GPU = max(compute%, memory_bandwidth%). Memory-bandwidth-bound workloads like LLM inference run at low compute utilization by design — using max() prevents incorrect flagging.
- **Memory capacity** (`DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_TOTAL`): when framebuffer utilization exceeds 80%, ACE blocks right-sizing recommendations for that job. Reducing GPU count when model weights fill available memory causes OOM.

## Right-sizing accuracy

ACE applies four guards before recommending a GPU count reduction:

| Guard | Condition | Outcome |
|---|---|---|
| Memory-bound | `mem_capacity_pct > 0.80` | Keep — reducing GPUs causes OOM |
| Group-healthy | Job is in a group where p90 util ≥ threshold | Keep — this run is an outlier; investigate, don't right-size |
| High utilization | Util ≥ 80% | Keep — already efficient |
| Topology-aware | `--topology-aware` flag | Round recommendation down to nearest valid GPU count (1, 2, 4, 8, 16, 32, 64) |

## Workload-type-aware thresholds

The flagging threshold adapts to workload type, read from PROFILE via `--profile`:

| Workload type | Threshold | Rationale |
|---|---|---|
| `inference_realtime` | 0.30 | Memory-bandwidth-bound; 30-40% compute util is correct |
| `inference_batch` | 0.35 | — |
| `preprocessing` | 0.45 | CPU-GPU pipeline bottlenecks are expected |
| `mixed` | 0.50 | — |
| `training_small` | 0.55 | — |
| `training_large` | 0.60 | Default — calibrated for large-scale distributed training |

## Repeat job grouping

ACE groups runs of the same job script (by `jobname` from the scheduler) and computes a utilization distribution across all runs in the period:

- **Group p90 ≥ threshold (group-healthy):** individual low-efficiency runs are outliers. ACE overrides the right-sizing recommendation to "investigate this run" — the script is well-tuned; this particular execution had a problem.
- **Group p90 < threshold (chronic underutilization):** every run is inefficient. Right-size the request.

This prevents a script that normally runs at 85% GPU utilization from accumulating a permanent right-sizing recommendation because of one bad run.

## assume_util transparency

When no per-job GPU utilization data is available (sacct-only, no DCGM), ACE accepts `--assume-util` to assign a uniform utilization to all jobs. When this mode is active, the export includes:

- An `assumed_utilization_warning` finding with `confidence: low`
- A top-level `"warnings"` list stating the value applied and that `gpu_efficiency_rate` is a uniform assumption, not a measurement

A certification produced with `assume_util` looks numerically identical to a real measurement. The warning makes the distinction visible.

## Full findings list

| Metric | Description |
|---|---|
| `gpu_efficiency_rate` | GPU-hours weighted efficiency — GRADE primary |
| `gpu_efficiency_score` | Per-job mean utilization — secondary |
| `jobs_submitted` | Total GPU jobs submitted (all states) |
| `jobs_analyzed` | GPU jobs used for utilization analysis (completed + timeout) |
| `gpu_hours_requested` | Σ(requested_gpus × elapsed_hours) |
| `gpu_hours_used` | Σ(used_gpus × elapsed_hours) |
| `flagged_jobs_pct` | Fraction of jobs below the workload-type threshold |
| `flagged_jobs_count` | Count of flagged jobs |
| `near_zero_jobs_pct` | Fraction of jobs below 5% utilization |
| `short_jobs_pct` | Fraction of jobs completing under 1 minute |
| `over_request_ratio` | avg_requested / avg_used |
| `job_failure_rate` | Application-error failures / submitted |
| `node_fail_rate` | Hardware failures / submitted |
| `job_cancel_rate` | Cancellations / submitted |
| `job_timeout_rate` | Walltime-exceeded / submitted |
| `early_fail_rate` | Crash-on-start (< 5 min) / submitted |
| `walltime_efficiency_rate` | mean(elapsed / timelimit) — when timelimit available |
| `walltime_overrequest_pct` | Fraction using < 50% of requested walltime |
| `gpu_memory_capacity_pct` | mean(FB_USED/FB_TOTAL) — DCGM only |
| `job_groups_total` | Repeat job script groups with ≥ 2 runs |
| `chronic_underutil_groups` | Groups where p90 utilization < threshold |
| `assumed_utilization_warning` | Emitted when assume_util is active |

## CLI usage

```bash
# Slurm — ingest sacct export, then analyze
ace ingest --source slurm-sacct \
  --input sacct_export.csv \
  --output canonical_ace.csv

ace analyze input --input canonical_ace.csv \
  --profile profile_output.json \
  --output ace_report.txt \
  --json-out ace_report.json

# Export to ptl_output_v1.json for GRADE
ace export \
  --input ace_report.json \
  --organization "MIT Supercloud" \
  --period 2026 \
  --output ace_output.json

# PBS Pro / OpenPBS
ace ingest --source pbs-accounting \
  --input /var/spool/PBS/server_priv/accounting/20260601 \
  --output canonical_ace.csv

# XDMoD (multi-scheduler)
ace ingest --source xdmod \
  --input xdmod_jobs_export.csv \
  --output canonical_ace.csv

# LSF
ace ingest --source lsf-bacct \
  --input lsf_jobs.csv \
  --output canonical_ace.csv

# With DCGM telemetry (any scheduler)
ace ingest --source slurm-sacct \
  --input sacct_export.csv \
  --telemetry dcgm_telemetry.csv \
  --telemetry-util-col smutilization_pct_avg \
  --telemetry-mem-util-col memutilization_pct_avg \
  --output canonical_ace.csv

# Kubernetes / DCGM aggregate → ptl_output directly
ace analyze input \
  --input k8s_pod_metrics.json \
  --input-path k8s_metrics \
  --organization "My Cluster" \
  --period 2026 \
  --ptl-output ace_output.json
```

## Source

- [View ACE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/ace)
- [ACE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/ace_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

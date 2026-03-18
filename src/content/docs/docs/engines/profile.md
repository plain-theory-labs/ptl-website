---
title: PROFILE — Cluster Profile Engine
description: PROFILE characterizes your cluster and routes data to downstream PTL engines.
---

PROFILE is the first engine in every PTL assessment. It characterizes your cluster — scheduler type, GPU fleet, telemetry sources, MIG configuration — and produces the routing manifest that all downstream engines use. PROFILE is not scored. It is a prerequisite.

## What PROFILE does

*Scheduler detection.* PROFILE identifies your scheduler type — Slurm, Kubernetes, or Ray — and records the input path each downstream engine should use.

*GPU fleet characterization.* PROFILE maps your hardware inventory to PTL model keys. CORE uses this to compute hardware-workload fit. PROFILE also detects MIG (Multi-Instance GPU) configuration when present.

*Telemetry source routing.* ACE supports four input paths: CLAW telemetry, DCGM metrics, Kubernetes pod metrics, and Slurm `sacct`. PROFILE evaluates which sources are available and sets the priority order — CLAW takes precedence, then DCGM, then Kubernetes metrics, then `sacct`.

## Output

PROFILE produces a routing manifest JSON with:

- `scheduler_type` — detected scheduler (slurm, kubernetes, ray)
- `ace_input_path` — preferred telemetry source for ACE
- `pace_input_path` — scheduler path for PACE
- `gpu_fleet` — list of GPU model keys with counts
- `mig_enabled` — boolean; whether any GPUs are MIG-partitioned
- `profile_version` — engine version string

GRADE and ATLAS receive the profile path and use it to include a cluster profile section in the certification report.

## Data requirements

A standard PROFILE run requires hardware inventory — GPU model and count per node. If running in Slurm mode, `sacct` output provides job history for ACE and PACE. CLAW automates profile collection for organizations where it can be deployed.

## Source

- [View PROFILE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/profile)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

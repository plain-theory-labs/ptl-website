---
title: CLAW — NemoClaw Intake Agent
description: CLAW automates GPU telemetry collection for PTL assessments with a configurable privacy model.
---

CLAW is the PTL intake agent — software that runs inside your environment and automates the data collection step of a PTL assessment. CLAW supports three collection modes depending on your organization's data handling requirements. In all modes, CLAW is optional; a standard `sacct` export is sufficient for a full ACE, PACE, and GRADE assessment.

:::note[Version]
CLAW v0.1.0 · Released 2026-03-01
:::

## What CLAW collects

CLAW interrogates the cluster using five data sources, in priority order:

```
Priority 1 — DCGM telemetry
  Metric: DCGM_FI_DEV_GPU_UTIL
  Interval: configurable (default 60s)
  Fidelity: high — hardware-verified

Priority 2 — nvidia-smi
  Fields: GPU utilization, memory, power draw
  Interval: configurable (default 60s)
  Fidelity: high — process-level

Priority 3 — kubectl (Kubernetes clusters)
  Fields: node GPU resources, pod allocations
  Source: metrics-server or kube-state-metrics
  Fidelity: medium — scheduler-reported

Priority 4 — Slurm sacct
  Fields: job accounting, GPU hours, runtime
  Source: sacct --format export
  Fidelity: medium — scheduler-reported

Priority 5 — Inference server endpoints
  Sources: vLLM /health, NIM /health, NemoClaw agents
  Fields: server status, model loaded, request rate
  Fidelity: medium — application-level
```

## Collection modes

**Continuous automated.** CLAW runs as a background agent, collecting DCGM GPU telemetry, Slurm or Kubernetes scheduler data, and facility metrics on a configurable schedule. At the end of an assessment window, CLAW packages and delivers the dataset to PTL.

**Manual export.** CLAW runs once and produces a structured JSON export. You review the export, then deliver it to PTL through your preferred channel. The schema is documented — you can inspect every field before sending.

**Local-only privacy mode.** CLAW runs all computation inside your environment. Only computed metrics transit to PTL — not raw telemetry, not job names, not user identifiers. The privacy router is the planned v1.0 feature.

## Scheduler support

CLAW supports Slurm, Kubernetes, and Ray schedulers. In Slurm mode, CLAW augments `sacct` with DCGM GPU utilization data when available, producing higher-fidelity ACE input than `sacct` alone.

## Data schema

CLAW produces output conforming to the PTL v1 output schema (`ptl_output_v1.json`). The schema is the contract between CLAW and the engine stack. Every field has a type, a unit, and a source label.

## Current status

CLAW v0.1.0 supports manual JSON delivery with the documented schema. The v1.0 privacy router — computed metrics only transit to PTL — is in development. Organizations with strict data handling requirements can begin a pilot with a standard `sacct` export and transition to CLAW when the privacy router is available.

## NemoClaw

NVIDIA announced NemoClaw at GTC 2026. PTL's CLAW intake agent is designed to operate alongside NemoClaw for organizations adopting NVIDIA's enterprise GPU telemetry stack. Where NemoClaw provides process-level GPU activity data, CLAW ingests it as the highest-priority ACE input path.

## Installation

CLAW runs inside a NemoClaw OpenShell sandbox.

```bash
# Install via NemoClaw
nemoclaw install ptl-claw

# Or install directly
pip install ptl-claw

# Verify installation
claw --version

# Run a one-time assessment package
claw collect --output claw_package.json

# Run continuous telemetry (daemon mode)
claw daemon --interval 300 --output-dir /var/ptl/telemetry
```

## Privacy model

Data stays inside the organization's infrastructure until explicitly shared. CLAW packages telemetry locally. Transmission to PTL requires a manual step — CLAW never sends data automatically.

In NemoClaw environments, OpenShell policy controls what data CLAW can access. Network egress requires explicit operator approval via NemoClaw's network policy interface.

## Output schema

CLAW produces a structured JSON package:

| Field | Type | Description |
|-------|------|-------------|
| claw_version | string | CLAW agent version |
| collection_timestamp | ISO8601 | When collection ran |
| cluster_id | string | Unique cluster identifier |
| gpu_fleet | array | Detected GPU models and counts |
| scheduler_type | string | slurm, kubernetes, pbs, ray |
| dcgm_available | boolean | Whether DCGM metrics were collected |
| utilization_samples | array | GPU utilization time-series |
| job_accounting | object | Slurm/PBS accounting summary (if available) |
| pod_metrics | object | Kubernetes pod GPU metrics (if available) |
| inference_servers | array | Detected inference endpoints and status |
| data_sources_used | array | Which of the five sources were active |

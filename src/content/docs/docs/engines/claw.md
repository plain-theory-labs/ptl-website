---
title: CLAW — NemoClaw Intake Agent
description: CLAW automates GPU telemetry collection for PTL assessments with a configurable privacy model.
---

CLAW is the PTL intake agent — software that runs inside your environment and automates the data collection step of a PTL assessment. CLAW supports three collection modes depending on your organization's data handling requirements. In all modes, CLAW is optional; a standard `sacct` export is sufficient for a full ACE, PACE, and GRADE assessment.

:::note[Version]
<span class="ptl-badge-row"><span class="ptl-badge ptl-badge--version">engine v0.1.0</span><span class="ptl-badge ptl-badge--release">public release 2026-05-11</span><span class="ptl-badge ptl-badge--license">MIT</span><span class="ptl-badge ptl-badge--checks">checks passing</span></span>
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

Where NemoClaw-compatible process-level GPU activity data is available, CLAW can ingest it as a high-fidelity ACE input path. This integration path is optional; CLAW also supports manual JSON delivery and standard scheduler exports.

## Installation

CLAW has two interfaces: a Python CLI for standalone use, and a TypeScript plugin for NemoClaw/OpenClaw environments.

**Python CLI (standalone):**

```bash
# Install directly
pip install ptl-claw

# Run cluster discovery and package for PTL
claw collect
claw collect --output ptl_claw_package.json

# Run discovery only — no packaging
claw discover

# Print version
claw version
```

**OpenClaw plugin (compatible environments):**

```bash
# Install via OpenClaw
openclaw install ptl-claw

# One-shot collection
ptl-claw collect --profile one_shot

# Show collection status and active data sources
ptl-claw status

# Show packaged output location before transmission
ptl-claw package

# Continuous background collection
ptl-claw daemon --interval 300
```

## Privacy model

Data stays inside the organization's infrastructure until explicitly shared. CLAW packages telemetry locally. Transmission to PTL requires a manual step — CLAW never sends data automatically.

In NemoClaw environments, OpenShell policy controls what data CLAW can access. Network egress requires explicit operator approval via NemoClaw's network policy interface.

## Output schema

`claw collect` writes a JSON package (`ptl_claw_package.json` by default) with the following top-level structure:

| Field | Type | Description |
|-------|------|-------------|
| `ptl_component` | string | Always `"claw"` |
| `version` | string | CLAW agent version |
| `package_timestamp` | ISO8601 | When the package was written |
| `organization` | string | Organization name (if provided) |
| `transmission_method` | string | `"manual_v01"` in v0.1 |
| `discovery` | object | Discovery results (see below) |
| `instructions` | string | Transmission instructions |

**`discovery` object:**

| Field | Type | Description |
|-------|------|-------------|
| `ptl_claw_version` | string | CLAW version |
| `discovery_timestamp` | ISO8601 | When discovery ran |
| `collection_results` | object | Per-source results (nvidia_smi, k8s_nodes, dcgm, inference_servers) |
| `data_sources_found` | object | Per-source success boolean |

## Source

- [View CLAW source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/claw)
- [NemoClaw documentation](https://docs.nvidia.com/nemoclaw)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

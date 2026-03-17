---
title: CLAW — NemoClaw Intake Agent
description: CLAW automates GPU telemetry collection for PTL assessments with a configurable privacy model.
---

CLAW is the PTL intake agent — software that runs inside your environment and automates the data collection step of a PTL assessment. CLAW supports three collection modes depending on your organization's data handling requirements. In all modes, CLAW is optional; a standard `sacct` export is sufficient for a full ACE, PACE, and GRADE assessment.

## Collection modes

**Continuous automated.** CLAW runs as a background agent, collecting DCGM GPU telemetry, Slurm or Kubernetes scheduler data, and facility metrics on a configurable schedule. At the end of an assessment window, CLAW packages and delivers the dataset to PTL.

**Manual export.** CLAW runs once and produces a structured JSON export. You review the export, then deliver it to PTL through your preferred channel. The schema is documented — you can inspect every field before sending.

**Local-only privacy mode.** CLAW runs all computation inside your environment. Only computed metrics transit to PTL — not raw telemetry, not job names, not user identifiers. The privacy router is the planned v1.0 feature.

## Scheduler support

CLAW supports Slurm, Kubernetes, and Ray schedulers. In Slurm mode, CLAW augments `sacct` with DCGM GPU utilization data when available, producing higher-fidelity ACE input than `sacct` alone.

## Data schema

CLAW produces output conforming to the PTL v1 output schema (`ptl_output_v1.json`). The schema is the contract between CLAW and the engine stack. Every field has a type, a unit, and a source label. The schema is public at [github.com/plain-theory-labs/ptl-engines](https://github.com/plain-theory-labs/ptl-engines).

## Current status

CLAW v0.1.0 supports manual JSON delivery with the documented schema. The v1.0 privacy router — computed metrics only transit to PTL — is in development. Organizations with strict data handling requirements can begin a pilot with a standard `sacct` export and transition to CLAW when the privacy router is available.

## NemoClaw

NVIDIA announced NemoClaw at GTC 2026. PTL's CLAW intake agent is designed to operate alongside NemoClaw for organizations adopting NVIDIA's enterprise GPU telemetry stack. Where NemoClaw provides process-level GPU activity data, CLAW ingests it as the highest-priority ACE input path.

---
title: Plain Theory Labs
description: Documentation for the PTL assessment framework for AI compute infrastructure.
---

Plain Theory Labs is an open, independent assessment framework for AI compute infrastructure. We measure what GPU clusters are doing, score those observations against a documented methodology, and deliver reproducible findings with disclosed assumptions.

## What PTL produces

A PTL assessment produces a PTL Score — a number between 0.0 and 1.0 — derived from analytical engines running independently against the provided data. The score determines the assessment tier. The tier is shorthand. The score carries the detail.

## Nine engines

Each engine addresses a distinct dimension of infrastructure performance:

*Data collection.* PROFILE characterizes your cluster — scheduler type, GPU fleet, telemetry sources — and routes data to downstream engines. CLAW is the intake agent. It installs as an OpenClaw plugin (`openclaw install ptl-claw`) and automates data collection inside NemoClaw environments.

*Efficiency measurement.* ACE (Adaptive Compute Efficiency Engine) measures GPU utilization from Slurm, Kubernetes, or DCGM telemetry. PACE measures scheduler efficiency — how well your cluster allocates resources across competing workloads.

*Facility and hardware.* COOL measures cooling system performance relative to a PUE benchmark. FLUX grades your carbon accounting methodology. CORE evaluates hardware-workload fit, fleet age, and embodied carbon.

*Scoring and recommendations.* GRADE aggregates engine scores into a composite PTL Score and produces the assessment report. ATLAS generates a ranked action plan — the specific changes most likely to improve your score in the next assessment.

## Public dataset examples

These results were computed from publicly available GPU cluster datasets. Every number is intended to be reproducible from source data using open converters in the ptl-engines repository.

| Organization        | ACE Score | Telemetry      | Jobs    | Reference        |
|---------------------|-----------|----------------|---------|------------------|
| MIT Supercloud      | 0.339     | DCGM           | 73,367  | Samsi et al., SC22 |
| Alibaba Helios 2020 | 0.214     | Hardware sensor | 361,498 | Weng et al., NSDI 2022 |
| Microsoft Philly 2017 | 0.502   | nvidia-smi     | 74,020  | Jeon et al., USENIX ATC 2019 |

ACE reports two efficiency metrics for each dataset:
- **GPU-hours weighted efficiency (GRADE primary)** — of all GPU-hours allocated, what fraction did useful work. This is the primary GRADE input.
- **Per-job mean utilization** — average per-job GPU utilization, equal weight per job. This is what most facilities self-report internally.

GRADE uses the GPU-hours weighted metric because it reflects infrastructure efficiency in physical terms: wasted GPU-hours equal wasted energy. The public examples are comparable with published EE HPC WG benchmarks for GPU environments.

Methodology worked examples using public datasets are available in [ptl-methodology/VALIDATION.md](https://github.com/plain-theory-labs/ptl-methodology/blob/main/VALIDATION.md) with full assumptions documented. These are illustrations of the methodology, not independent endorsements of any facility.

## Longitudinal assessment

A PTL assessment is designed to be repeatable. Year one is a baseline. Year three is a trend. Organizations that improve from DEVELOPING to CAPABLE to OPTIMIZED across assessments have a documented record of what changed and how the score moved. PTL maintains the assessment method. You own the findings.

## Get started

Read [how assessment works](/docs/certification/) or [start a pilot](/docs/pilot/).

## Repositories

Every number PTL produces is reproducible from source. The engines, methodology, and this documentation site are all public.

| Repository | Description | License |
|------------|-------------|---------|
| [ptl-engines](https://github.com/plain-theory-labs/ptl-engines) | All nine analytical engines, public fixtures, dataset converters, 1,426 passing tests | MIT |
| [ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) | Scoring formulas, coefficients, tiers | CC BY 4.0 |
| [ptl-website](https://github.com/plain-theory-labs/ptl-website) | This documentation site | MIT |
| [ptl-context](https://github.com/plain-theory-labs/ptl-context) | Engineering session logs and internal notes — not methodology or scoring logic | Private |

All methodology is public and citable. Source code is open under MIT license. The organization is at [github.com/plain-theory-labs](https://github.com/plain-theory-labs).

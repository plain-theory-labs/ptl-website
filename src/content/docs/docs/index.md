---
title: Plain Theory Labs
description: Documentation for the PTL certification framework for AI compute infrastructure.
---

Plain Theory Labs is an independent certification framework for AI compute infrastructure. We measure what GPU clusters are actually doing, score it against a documented methodology, and deliver findings against a published standard.

## What PTL produces

A PTL certification is a PTL Score — a number between 0.0 and 1.0 — derived from up to nine analytical engines running independently against your operational data. The score determines your certification tier. The tier is shorthand. The score is the truth.

## Nine engines

Each engine addresses a distinct dimension of infrastructure performance:

*Data collection.* PROFILE characterizes your cluster — scheduler type, GPU fleet, telemetry sources — and routes data to downstream engines. CLAW is the intake agent. It installs as an OpenClaw plugin (`openclaw install ptl-claw`) and automates data collection inside NemoClaw environments.

*Efficiency measurement.* ACE (Adaptive Compute Efficiency Engine) measures GPU utilization from Slurm, Kubernetes, or DCGM telemetry. PACE measures scheduler efficiency — how well your cluster allocates resources across competing workloads.

*Facility and hardware.* COOL measures cooling system performance relative to a PUE benchmark. FLUX grades your carbon accounting methodology. CORE evaluates hardware-workload fit, fleet age, and embodied carbon.

*Certification and recommendations.* GRADE aggregates engine scores into a composite PTL Score and produces the certification report. ATLAS generates a ranked action plan — the specific changes most likely to improve your score in the next assessment.

## Validated results

| Organization   | ACE Score | Engines Run | Data                             |
|----------------|-----------|-------------|----------------------------------|
| MIT Supercloud | 0.339     | ACE         | HPCA22 public dataset — 73,367 Slurm GPU jobs, peer-reviewed |

MIT Supercloud is the only result computed from real job-level telemetry obtained from
a public dataset. The HPCA22 release (Samsi et al., SC22) contains 73,367 production
GPU jobs from MIT's research cluster.

ACE reports two efficiency metrics for this dataset:
- **GPU-hours weighted efficiency (GRADE primary): 0.339** — of all GPU-hours allocated, 33.9% did useful work
- Per-job mean utilization: 0.257 — average per-job GPU utilization, equal weight per job

GRADE uses the GPU-hours weighted metric because it correctly reflects infrastructure
efficiency in physical terms: wasted GPU-hours equal wasted energy. Both numbers are
consistent with published EE HPC WG benchmarks for university HPC environments.

Methodology worked examples using published operational statistics (NERSC, OLCF, ALCF)
are available in [ptl-methodology/validation.md](https://github.com/plain-theory-labs/ptl-methodology)
with full assumptions documented. These are illustrations of the methodology, not
independent certifications of those facilities.

## Longitudinal certification

A PTL certification is not a one-time audit. Year one is a baseline. Year three is a dataset. Organizations that improve from DEVELOPING to CAPABLE to OPTIMIZED across assessments have a record that regulators, funders, and procurement offices can evaluate. PTL maintains the certification record. You own the findings.

## Get started

Read [how certification works](/docs/certification/) or [start a pilot](/docs/pilot/).

## Repositories

| Repository | Description | License |
|------------|-------------|---------|
| [ptl-engines](https://github.com/plain-theory-labs/ptl-engines) | All nine analytical engines — 1,184 tests | MIT |
| [ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) | Scoring formulas, coefficients, tiers | CC BY 4.0 |
| [ptl-website](https://github.com/plain-theory-labs/ptl-website) | This documentation site | MIT |
| [ptl-context](https://github.com/plain-theory-labs/ptl-context) | Engineering context and session logs | Private |

All methodology is public and citable. Source code is open under MIT license. The organization is at [github.com/plain-theory-labs](https://github.com/plain-theory-labs).

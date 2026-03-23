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

| Organization     | Score | Tier       | Data                 |
|------------------|-------|------------|----------------------|
| NERSC Perlmutter | 0.838 | Optimized  | Operational          |
| Meridian AI      | 0.808 | Optimized  | Operational          |
| OLCF Frontier    | 0.746 | Optimized  | Operational          |
| ALCF Polaris     | 0.606 | Capable    | Operational          |
| MIT Supercloud   | 0.457 | Developing | HPCA22 peer-reviewed |

## Longitudinal certification

A PTL certification is not a one-time audit. Year one is a baseline. Year three is a dataset. Organizations that improve from DEVELOPING to CAPABLE to OPTIMIZED across assessments have a record that regulators, funders, and procurement offices can evaluate. PTL maintains the certification record. You own the findings.

## Get started

Read [how certification works](/docs/certification/) or [start a pilot](/docs/pilot/).

## Repositories

| Repository | Description | License |
|------------|-------------|---------|
| [ptl-engines](https://github.com/plain-theory-labs/ptl-engines) | All nine analytical engines — 1,165 tests | MIT |
| [ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) | Scoring formulas, coefficients, tiers | CC BY 4.0 |
| [ptl-website](https://github.com/plain-theory-labs/ptl-website) | This documentation site | MIT |
| [ptl-context](https://github.com/plain-theory-labs/ptl-context) | Engineering context and session logs | Private |

All methodology is public and citable. Source code is open under MIT license. The organization is at [github.com/plain-theory-labs](https://github.com/plain-theory-labs).

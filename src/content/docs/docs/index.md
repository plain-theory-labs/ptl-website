---
title: Plain Theory Labs
description: Documentation for the PTL certification framework for AI compute infrastructure.
---

Plain Theory Labs is an independent certification framework for AI compute infrastructure. We measure what GPU clusters are actually doing, score it against a documented methodology, and deliver findings against a published standard.

## What PTL produces

A PTL certification is a PTL Score — a number between 0.0 and 1.0 — derived from up to nine analytical engines running independently against your operational data. The score determines your certification tier. The tier is shorthand. The score is the truth.

## Nine engines

Each engine addresses a distinct dimension of infrastructure performance:

*Data collection.* PROFILE characterizes your cluster — scheduler type, GPU fleet, telemetry sources — and routes data to downstream engines. CLAW is the intake agent that automates data collection where permitted.

*Efficiency measurement.* ACE (Adaptive Compute Efficiency Engine) measures GPU utilization from Slurm, Kubernetes, or DCGM telemetry. PACE measures scheduler efficiency — how well your cluster allocates resources across competing workloads.

*Facility and hardware.* COOL measures cooling system performance relative to a PUE benchmark. FLUX grades your carbon accounting methodology. CORE evaluates hardware-workload fit, fleet age, and embodied carbon.

*Certification and recommendations.* GRADE aggregates engine scores into a composite PTL Score and produces the certification report. ATLAS generates a ranked action plan — the specific changes most likely to improve your score in the next assessment.

## Longitudinal certification

A PTL certification is not a one-time audit. Year one is a baseline. Year three is a dataset. Organizations that improve from DEVELOPING to CAPABLE to OPTIMIZED across assessments have a record that regulators, funders, and procurement offices can evaluate. PTL maintains the certification record. You own the findings.

## Get started

Read [how certification works](/docs/certification/) or [start a pilot](/docs/pilot/).

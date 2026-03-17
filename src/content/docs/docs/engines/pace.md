---
title: PACE — Predictive Allocation and Cluster Efficiency
description: PACE measures scheduler efficiency — how well your cluster allocates resources across competing workloads.
---

Predictive Allocation and Cluster Efficiency (PACE) measures how well your cluster scheduler allocates resources across competing workloads. GPU efficiency (ACE) tells you whether jobs use what they request. PACE tells you whether the scheduler is giving resources to the right jobs at the right time.

## Primary metric

`pace_composite_score` — a number from 0.0 to 1.0 composed of three components:

- **Request accuracy** (50%) — how well job resource requests match actual usage
- **Queue incentive** (30%) — whether the scheduler configuration rewards efficient behavior
- **Fragmentation** (20%) — GPU node fragmentation from poorly-matched job sizes

## Slurm scoring

In Slurm mode, PACE analyzes `sacct` exports. Request accuracy is the ratio of used GPU-hours to requested GPU-hours. Queue incentive is scored from Slurm configuration — whether preemption is enabled, whether QOS policies exist, whether short-job penalties are in place.

The queue incentive component includes a short-job penalty: if more than 25% of jobs run for under 5 minutes, the queue incentive score is reduced proportionally. Short jobs indicate scheduling overhead problems, and schedulers that tolerate high short-job fractions are not directing compute efficiently.

For MIT Supercloud (41.1% short jobs), the short-job penalty reduced queue incentive by 8.2 percentage points, contributing to a PACE score of 0.475.

## Kubernetes scoring

In Kubernetes mode, PACE uses a different formula with different components:

- **Resource accuracy** (50%) — ratio of actual to requested GPU resources across pods
- **Scheduling quality** (30%) — average pod pending time in bands (0–5 min → 1.0, >60 min → 0.0)
- **Coverage** (20%) — GPU quota utilization across namespaces

PROFILE sets the input path. If your cluster runs Kubernetes, PACE runs the Kubernetes scoring path automatically.

## What low PACE scores mean

Low request accuracy indicates jobs are requesting resources they do not use — a different measurement than ACE's utilization score. Low queue incentive often indicates a scheduler with no preemption configured and no policies to reward GPU-efficient behavior. ATLAS receives the PACE findings and generates specific Slurm configuration recommendations: the exact `slurm.conf` parameters to add, with expected impact ranges.

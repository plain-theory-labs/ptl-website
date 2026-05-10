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

These results were computed directly from publicly available, peer-reviewed GPU cluster datasets. Every number is reproducible from source data using open converters in the ptl-engines repository.

| Dataset | Jobs | Telemetry source | gpu_efficiency_rate | gpu_efficiency_score |
|---|---|---|---|---|
| MIT Supercloud HPCA22 | 73,367 | DCGM telemetry | **0.339** | **0.257** |
| Alibaba Helios 2020 | 361,498 | Hardware sensor | **0.214** | **0.127** |
| Microsoft Philly 2017 | 74,020 | nvidia-smi | **0.502** | **0.320** |

`gpu_efficiency_rate` is the GPU-hours weighted metric GRADE uses for certification. `gpu_efficiency_score` is the per-job mean — the number most facilities self-report internally. The gap between them is significant: a cluster running many small efficient jobs alongside a few large wasteful ones can report a high per-job score while the majority of its GPU-hours go unused. PTL reports both. Certification is based on the weighted metric because it reflects what physically happened to the hardware.

Across all three independent production environments, GPU efficiency ranges from 21% to 50%. The pattern is consistent with published findings from the EE HPC WG and the GPU scheduling research community.

**Dataset provenance**

MIT Supercloud HPCA22 — 73,367 production GPU jobs from MIT's research cluster. Direct DCGM telemetry. Peer-reviewed at SC22 (Samsi et al.). Our primary validation reference.

Alibaba Helios 2020 — 361,498 GPU jobs from a production ML training cluster. `gpu_wrk_util` is direct hardware sensor data per GPU instance. CC BY 4.0. Published at NSDI 2022 (Weng et al.). Converter: `ace/tools/convert_helios_to_ace.py`

Microsoft Philly 2017 — 74,020 GPU jobs from Microsoft Research's internal DNN training cluster. Per-minute nvidia-smi readings per GPU, linked to job scheduling records. Published at USENIX ATC 2019 (Jeon et al.). Converter: `ace/tools/convert_philly_to_ace.py`

## Longitudinal certification

A PTL certification is not a one-time audit. Year one is a baseline. Year three is a dataset. Organizations that improve from DEVELOPING to CAPABLE to OPTIMIZED across assessments have a record that regulators, funders, and procurement offices can evaluate. PTL maintains the certification record. You own the findings.

## Get started

Read [how certification works](/docs/certification/) or [start a pilot](/docs/pilot/).

## Open source

All nine engines, the scoring methodology, and the validation converters are published under open licenses. The methodology is citable. The results are reproducible.

| Repository | Description | License |
|---|---|---|
| [ptl-engines](https://github.com/plain-theory-labs/ptl-engines) | All nine analytical engines, 220 tests, dataset converters | MIT |
| [ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) | Scoring formulas, coefficients, tiers | CC BY 4.0 |
| [ptl-website](https://github.com/plain-theory-labs/ptl-website) | This documentation site | MIT |

All methodology is public and citable. Source code is open under MIT license. The organization is at [github.com/plain-theory-labs](https://github.com/plain-theory-labs).

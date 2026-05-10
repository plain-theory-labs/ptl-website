---
title: Plain Theory Labs
description: Open-source GPU cluster efficiency certification. Nine analytical engines, published methodology, validated against 508,885 real production jobs across three peer-reviewed datasets.
---

PTL is an open-source certification framework for GPU cluster efficiency. Every engine,
every formula, and every validation dataset converter is published under MIT or CC BY 4.0
licenses. You can read the source, reproduce the numbers, and run the engines against
your own `sacct` export.

No vendor lock-in. No black-box scoring. No dashboard subscriptions.

---

## What the data shows

ACE validated against three independent production GPU cluster datasets — 508,885 real
jobs, three measurement methods, three organizations.

| Dataset | Jobs | Telemetry | `gpu_efficiency_rate` | `gpu_efficiency_score` |
|---|---|---|---|---|
| MIT Supercloud HPCA22 | 73,367 | DCGM | **0.339** | **0.257** |
| Alibaba Helios 2020 | 361,498 | Hardware sensor | **0.214** | **0.127** |
| Microsoft Philly 2017 | 74,020 | nvidia-smi | **0.502** | **0.320** |

`gpu_efficiency_rate` is GPU-hours weighted: `Σ(util × gpus × hours) / Σ(gpus × hours)`.
`gpu_efficiency_score` is per-job mean utilization — the number most clusters self-report.

The gap between them is not a rounding error. A cluster running ten large wasteful jobs
alongside a thousand small efficient ones can post a high `gpu_efficiency_score` while
wasting the majority of its GPU-hours. PTL certifies on `gpu_efficiency_rate` because
it reflects what physically happened to the hardware.

All three converters and canonical CSVs are in
[`ace/tools/`](https://github.com/plain-theory-labs/ptl-engines/tree/main/ace/tools).
Every number in this table is reproducible from the source data.

---

## How it works

PTL runs up to nine engines against your operational data. Each engine is independent.
Each produces structured findings. GRADE aggregates them into a PTL Score between 0.0
and 1.0. The score maps to a certification tier.

### Data collection

**PROFILE** characterizes your cluster: scheduler type, GPU model and count, available
telemetry sources. It produces a routing manifest that tells downstream engines which
data paths are available.

**CLAW** is the intake agent. It installs as an OpenClaw plugin:
```bash
openclaw install ptl-claw
```
Inside NemoClaw environments, CLAW automates the `sacct` export and routes it through
the canonical pipeline.

### Efficiency measurement

**ACE** — GPU utilization. Ingests Slurm `sacct`, PBS Pro accounting logs, IBM LSF
`bacct`, Open XDMoD CSV exports, NVIDIA DCGM telemetry, or Kubernetes pod metrics.
All paths normalize to the same five-column canonical CSV before analysis.

Primary metric: `gpu_efficiency_rate` (GPU-hours weighted). Secondary: `gpu_efficiency_score`
(per-job mean). Both are reported. GRADE uses the former.

**PACE** — Scheduler efficiency. Measures how well the cluster allocates resources
across competing workloads: queue wait time, backfill effectiveness, fragmentation.

### Facility and hardware

**COOL** — Cooling. Computes climate-adjusted delta PUE against a baseline benchmark.
A hot climate running the same cooling system as a cold climate should not receive the
same score.

**FLUX** — Carbon accounting methodology. Grades the rigor of your renewable energy
claims: bundled RECs, unbundled RECs, PPAs, direct generation. These are not equivalent.
FLUX scores them as such.

**CORE** — Hardware fit and fleet age. Evaluates GPU model against dominant workload
type, fleet age bands, and embodied carbon relative to utilization. Running A100s on
inference workloads they aren't suited for is a different problem from running aged GPUs.

### Certification

**GRADE** — Composite scorer. Applies engine weights, computes the PTL Score, assigns
the certification tier, and produces a structured `ptl_output_v1.json` report.

**ATLAS** — Action plan. Ranks every finding by estimated impact on the PTL Score.
Tells you which three changes will move the needle most before the next assessment.

---

## Certification tiers

| Tier | Score | What it means |
|---|---|---|
| OPTIMIZED | 0.80 – 1.00 | High efficiency, low waste, defensible carbon accounting |
| CAPABLE | 0.60 – 0.79 | Above average; specific improvements identified |
| DEVELOPING | 0.40 – 0.59 | Measurable waste; remediation plan available |
| BASELINE | 0.20 – 0.39 | Significant inefficiency; most public clusters fall here |
| UNCERTIFIED | < 0.20 | Below minimum threshold for certification |

The MIT Supercloud result (0.339) places in BASELINE. That is a peer-reviewed research
cluster at a top university. Most production clusters do not outperform it.

---

## What you need to run a pilot

A Slurm `sacct` export covering 30–90 days of GPU job history. Two hours to run the
export and send the file.

```bash
sacct -a --format=JobID,JobName,User,Partition,NCPUS,NNodes,AllocTRES,\
Elapsed,Timelimit,State,ExitCode,Submit,Start,End \
--state=CD,F,TO,CA,OOM \
--starttime=$(date -d '90 days ago' +%Y-%m-%d) \
--endtime=$(date +%Y-%m-%d) \
--parsable2 > sacct_export.csv
```

No credentials. No persistent access. No NDA required for an initial pilot.

PBS Pro, LSF, and XDMoD exports are supported with equivalent commands documented in
the [ACE engine docs](/docs/engines/ace/).

---

## Longitudinal certification

A single assessment is a measurement. Two assessments are a trend. Three assessments
are a record.

Organizations that move from DEVELOPING to CAPABLE to OPTIMIZED across annual assessments
have a documented efficiency trajectory that regulators, funders, and procurement offices
can evaluate. PTL maintains the certification record. You own the findings.

---

## Open source

| Repository | What's in it | License |
|---|---|---|
| [ptl-engines](https://github.com/plain-theory-labs/ptl-engines) | All nine engines, 220 tests, public dataset converters | MIT |
| [ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) | Scoring formulas, tier thresholds, coefficients | CC BY 4.0 |
| [ptl-website](https://github.com/plain-theory-labs/ptl-website) | This site | MIT |

The methodology is citable. The engines are forkable. The validation results are
reproducible. If the numbers are wrong, open an issue and show the diff.

[github.com/plain-theory-labs](https://github.com/plain-theory-labs)

---

## Get started

[How certification works](/docs/certification/) · [Start a pilot](/docs/pilot/) · [Recoverable value](/docs/recoverable-value/)

---
title: Recoverable Value
description: What GPU efficiency improvement is worth in dollars. Computed from public cluster datasets, not vendor estimates.
---

GPU clusters are expensive to buy, expensive to power, and expensive to cool. Most of
them are also substantially underutilized. PTL quantifies that gap — and this page shows
what closing it is worth.

These numbers come from the same public datasets used to evaluate ACE. The math
is shown. You can check it.

---

## What the data shows

Across three public GPU cluster datasets (508,885 jobs):

| Dataset | Jobs | gpu_efficiency_rate | GPU-hours wasted per 100 allocated |
|---|---|---|---|
| MIT Supercloud HPCA22 | 73,367 | 0.339 | **66.1 hours** |
| Alibaba Helios 2020 | 361,498 | 0.214 | **78.6 hours** |
| Microsoft Philly 2017 | 74,020 | 0.502 | **49.8 hours** |

`gpu_efficiency_rate` is the GPU-hours weighted metric. It measures what fraction of
allocated GPU-hours did useful compute work. The rest is waste.

A cluster at `0.339` efficiency is consuming **2.95× the energy and capital** required
to do its actual workload. The other 1.95× is overhead.

---

## The calculation

**For a 100-GPU cluster running continuously:**

```
GPU-hours per year = 100 GPUs × 8,760 hours = 876,000 GPU-hours/year
```

At MIT Supercloud's efficiency rate (0.339):
```
Useful GPU-hours  = 876,000 × 0.339 = 297,004
Wasted GPU-hours  = 876,000 × 0.661 = 578,996
```

**Cloud pricing reference (NVIDIA A100, on-demand):**

| Provider | A100 80GB | Hourly rate |
|---|---|---|
| AWS (p4d.24xlarge / 8 GPU) | per GPU | ~$4.10 |
| Azure (ND96asr_v4 / 8 GPU) | per GPU | ~$3.84 |
| GCP (a2-highgpu-8g / 8 GPU) | per GPU | ~$3.67 |

Using a conservative **$3.50/GPU-hour**:

```
Annual waste = 578,996 GPU-hours × $3.50 = $2,026,486/year
```

**On a 100-GPU cluster at 33.9% efficiency, over $2 million per year is allocated
but not doing useful work.**

---

## Recoverable value at different cluster sizes

These tables use the MIT Supercloud baseline (0.339 efficiency) and a conservative
$3.50/GPU-hour. All figures assume continuous operation.

### Moving from 0.339 → 0.55 efficiency (DEVELOPING → CAPABLE tier)

| Cluster size | Annual waste (current) | Annual waste (target) | **Recovered/year** |
|---|---|---|---|
| 50 GPUs | $1.01M | $652K | **$362K** |
| 100 GPUs | $2.03M | $1.30M | **$724K** |
| 500 GPUs | $10.1M | $6.52M | **$3.6M** |
| 1,000 GPUs | $20.3M | $13.0M | **$7.2M** |
| 5,000 GPUs | $101M | $65.2M | **$36M** |

### Moving from 0.339 → 0.70 efficiency (CAPABLE → OPTIMIZED tier)

| Cluster size | Annual waste (current) | Annual waste (target) | **Recovered/year** |
|---|---|---|---|
| 50 GPUs | $1.01M | $459K | **$554K** |
| 100 GPUs | $2.03M | $919K | **$1.1M** |
| 500 GPUs | $10.1M | $4.6M | **$5.5M** |
| 1,000 GPUs | $20.3M | $9.2M | **$11.1M** |
| 5,000 GPUs | $101M | $45.9M | **$55M** |

---

## For owned hardware (capital cost perspective)

Cloud pricing overstates the marginal cost of underutilization for owned hardware.
The relevant number for on-premise clusters is **capital utilization and energy**.

**Capital**: An NVIDIA H100 SXM5 lists at approximately $30,000–$40,000 per GPU.
A 100-GPU cluster represents $3M–$4M in capital. At 0.339 efficiency, the effective
capital doing useful work is $1.0M–$1.4M. The other $2M–$2.6M is allocated but idle.

**Energy**: GPU clusters running at 30–35% efficiency consume roughly 3× the power
required for the actual workload. At $0.10/kWh and 300W per GPU:

```
100 GPUs × 300W × 8,760 hrs × $0.10/kWh = $262,800/year (electricity alone)
At 0.339 efficiency: $178K of that powers waste
```

**Cooling**: PUE of 1.4 (typical data center) adds 40% on top of compute power.
Wasted GPU power drives wasted cooling energy at the same ratio.

---

## What PTL measures and what moves the number

PTL assessment identifies the specific levers. ACE produces a ranked list of
right-sizing recommendations — the exact jobs, scripts, and workload types
contributing most to waste, with estimated GPU-hour impact per fix.

The four highest-impact findings in order of typical contribution:

1. **Chronic underutilization** — jobs that consistently request 8 GPUs and use
   the equivalent of 1–2. These dominate `gpu_efficiency_rate` because they are
   large and long. Right-sizing the GPU request directly recovers those hours.

2. **Near-zero utilization** — jobs below 5% GPU utilization. Typically stuck
   on data loading, incorrect GPU affinity, or framework misconfiguration.
   Fixing one class of issue can move the cluster rate by several percentage points.

3. **Walltime over-request** — jobs that hold queue slots for 24 hours and finish
   in 2. Does not directly waste GPU-hours but reduces throughput and effective
   cluster capacity, increasing the per-job cost of everything else.

4. **Failed job rate** — jobs that crash within 5 minutes of start have consumed
   GPU allocation with zero useful output. At 10% early-fail rate on a 1,000-GPU
   cluster, that is 876,000 GPU-hours/year producing nothing.

---

## What PTL does not claim

PTL does not claim that any specific organization can achieve any specific efficiency
improvement. These are potential recoveries if efficiency improves — the underlying
driver of improvement is operational change, not the assessment itself.

PTL measures the current state accurately, identifies what is driving waste, and
tracks whether changes made between assessments moved the number. The recoverable
value is the difference. What you do with the findings is up to you.

---

## Source data

All efficiency rates on this page come from public datasets. The converters and
canonical CSVs are in the
[ptl-engines repository](https://github.com/plain-theory-labs/ptl-engines/tree/main/ace).
GPU pricing figures are from public cloud pricing pages as of May 2026 and may change.
Energy cost is a conservative US average from EIA.

See [ACE methodology](/docs/engines/ace/) for the exact efficiency formula.
See [Scoring methodology](/docs/methodology/scoring/) for how ACE feeds the PTL Score.

---
title: Scoring Methodology
description: How PTL computes engine scores and the composite PTL Score.
---

Every PTL engine produces a score between 0.0 and 1.0. GRADE aggregates engine scores into a composite PTL Score using published coefficients. The score is the truth. The tier is the label.

## Score-first principle

PTL reports PTL Score first. The certification tier — FRONTIER, OPTIMIZED, CAPABLE, DEVELOPING, BASELINE — is shorthand for where the score lands. The score contains more information. 0.871 and 0.852 are both FRONTIER; they are not the same. The score is always disclosed.

## Engine scores

Each engine's scoring formula is fully documented:

**ACE** — GPU-hours weighted efficiency rate: `gpu_hours_used / gpu_hours_requested`. Large, long jobs count proportionally more than small, short jobs. This correctly reflects infrastructure efficiency in physical terms. ACE also reports `gpu_efficiency_score` (per-job mean, equal job weighting) as a secondary finding for scheduler analysis.

**COOL** — continuous linear function of PUE. PUE 1.20 → 1.00; PUE 1.60 → 0.00. Every tenth of a PUE point matters.

**FLUX** — discrete score by carbon accounting method. Grid average → 0.50. Direct documented PPA → 1.00. Unbundled RECs with claimed emissions → 0.10.

**PACE** — weighted composite: request accuracy (50%), queue incentive (30%), fragmentation (20%). Queue incentive is computed from job trace data — scheduling pressure ratio, small-job wait advantage, and wait time spread — not self-reported feature flags.

**CORE** — weighted composite: hardware fit (40%), fleet age (35%), embodied carbon (25%).

## Composite scoring

GRADE computes the composite as a weighted average of engine scores using the coefficients published in [Coefficients](/docs/methodology/coefficients/). Engines not included in the assessment are excluded from the composite — they do not count as zero.

### Validated result — MIT Supercloud (real data)

MIT Supercloud, computed from the HPCA22 public dataset (73,367 Slurm GPU jobs):

```
Active engines: ACE only
Active weight sum: 0.35

ACE primary score: 0.339  (gpu_efficiency_rate — GPU-hours weighted)
  gpu_hours_used / gpu_hours_requested = 229,242 / 675,447 = 0.339
  Larger jobs weighted proportionally by resource consumption.

ACE secondary (not GRADE input): 0.257  (gpu_efficiency_score — per-job mean)
  mean(used/requested) across all 73,367 jobs, equal weighting per job.

Normalized weight: 0.35 / 0.35 = 1.00

PTL Score = 0.339 × 1.00 = 0.339
Tier: BASELINE (ACE only, first measurement)
```

### Five-engine formula illustration (hypothetical)

Demonstrating how GRADE aggregates all five engines when present:

```
Engine scores (hypothetical inputs):
  ACE  = 0.740 × 0.35 = 0.25900
  PACE = 0.853 × 0.25 = 0.21325
  COOL = 1.000 × 0.20 = 0.20000
  CORE = 0.713 × 0.12 = 0.08556
  FLUX = 1.000 × 0.08 = 0.08000
  ─────────────────────────────
  PTL Score = 0.83781 → 0.838
  Tier: OPTIMIZED (≥ 0.70, all five engines)
```

These are hypothetical values used to illustrate the formula, not
results from an actual PTL assessment.

## Confidence labels

Every metric carries a confidence label:

- `high` — derived from metered or directly measured data
- `medium` — estimated from facility reports or spot measurements
- `low` — single-point measurement, vendor specification, or estimate

Confidence is disclosed in every engine finding. An ACE score derived from DCGM telemetry carries `high` confidence. An ACE score derived from `sacct` alone carries `medium` confidence — Slurm accounting records requested GPU-hours, not actual GPU utilization.

## Assumptions

Every engine discloses its assumptions in the methodology documentation and in the certification report. If COOL assumes a PUE you reported rather than measured, that assumption is labeled. If FLUX cannot verify your power purchase agreement documentation, the finding says so.

Assumptions are not weaknesses. They are disclosed so the score can be interpreted correctly. An organization that provides metered data gets higher confidence labels and a more defensible score.

## Determinism

PTL scoring is deterministic. The same input produces the same output. This is an architectural requirement. Certification records can be verified against the engine source code and the disclosed methodology. If our methodology changes, we version the change and document what changed and why.

## Source

- [Full methodology repository](https://github.com/plain-theory-labs/ptl-methodology)
- [Scoring methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/scoring.md)
- [Suggest a methodology change](https://github.com/plain-theory-labs/ptl-methodology/issues)

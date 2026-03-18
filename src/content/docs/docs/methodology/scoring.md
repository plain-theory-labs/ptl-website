---
title: Scoring Methodology
description: How PTL computes engine scores and the composite PTL Score.
---

Every PTL engine produces a score between 0.0 and 1.0. GRADE aggregates engine scores into a composite PTL Score using published coefficients. The score is the truth. The tier is the label.

## Score-first principle

PTL reports PTL Score first. The certification tier — FRONTIER, OPTIMIZED, CAPABLE, DEVELOPING, BASELINE — is shorthand for where the score lands. The score contains more information. 0.871 and 0.852 are both FRONTIER; they are not the same. The score is always disclosed.

## Engine scores

Each engine's scoring formula is fully documented:

**ACE** — mean of per-job GPU utilization across all analyzed jobs. Linear: 0.257 average utilization → 0.257 score. No curve.

**COOL** — continuous linear function of PUE. PUE 1.20 → 1.00; PUE 1.60 → 0.00. Every tenth of a PUE point matters.

**FLUX** — discrete score by carbon accounting method. Grid average → 0.50. Direct documented PPA → 1.00. Unbundled RECs with claimed emissions → 0.10.

**PACE** — weighted composite: request accuracy (50%), queue incentive (30%), fragmentation (20%). Queue incentive includes a short-job penalty.

**CORE** — weighted composite: hardware fit (40%), fleet age (35%), embodied carbon (25%).

## Composite scoring

GRADE computes the composite as a weighted average of engine scores using the coefficients published in [Coefficients](/docs/methodology/coefficients/). Engines not included in the assessment are excluded from the composite — they do not count as zero.

### Full worked example

Using NERSC Perlmutter Q1 2026 results:

```
Engine scores:
  ACE  = 0.891 × 0.35 = 0.31185
  PACE = 0.821 × 0.25 = 0.20525
  COOL = 0.912 × 0.20 = 0.18240
  CORE = 0.880 × 0.12 = 0.10560
  FLUX = 0.850 × 0.08 = 0.06800
  ─────────────────────────────
  PTL Score = 0.87310 → 0.873
  Tier: Frontier (≥ 0.85, all five engines)
```

### Partial assessment example

Using MIT Supercloud with ACE only (first assessment):

```
Active engines: ACE only
Active weight sum: 0.35

ACE score: 0.257
Normalized weight: 0.35 / 0.35 = 1.00

PTL Score = 0.257 × 1.00 = 0.257
Tier: Baseline (ACE only, first measurement)
```

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

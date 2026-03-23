---
title: GRADE — Granular Rating for AI Datacenter Efficiency
description: GRADE aggregates engine scores into a composite PTL Score and produces the certification report.
---

Granular Rating for AI Datacenter Efficiency (GRADE) is the aggregation and reporting engine. GRADE ingests all upstream engine outputs, applies published coefficients, computes the composite PTL Score, assigns a certification tier, and produces the full certification report.

:::note[Version]
GRADE v2.0.0 · Released 2026-03-13
:::

## What GRADE produces

- **PTL Score** — composite 0.0–1.0
- **Certification tier** — FRONTIER, OPTIMIZED, CAPABLE, DEVELOPING, BASELINE, or PENDING
- **HTML certification report** — score-first layout with engine findings, ATLAS recommendations
- **Certification record** — tamper-evident cert ID with SHA256 hash

## Composite formula

GRADE computes the PTL Score as a weighted average of engine scores using published coefficients:

```
PTL_Score = Σ(engine_score_i × weight_i) / Σ(weight_i)

Current coefficients (v2.0):
  ACE  × 0.35
  PACE × 0.25
  COOL × 0.20
  CORE × 0.12
  FLUX × 0.08
  ────────────
  Sum  = 1.00
```

When an engine is excluded from the assessment, weights are normalized proportionally:

```
normalized_weight_i = weight_i / Σ(active_weights)
```

**Example:** If COOL and FLUX are excluded:

```
active_sum = 0.35 + 0.25 + 0.12 = 0.72

ACE  normalized = 0.35 / 0.72 = 0.486
PACE normalized = 0.25 / 0.72 = 0.347
CORE normalized = 0.12 / 0.72 = 0.167
```

## Worked example

**Input** (all five engines present, NERSC Perlmutter):

| Engine | Score | Weight |
|--------|-------|--------|
| ACE    | 0.740 | 0.35   |
| PACE   | 0.853 | 0.25   |
| COOL   | 1.000 | 0.20   |
| CORE   | 0.713 | 0.12   |
| FLUX   | 1.000 | 0.08   |

**Calculation:**

```
PTL_Score =
  (0.740 × 0.35) +
  (0.853 × 0.25) +
  (1.000 × 0.20) +
  (0.713 × 0.12) +
  (1.000 × 0.08)

= 0.25900 + 0.21325 + 0.20000 + 0.08556 + 0.08000
= 0.83781
```

**Result:** PTL Score 0.838 — Optimized. This matches the NERSC Perlmutter certification.

## Composite scoring

GRADE weights engine scores using published coefficients and aggregates them into the composite. Engines for which data was not provided are excluded from the composite. Partial certification is meaningful certification — a cluster certified on three engines has a real score, not a penalty for missing the other two.

Engine weights are published in [Coefficients](/docs/methodology/coefficients/).

## Tier assignment

| PTL Score | Tier | Engines required |
|-----------|------|-----------------|
| ≥ 0.85 | Frontier | All five engines |
| ≥ 0.70 | Optimized | Four or more engines |
| ≥ 0.60 | Capable | Three or more engines |
| ≥ 0.45 | Developing | Two or more engines incl. ACE |
| ACE only | Baseline | First measurement |
| None | Pending | No engines complete |

## Certification record

Every GRADE run produces a certification record with a unique cert ID in the format:

```
PTL-YYYYMMDD-ORGSLUG-TIER
```

For example: `PTL-20260317-MITSUPERCLOUD-DEVELOPING`

The cert ID is paired with a SHA256 hash of all certification fields. PTL can verify any cert ID against its record. Organizations can use the cert ID in reporting — funders, regulators, and procurement offices can request verification directly from PTL.

## Report structure

The GRADE report contains six sections:

1. **Executive summary** — tier, composite score, plain-language summary, top ATLAS recommendations, path to next tier
2. **Engine findings** — one card per engine: what was measured, the finding, the score, and what the score means
3. **Key findings** — five numbered findings with specific data callouts in monospace
4. **Path forward** — the composite gap to next tier, per-engine improvement potential sorted by maximum composite gain
5. **Recommended next steps** — ATLAS specific action text
6. **Methodology** — engine weights, tier thresholds, scoring methodology, confidence levels, disclosed assumptions

## What GRADE does not do

GRADE does not soften findings. If ACE scores 0.257, the report says 0.257 and describes what that means in operational terms. PTL's value is the specificity of the measurement. An independent certification that rounds up or adds qualitative adjustments for difficult circumstances is not a certification.

## CLI usage

```bash
# Run GRADE on individual engine output files
grade aggregate \
  --ace ace_result.json \
  --pace pace_result.json \
  --cool cool_result.json \
  --core core_result.json \
  --flux flux_result.json

# Run with partial engines (COOL and FLUX excluded)
grade aggregate \
  --ace ace_result.json \
  --pace pace_result.json \
  --core core_result.json

# Generate full certification report
grade aggregate \
  --ace ace_result.json \
  --pace pace_result.json \
  --cool cool_result.json \
  --core core_result.json \
  --flux flux_result.json \
  --org "NERSC Perlmutter" \
  --output ptl_report.json
```

## Source

- [View GRADE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/grade)
- [GRADE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/grade_methodology.md)
- [Coefficients changelog](https://github.com/plain-theory-labs/ptl-methodology/blob/main/coefficients.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

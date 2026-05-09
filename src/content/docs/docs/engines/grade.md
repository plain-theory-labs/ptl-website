---
title: GRADE — Granular Rating for AI Datacenter Efficiency
description: GRADE aggregates engine scores into a composite PTL Score and produces the certification report.
---

Granular Rating for AI Datacenter Efficiency (GRADE) is the aggregation and reporting engine. GRADE ingests all upstream engine outputs, applies published coefficients, computes the composite PTL Score, assigns a certification tier, and produces the full certification report.

:::note[Version]
GRADE v0.1.0 · Released 2026-03-13
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

**Input** (ACE only, MIT Supercloud — HPCA22 real data):

| Engine | Score | Metric | Weight (rescaled) |
|--------|-------|--------|------------------|
| ACE    | 0.339 | gpu_efficiency_rate (GPU-hours weighted) | 1.00 |

**Calculation:**

```
PTL_Score = 0.339 × 1.00 = 0.339
Tier: BASELINE (ACE only, first measurement)
```

**Result:** ACE Score 0.339 — BASELINE. 73,367 production Slurm jobs from the
MIT Supercloud HPCA22 public dataset. 33.9% of allocated GPU-hours did useful
work (GPU-hours weighted). Per-job mean utilization is 0.257 — also in the
findings, but not the GRADE primary metric.

**Five-engine methodology illustration** (hypothetical, showing formula):

| Engine | Example Score | Weight |
|--------|--------------|--------|
| ACE    | 0.740        | 0.35   |
| PACE   | 0.853        | 0.25   |
| COOL   | 1.000        | 0.20   |
| CORE   | 0.713        | 0.12   |
| FLUX   | 1.000        | 0.08   |

```
PTL_Score =
  (0.740 × 0.35) + (0.853 × 0.25) + (1.000 × 0.20) +
  (0.713 × 0.12) + (1.000 × 0.08)
= 0.83781 → 0.838 — Optimized tier
```

This illustrates how GRADE aggregates all five engines. The specific numbers
above are hypothetical inputs used to demonstrate the formula.

## Composite scoring

GRADE weights engine scores using published coefficients and aggregates them into the composite. Engines for which data was not provided are excluded from the composite — they do not count as zero. Partial certification is real certification. A cluster certified on two engines has a legitimate score on those two dimensions.

Engine weights are published in [Coefficients](/docs/methodology/coefficients/).

## Data quality tracking

GRADE tracks the input quality of each engine score and reports a composite confidence level. Not all engine inputs are equally verifiable.

| Engine | Input type |
|--------|-----------|
| ACE | Trace-derived — computed from Slurm sacct or DCGM telemetry |
| PACE | Trace-derived — computed from job wait-time metrics |
| COOL | Operator-reported — facility provides annual PUE |
| CORE | Operator-reported — facility provides hardware inventory |
| FLUX | Operator-reported — facility reports carbon accounting method |

The composite confidence label:

| Label | Meaning |
|-------|---------|
| HIGH | All present engines are trace-derived or directly measured |
| MEDIUM | Mix of trace-derived and operator-reported engines |
| LOW | All present engines are operator-reported |

When ACE and PACE are both run, the composite confidence is MEDIUM at minimum — those two engines anchor the score in measured data. A five-engine score with all operator-reported inputs (COOL + CORE + FLUX only, no ACE or PACE) carries LOW confidence.

This is displayed in the certification report and included in the certification record JSON.

## Tier assignment

| PTL Score | Tier | Engines required |
|-----------|------|-----------------|
| ≥ 0.85 | FRONTIER | All five engines |
| ≥ 0.70 | OPTIMIZED | Four or more engines |
| ≥ 0.60 | CAPABLE | Three or more engines |
| ≥ 0.45 | DEVELOPING | Two or more engines incl. ACE |
| ACE only | BASELINE | First measurement |
| None | PENDING | No engines complete |

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

GRADE does not soften findings. If ACE scores 0.339, the report says 0.339 and describes what that means in operational terms. PTL's value is the specificity of the measurement. An independent certification that rounds up or adds qualitative adjustments for difficult circumstances is not a certification.

## CLI usage

```bash
# Certify one organization from a grade_input JSON file
grade certify \
  --input grade_input.json \
  --output grade_output.json \
  --report certification_report.html

# With ATLAS recommendations section
grade certify \
  --input grade_input.json \
  --output grade_output.json \
  --report certification_report.html \
  --atlas atlas_output.json

# Run all synthetic organizations and print tiers
grade demo

# Validate a ptl_output_v1.json export against the PTL schema
grade validate --input grade_output.json
```

**Example `grade_input.json`:**

```json
{
  "organization": "NERSC Perlmutter",
  "period": "2026",
  "ace_report":  "ace_output.json",
  "pace_report": "pace_output.json",
  "cool_report": "cool_output.json",
  "core_report": "core_output.json",
  "flux_report": "flux_output.json",
  "prior_certifications": [
    {"year": "2025", "tier": "CAPABLE", "composite": 0.631}
  ]
}
```

Engines are excluded simply by omitting their report path — absent paths are not counted as zero. Partial certification is real certification.

## Source

- [View GRADE source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/grade)
- [GRADE methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/grade_methodology.md)
- [Coefficients changelog](https://github.com/plain-theory-labs/ptl-methodology/blob/main/coefficients.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

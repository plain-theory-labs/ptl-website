---
title: GRADE — Granular Rating for AI Datacenter Efficiency
description: GRADE aggregates engine scores into a composite PTL Score and produces the certification report.
---

Granular Rating for AI Datacenter Efficiency (GRADE) is the aggregation and reporting engine. GRADE ingests all upstream engine outputs, applies published coefficients, computes the composite PTL Score, assigns a certification tier, and produces the full certification report.

## What GRADE produces

- **PTL Score** — composite 0.0–1.0
- **Certification tier** — FRONTIER, OPTIMIZED, CAPABLE, DEVELOPING, BASELINE, or PENDING
- **HTML certification report** — score-first layout with engine findings, ATLAS recommendations
- **Certification record** — tamper-evident cert ID with SHA256 hash

## Composite scoring

GRADE weights engine scores using published coefficients and aggregates them into the composite. Engines for which data was not provided are excluded from the composite. Partial certification is meaningful certification — a cluster certified on three engines has a real score, not a penalty for missing the other two.

Engine weights are published in [Coefficients](/docs/methodology/coefficients/).

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

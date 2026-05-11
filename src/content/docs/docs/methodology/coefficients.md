---
title: Engine Coefficients
description: The weights PTL applies to engine scores when computing the composite PTL Score.
---

GRADE aggregates engine scores using published coefficients. The coefficients reflect the relative contribution of each dimension to overall AI compute infrastructure efficiency. Coefficients are versioned — changes are documented with rationale.

## Current coefficients (v2.0)

| Engine | Weight | Rationale |
|---|---|---|
| ACE | 0.35 | GPU utilization is the primary measure of compute efficiency |
| PACE | 0.25 | Scheduler policy determines whether utilization is achievable |
| COOL | 0.20 | Cooling overhead is the largest non-compute energy consumer |
| CORE | 0.12 | Hardware fit affects efficiency ceiling; embodied carbon is a lifecycle factor |
| FLUX | 0.08 | Carbon accounting methodology matters; weight reflects current data availability |

Coefficients sum to 1.00. When an engine is excluded from an assessment, remaining engine scores are normalized proportionally before aggregation.

## Normalization for partial assessments

If COOL and FLUX are excluded (a common pattern for first assessments), the remaining engines — ACE, PACE, CORE — are re-weighted proportionally:

- ACE: 0.35 / 0.72 = 0.486
- PACE: 0.25 / 0.72 = 0.347
- CORE: 0.12 / 0.72 = 0.167

The composite is computed against the normalized weights. The certification report discloses which engines were included and the normalized weights applied.

## Why ACE is weighted highest

GPU utilization directly measures whether allocated compute is doing useful work. A cluster where 89% of jobs run below the 40% utilization threshold is wasting the majority of its purchased GPU capacity, regardless of how well-cooled or carbon-accounted it is. ACE is weighted highest because it is the most direct measure of the fundamental problem PTL is designed to address.

## Why FLUX is weighted lowest

Carbon accounting methodology is important. It is also the dimension where organizational control is most constrained by geography, utility availability, and regulatory environment. An organization in a region with no viable PPA market cannot easily move from 0.50 to 1.00 on FLUX in one assessment cycle. The coefficient reflects this constraint — FLUX is measured and reported, but not allowed to dominate the composite.

## Coefficient versioning

Current coefficients: v2.0, published 2026-03-18. These coefficients are documented in the public methodology repository. The cleaned public repository history begins at `v0.1.0`; older pre-public tags are no longer part of the public release surface.

## Source

- [Full methodology repository](https://github.com/plain-theory-labs/ptl-methodology)
- [Coefficients document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/coefficients.md)
- [Coefficient changelog](https://github.com/plain-theory-labs/ptl-methodology/blob/main/CHANGELOG.md)
- [Propose a coefficient change](https://github.com/plain-theory-labs/ptl-methodology/issues)

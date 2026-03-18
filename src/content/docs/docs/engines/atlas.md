---
title: ATLAS — Actionable Trajectory and Longitudinal Analysis
description: ATLAS ranks the actions most likely to improve your PTL certification in the next assessment.
---

Actionable Trajectory and Longitudinal Analysis (ATLAS) receives all engine outputs and produces a ranked action plan. Each recommendation is specific enough to act on immediately — not a category of improvement but the exact configuration change, the expected impact, and the current baseline.

:::note[Version]
ATLAS v2.0.0 · Released 2026-03-13
:::

## How ATLAS ranks recommendations

ATLAS receives all engine output JSON files and ranks actions by expected composite score impact:

```
recommendation_priority =
  (expected_score_delta × engine_weight) / estimated_effort

where:
  expected_score_delta = projected improvement to engine score
  engine_weight        = that engine's coefficient in GRADE
  estimated_effort     = low (1) | medium (2) | high (3)
```

Actions are ranked highest-priority-first. ATLAS never recommends actions that require capital investment before operational changes — configuration improvements appear before hardware recommendations.

## Worked example

**Input:** MIT Supercloud engine findings

```
ACE findings:
  gpu_efficiency_score = 0.257
  flagged_jobs_count   = 18,441
  near_zero_jobs_pct   = 0.23
  short_jobs_pct       = 0.411

PACE findings:
  request_accuracy = 0.31
  queue_incentive  = 0.42
  short_job_pct    = 0.411
```

**ATLAS output (ranked):**

```
1. Audit top 10 job scripts by GPU-hours wasted
   and enable --gpu-bind=closest in Slurm defaults
   Engine: ACE + PACE · Expected delta: +0.08 composite
   Effort: low

2. Deploy per-user GPU efficiency dashboard
   Engine: ACE · Expected delta: +0.05 composite
   Effort: medium

3. Enable Slurm preemption for QOS tiers
   Engine: PACE · Expected delta: +0.03 composite
   Effort: low
```

## How ATLAS works

ATLAS computes a priority score for each potential action based on three factors: the gap between your current engine score and the maximum achievable score, the engine's weight in the PTL composite, and the operational impact (how difficult the change is to implement relative to how much it moves the composite).

The output is a ranked list of actions, where item 1 represents the highest expected composite gain per unit of operational effort.

## Routing and specialization

ATLAS reads PROFILE's routing manifest to determine which recommendation templates to apply. Kubernetes clusters receive Kubernetes-specific scheduler recommendations — not Slurm configuration changes. Clusters with CLAW telemetry available receive ACE recommendations specific to agent-mode data collection.

ATLAS maintains separate recommendation templates for:

- Slurm scheduler configuration
- Kubernetes resource policies and pending time reduction
- DCGM-enabled clusters where agent metrics are available
- Carbon accounting methodology upgrades

## Example recommendations

MIT Supercloud (PTL Score 0.450, DEVELOPING):

**Recommendation 1 — ACE (priority 0.18):**
ACE analyzed 73,367 jobs. 89% ran below the 40% GPU utilization threshold. 38.7% showed near-zero GPU activity — likely walltime padding or misconfigured job scripts. Primary action: audit the top 10 job scripts by GPU-hours wasted and implement a right-sizing policy for repeat offenders. Secondary action: enable `--gpu-bind=closest` in Slurm defaults. Expected improvement: 10–20 percentage points in average utilization (current: 25.7%).

**Recommendation 2 — PACE (priority 0.02):**
Preemption is not configured. High-priority jobs currently queue behind lower-priority jobs holding idle GPUs. Recommended: `PreemptType=preempt/qos` in `slurm.conf` with a grace period of 60–120 seconds.

## Trajectory analysis

With multi-year certification data, ATLAS generates trajectory projections — given the changes implemented since the last assessment, what composite improvement is plausible in the next assessment window. This projection is documented as an estimate with disclosed confidence. It is not a guarantee.

Trajectory analysis becomes meaningful after the second assessment. The first assessment establishes the baseline.

## CLI usage

```bash
# Generate recommendations from engine outputs
atlas recommend \
  --ace ace_result.json \
  --pace pace_result.json \
  --cool cool_result.json \
  --core core_result.json \
  --flux flux_result.json \
  --profile profile_output.json

# Output ranked recommendations to JSON
atlas recommend \
  --ace ace_result.json \
  --pace pace_result.json \
  --output atlas_recommendations.json

# Limit to top N recommendations
atlas recommend \
  --ace ace_result.json \
  --pace pace_result.json \
  --top 5
```

## Source

- [View ATLAS source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/atlas)
- [ATLAS methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/atlas_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

---
title: ATLAS — Actionable Trajectory and Longitudinal Analysis
description: ATLAS ranks the actions most likely to improve your PTL Score in the next assessment.
---

Actionable Trajectory and Longitudinal Analysis (ATLAS) receives all engine outputs and produces a ranked action plan. Each recommendation is specific enough to act on immediately — not a category of improvement but the exact configuration change, the expected impact, and the current baseline.

:::note[Version]
<span class="ptl-badge-row"><span class="ptl-badge ptl-badge--version">engine v0.1.0</span><span class="ptl-badge ptl-badge--release">public release 2026-05-11</span><span class="ptl-badge ptl-badge--license">MIT</span><span class="ptl-badge ptl-badge--checks">checks passing</span></span>
:::

## How ATLAS ranks recommendations

ATLAS receives all engine output JSON files and ranks actions by expected composite score impact:

```
recommendation_priority =
  gap × engine_weight × impact_factor

where:
  gap             = target_score - current_engine_score
  engine_weight   = ATLAS operational weight (reflects tractability,
                    not the GRADE scoring coefficient)
  impact_factor   = per-engine multiplier for operational impact

ATLAS operational weights (tractability — how quickly improvement lands):
  ACE  × 0.35  — scheduler/right-sizing, zero downtime, immediate
  PACE × 0.30  — scheduler config changes, zero downtime, immediate
  COOL × 0.20  — facilities team, medium term
  FLUX × 0.10  — utility contracts, external dependencies
  CORE × 0.05  — hardware refresh cycle, capital expenditure
```

Actions are ranked highest-priority-first. ATLAS never recommends actions that require capital investment before operational changes — configuration improvements appear before hardware recommendations.

## Worked example

**Input:** MIT Supercloud ACE findings (HPCA22 public dataset — ACE engine only)

```
ACE findings:
  gpu_efficiency_rate  = 0.339   (GRADE primary — GPU-hours weighted)
  gpu_efficiency_score = 0.257   (secondary — per-job mean)
  jobs_analyzed        = 73,367
  flagged_jobs_pct     = 0.89   (89% below utilization threshold)
  near_zero_jobs_pct   = 0.23
  short_jobs_pct       = 0.411
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

MIT Supercloud (ACE score 0.339, BASELINE — ACE engine only, GPU-hours weighted):

**Recommendation 1 — ACE (highest priority):**
ACE analyzed 73,367 jobs. 89% ran below the 60% GPU utilization threshold. Primary action: audit the top 10 job scripts by GPU-hours wasted and implement a right-sizing policy for repeat offenders. Secondary action: enable `--gpu-bind=closest` in Slurm defaults. Expected improvement: 10–20 percentage points in average utilization (current: 25.7%).

**Recommendation 2 — Add PACE analysis:**
PACE has not been run. Adding scheduler efficiency analysis will reveal whether the queue incentive structure is contributing to the low GPU utilization. Run `pace.queue_metrics.compute_queue_metrics()` on the sacct export to compute wait-time signals.

## Trajectory analysis

With multi-year assessment data, ATLAS generates trajectory projections — given the changes implemented since the last assessment, what composite improvement is plausible in the next assessment window. This projection is documented as an estimate with disclosed confidence, not a promised outcome.

Trajectory analysis becomes meaningful after the second assessment. The first assessment establishes the baseline.

## CLI usage

```bash
# Analyze one organization from an atlas_input JSON file
atlas analyze \
  --input atlas_input.json \
  --output atlas_output.json

# Run all synthetic scenarios and print ranked recommendations
atlas demo

# Validate an atlas output file
atlas validate --input atlas_output.json
```

**Example `atlas_input.json`:**

```json
{
  "organization": "MIT Supercloud",
  "period": "2026",
  "grade_report_path": "grade_output.json",
  "ace_report_path":   "ace_output.json",
  "pace_report_path":  "pace_output.json",
  "cool_report_path":  "cool_output.json",
  "core_report_path":  "core_output.json",
  "flux_report_path":  "flux_output.json",
  "prior_periods": [
    {"period": 2025, "composite": 0.521},
    {"period": 2024, "composite": 0.487}
  ]
}
```

ATLAS requires the GRADE output as its primary input (`grade_report_path`). Engine outputs are optional — when present, ATLAS generates specific recommendation text using available metric values from each engine rather than generic templates.

## Source

- [View ATLAS source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/atlas)
- [ATLAS methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/atlas_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

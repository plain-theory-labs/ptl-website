---
title: How Assessment Works
description: The PTL assessment process — data collection, engine analysis, scoring, and delivery.
---

PTL assessment is a structured process: data collection, independent engine analysis, composite scoring, and report delivery. Each step is documented before the engagement begins.

## Data collection

You provide a Slurm scheduler export and basic facility information — cooling type, location, carbon accounting method. Additional engines require additional data. Every data requirement is documented in the pilot intake form before the engagement begins. The data collection phase takes under two hours for a standard Slurm export.

CLAW, the PTL intake agent, automates data collection for organizations that can deploy it. For organizations with stricter data policies, CLAW operates in local-only mode — only computed metrics transit to PTL, not raw telemetry.

## Engine analysis

Each engine runs independently against your data. Independence is architectural — no engine imports another, and no engine's output can alter another engine's analysis. Every finding includes a confidence label and disclosed assumptions.

PROFILE runs first. It characterizes your cluster — scheduler type, GPU fleet, MIG configuration, telemetry sources — and produces the routing manifest that ACE and PACE use to select the correct input path. PROFILE is not scored; it is a prerequisite.

Scored engines: ACE, COOL, FLUX, PACE, CORE. Each produces a score between 0.0 and 1.0 and a structured findings JSON that GRADE ingests.

## GRADE scoring

GRADE aggregates engine scores using published coefficients into a composite PTL Score. Engines for which you have not provided data are excluded from the composite, and the report labels which engines were included.

The composite determines your assessment tier. See [Tiers](/docs/methodology/tiers/) for the full table.

## ATLAS recommendations

ATLAS receives the engine outputs and ranks the actions most likely to improve your score in the next assessment. Priority is determined by gap size, engine weight, and operational impact.

You receive a ranked action plan alongside your assessment report. Recommendations are specific enough to act on: not "improve GPU utilization" but the precise Slurm configuration change and estimated percentage point improvement.

## What you receive

- HTML assessment report with your PTL Score, tier, and engine findings
- Structured JSON output for all engines
- ATLAS ranked action plan
- Assessment record with a tamper-evident report ID (format: `PTL-YYYYMMDD-ORGSLUG-TIER`)

The findings belong to your organization. PTL keeps the methodology public at [github.com/plain-theory-labs/ptl-methodology](https://github.com/plain-theory-labs/ptl-methodology) under CC BY 4.0.

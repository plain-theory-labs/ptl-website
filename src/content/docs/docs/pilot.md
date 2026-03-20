---
title: Start a Pilot
description: How to begin a PTL pilot certification — what you provide, what we deliver.
---

A pilot begins with your Slurm scheduler export and four questions about your facility. We run the analysis and deliver a private certification report to your team. The data collection takes under two hours.

## What a pilot covers

A standard pilot runs ACE, PACE, and GRADE — the core efficiency engines that require only a Slurm scheduler export. If you can share facility information (cooling type, power source), we add COOL and FLUX. If you have hardware inventory data, we add CORE. You receive a PTL Score and full ATLAS recommendations for every engine we run.

## What you provide

- A Slurm `sacct` export covering at least 30 days of job history
- Facility basics: cooling type, location, grid carbon intensity estimate
- Optional: hardware inventory, power source documentation

If your Slurm export contains sensitive job names or user identifiers, we work with you to anonymize before transfer. CLAW's local-only mode computes metrics inside your environment — only the computed numbers transit to PTL.

## What we deliver

Within five business days of receiving your data:

- Full HTML certification report — PTL Score, tier, engine findings, ATLAS action plan
- Structured JSON exports for all engines you provide data for
- A working session to review findings together

You decide what to do with the results. We do not publish pilot findings without explicit permission. Pilot organizations that proceed to formal certification receive the pilot findings as their baseline assessment.

## Start a pilot

Write to [research@plaintheory.org](mailto:research@plaintheory.org). Include a brief description of your cluster — scheduler type, approximate GPU count, and primary workload category. We will send the pilot intake form within one business day.

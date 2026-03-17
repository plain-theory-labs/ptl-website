---
title: FLUX — Facility Load and Utilization Index
description: FLUX grades carbon accounting methodology and power source documentation quality.
---

The Facility Load and Utilization Index (FLUX) grades your carbon accounting methodology — how you document, measure, and report the carbon intensity of your facility's power supply. FLUX does not measure emissions. It grades the rigor of the methodology you use to measure and report them.

## Primary metric

`flux_methodology_score` — a number from 0.0 to 1.0 based on the carbon accounting method you use and the quality of documentation supporting it.

## Scoring by method

| Method | Score |
|---|---|
| PPA (direct, documented) + on-site generation | 1.00 |
| PPA (direct, documented) | 1.00 |
| Utility green tariff (documented) | 0.80 |
| Market-based RECs (bundled, documented) | 0.65 |
| Grid average (location-based) | 0.50 |
| Unbundled RECs + emissions claimed | 0.10 |
| No accounting | 0.00 |

## Greenwashing detection

FLUX includes explicit greenwashing detection. If an organization uses unbundled RECs (renewable energy credits purchased separately from power consumption) and claims zero or near-zero emissions, FLUX fires a finding at the `high` confidence level. Unbundled RECs do not demonstrate that renewable power was delivered to your facility at the time your cluster was running. The finding appears in the certification report.

## Carbon method code

FLUX exports a `carbon_method_code` integer (0–6) that ATLAS uses for routing. Organizations with lower method codes receive specific recommendations for upgrading their accounting methodology — what kind of PPA to pursue, which utility programs are available, what documentation is required.

## What FLUX rewards

*Traceability.* Can you document that the renewable power you are claiming corresponds to actual generation delivered at the time your cluster was operating? A direct PPA with a generator in your grid region is traceable. Grid average accounting is not — it is an estimate, and FLUX scores it accordingly.

The methodology is public. Organizations that disagree with our assessment of their accounting method can submit evidence for review.

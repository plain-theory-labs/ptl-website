---
title: FLUX — Facility Load and Utilization Index
description: FLUX grades carbon accounting methodology and power source documentation quality.
---

The Facility Load and Utilization Index (FLUX) grades your carbon accounting methodology — how you document, measure, and report the carbon intensity of your facility's power supply. FLUX does not measure emissions. It grades the rigor of the methodology you use to measure and report them.

:::note[Version]
FLUX v0.1.0 · Released 2026-02-14
:::

## Primary metric

`flux_methodology_score` — a number from 0.0 to 1.0 based on the carbon accounting method you use and the quality of documentation supporting it.

## Formula

FLUX uses a discrete scoring table based on carbon accounting method:

```
flux_methodology_score = method_score × documentation_multiplier

where method_score is:
  1.00  PPA (direct, documented) or on-site generation
  0.80  Utility green tariff (documented)
  0.65  Market-based RECs (bundled, documented)
  0.50  Grid average (location-based)
  0.10  Unbundled RECs + emissions claimed
  0.00  No accounting

and documentation_multiplier is:
  1.00  Full documentation provided and verified
  0.85  Partial documentation
  0.70  Self-reported, not verified
```

The greenwashing detection override applies when unbundled RECs are used and zero emissions are claimed — the score is forced to 0.10 regardless of documentation quality.

## Worked example

**Scenario A — Direct PPA:**
Organization holds a direct Power Purchase Agreement with a wind farm in the same grid region. Documentation includes the PPA contract and matching RECs.

```
flux_methodology_score = 1.00 × 1.00 = 1.00
```

**Scenario B — Grid average, self-reported:**
Organization claims grid average renewable percentage without documentation.

```
flux_methodology_score = 0.50 × 0.70 = 0.35
```

**Scenario C — Greenwashing detection:**
Organization uses unbundled RECs purchased from another region and claims zero emissions.

```
flux_methodology_score = 0.10 (override applied)
Finding: GREENWASHING_DETECTED — high confidence
```

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

## Input schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| carbon_method | string | yes | ppa_direct, utility_green, recs_bundled, grid_average, recs_unbundled, none |
| documentation_status | string | yes | verified, partial, self_reported |
| renewable_pct_claimed | float | no | Percentage of power claimed as renewable (0–100) |
| ppa_documented | boolean | no | Whether PPA documentation was provided |
| recs_bundled | boolean | no | Whether RECs are bundled with power delivery |
| grid_region | string | no | Grid region identifier for location-based accounting |

## CLI usage

```bash
# Score from carbon accounting method
flux analyze --method ppa_direct --documentation verified

# Score with full context
flux analyze \
  --method grid_average \
  --documentation self_reported \
  --renewable-pct 34

# Output to JSON
flux analyze --method ppa_direct --output flux_result.json
```

## Source

- [View FLUX source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/flux)
- [FLUX methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/flux_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

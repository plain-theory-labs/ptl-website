---
title: FLUX — Facility Load and Utilization Index
description: FLUX grades carbon accounting methodology quality and detects greenwashing by comparing claimed carbon footprints against EPA eGRID grid intensity estimates. It identifies whether carbon reporting is the binding constraint on sustainability credibility.
---

The Facility Load and Utilization Index (FLUX) grades the rigor of an organization's carbon accounting methodology — not the carbon number itself. An organization can report a very low footprint using instruments that have no physical connection to actual renewable generation. The most common example: purchasing unbundled Renewable Energy Certificates with no temporal or geographic matching, then claiming 100% renewable status while consuming from a high-carbon grid. The reported figure may be near zero. The physical reality is the full eGRID intensity times every MWh consumed. FLUX scores the method, computes what the grid actually implies, and flags the gap.

:::note[Version]
<span class="ptl-badge-row"><span class="ptl-badge ptl-badge--version">engine v0.1.0</span><span class="ptl-badge ptl-badge--release">public release 2026-05-11</span><span class="ptl-badge ptl-badge--license">MIT</span><span class="ptl-badge ptl-badge--checks">checks passing</span></span>
:::

## Primary metric

`flux_methodology_score` — a continuous 0.0–1.0 score based on the carbon accounting method used and the quality of documentation supporting it.

## Formula

```
methodology_score = min(1.0,
    method_base_score
    + (0.15 if rec_vintage_matched else 0)
    + (0.10 if ppa_documentation else 0))
```

Bonuses are additive and the total is capped at 1.0.

## Carbon accounting methods

| Method | Base score | Description |
|---|---|---|
| `ppa_direct` | 1.0 | Direct PPA — contractual link to specific generation asset |
| `ppa_proxy` | 0.8 | PPA with proxy generation data |
| `marginal` | 0.7 | Time-matched marginal emission rates |
| `grid_average` | 0.5 | Annual average eGRID factor — honest but imprecise |
| `rec_bundled` | 0.4 | Bundled RECs — weak temporal matching |
| `rec_unbundled` | 0.2 | Unbundled RECs — no temporal or geographic match |
| `unknown` | 0.0 | No methodology disclosed |

Sources: WRI GHG Protocol Scope 2 Guidance 2015, Rocky Mountain Institute — The Emissions First Principle 2022, RE100 Technical Criteria 2023.

## Bonuses

| Bonus | Value | Condition |
|---|---|---|
| `rec_vintage_matched` | +0.15 | RECs matched to the same year as consumption |
| `ppa_documentation` | +0.10 | PPA contract documentation provided |

## Letter grade

| Grade | Condition | Label |
|---|---|---|
| A | score ≥ 0.85 | Excellent |
| B | score ≥ 0.65 | Good |
| C | score ≥ 0.45 | Adequate |
| D | score ≥ 0.25 | Poor |
| F | score < 0.25 | Failing |

## Worked examples

**Direct PPA with documentation:**
```
carbon_method:     ppa_direct    → 1.0 base
ppa_documentation: true          → +0.10
rec_vintage_matched: false

methodology_score = min(1.0, 1.0 + 0.10) = 1.0
Grade: A (Excellent)
```

**Marginal with vintage-matched RECs:**
```
carbon_method:     marginal      → 0.70 base
rec_vintage_matched: true        → +0.15

methodology_score = min(1.0, 0.70 + 0.15) = 0.85
Grade: A (Excellent — at the threshold)
```

**Unbundled RECs:**
```
carbon_method:     rec_unbundled → 0.20 base
ppa_documentation: false
rec_vintage_matched: false

methodology_score = 0.20
Grade: F (Failing)
```

## eGRID carbon intensity

FLUX computes an estimated actual carbon footprint from the facility's total energy consumption and EPA eGRID 2023 grid intensity for its subregion:

```
actual_carbon_kg = total_energy_mwh × egrid_intensity_kg_mwh
carbon_delta_kg  = actual_carbon_kg - claimed_carbon_kg
```

A positive `carbon_delta_kg` means the organization's claimed footprint is below what the grid implies.

**Selected eGRID subregions (kg CO2/MWh):**

| Subregion | Intensity | States |
|---|---|---|
| MROW | 386 | MN, WI, IA, IL |
| RMPA | 617 | CO, WY |
| ERCT | 386 | TX |
| FRCC | 430 | FL |
| NPCC | 195 | NY, MA, CT |
| SERC | 394 | GA, NC, SC, TN, AL |
| WECC | 287 | CA, WA, OR, NV, AZ |
| RFCE | 285 | PA, NJ, MD, DE, DC |
| RFCW | 500 | OH, IN, WV, KY |
| HICC | 650 | HI |
| AKGD | 493 | AK |

Source: EPA eGRID 2023, Summary Tables, Table 1.

Full subregion coverage and international grid intensities in `flux/coefficients/flux_coefficients.json`.

## International support

For non-US facilities, supply the `egrid_subregion` field directly with an international grid code:

| Code | Grid | Intensity (kg CO2/MWh) |
|---|---|---|
| `EU_AVG` | EU-27 average | 276 |
| `DE` | Germany | 385 |
| `FR` | France | 58 |
| `NL` | Netherlands | 298 |
| `SE` | Sweden | 13 |
| `NO` | Norway | 7 |
| `GB` | United Kingdom | 207 |
| `CN` | China national | 537 |
| `JP` | Japan | 453 |
| `CA_ON` | Canada Ontario | 29 |
| `SG` | Singapore | 408 |
| `IN` | India | 708 |

Sources: ENTSO-E Transparency Platform 2023 (Europe), IEA World Energy Outlook 2023, China MEE National Carbon Emissions Report 2022.

## Greenwashing detection

FLUX flags greenwashing when all three conditions hold:

1. `carbon_method` is `rec_unbundled` or `rec_bundled`
2. `claimed_renewable_pct > 0`
3. `claimed_carbon_kg < actual_carbon_kg × 0.50`

The flag is a separate finding (`greenwashing_flag = 1.0`). It does not change the methodology score — the score already reflects the weakness of the REC method. The flag surfaces in the GRADE certification report with the reason string, which includes the claimed percentage, the actual grid-implied carbon, and the claimed carbon.

The greenwashing check does not apply to `grid_average`, `marginal`, `ppa_proxy`, or `ppa_direct` — those methods do not involve certificate-based accounting.

## Findings exported to GRADE

| Metric | Unit | Description |
|---|---|---|
| `flux_methodology_score` | score_0_to_1 | Carbon accounting quality score — GRADE input |
| `carbon_accounting_grade` | grade_points_0_to_4 | A=4, B=3, C=2, D=1, F=0 |
| `actual_carbon_kg` | kg_CO2 | `total_energy_mwh × egrid_intensity` |
| `claimed_carbon_kg` | kg_CO2 | Organization self-reported footprint |
| `carbon_delta_kg` | kg_CO2 | `actual_carbon_kg − claimed_carbon_kg` |
| `greenwashing_flag` | boolean_as_float | 1.0 if flagged, 0.0 if not |
| `egrid_intensity_kg_mwh` | kg_CO2_per_MWh | Grid intensity used for estimate |
| `carbon_method_code` | method_code_0_to_6 | Integer code for ATLAS recommendation routing |

## What FLUX rewards

**Traceability.** Can the organization document that the renewable power it claims corresponds to actual generation delivered at the time its cluster was running? A direct PPA with a generator in the same grid region is traceable. Unbundled RECs purchased from another region after the fact are not — they are a financial instrument, not a physical connection to renewable power.

The methodology quality score rewards progressively better traceability: from no accounting (0.0) through grid averages (0.5) to time-matched marginal rates (0.7) to direct PPAs (1.0).

## Input schema

| Field | Type | Required | Description |
|---|---|---|---|
| `organization` | string | yes | Organization name |
| `period` | string | yes | Reporting year (YYYY) |
| `location_state` | string | yes | 2-letter US state abbreviation, or `""` for international |
| `total_energy_mwh` | float | yes | Gross facility energy consumption |
| `carbon_method` | string | yes | One of the seven method enum values above |
| `claimed_renewable_pct` | float | yes | Claimed renewable percentage (0–100) |
| `claimed_carbon_kg` | float | yes | Organization self-reported carbon footprint |
| `egrid_subregion` | string | no | Override state lookup — use for international facilities |
| `ppa_documentation` | bool | no | PPA contract documentation provided |
| `rec_vintage_matched` | bool | no | RECs matched to the same year as consumption |
| `utility_provider` | string | no | Utility provider name (for display) |

## CLI usage

```bash
# Score a single facility from a flux_input_v1.json file
flux analyze \
  --input flux_input.json \
  --output flux_output.json

# Run all five synthetic organizations and print summary table
flux demo

# Validate a ptl_output_v1.json file against the PTL schema
flux validate --input flux_output.json
```

**Example `flux_input.json`:**

```json
{
  "organization": "Midwest Research Computing",
  "period": "2026",
  "location_state": "MN",
  "total_energy_mwh": 18500,
  "carbon_method": "ppa_direct",
  "claimed_renewable_pct": 100,
  "claimed_carbon_kg": 0,
  "ppa_documentation": true
}
```

**International facility:**

```json
{
  "organization": "European AI Institute",
  "period": "2026",
  "location_state": "",
  "egrid_subregion": "FR",
  "total_energy_mwh": 12000,
  "carbon_method": "grid_average",
  "claimed_renewable_pct": 0,
  "claimed_carbon_kg": 696000
}
```

## Source

- [View FLUX source on GitHub](https://github.com/plain-theory-labs/ptl-engines/tree/main/flux)
- [FLUX methodology document](https://github.com/plain-theory-labs/ptl-methodology/blob/main/engines/flux_methodology.md)
- [Report an issue](https://github.com/plain-theory-labs/ptl-engines/issues)

#!/usr/bin/env python3
"""
PTL certification badge generator.
Generates SVG badge files for each certification tier.
Output: ptl-website/public/badges/
"""

import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

TIERS = [
    {"name": "PLATINUM", "color": "#b8860b"},
    {"name": "GOLD",     "color": "#c9a84c"},
    {"name": "SILVER",   "color": "#708090"},
    {"name": "BRONZE",   "color": "#8b5e3c"},
    {"name": "MEASURED", "color": "#5a5248"},
    {"name": "PENDING",  "color": "#8a8078"},
]


def make_badge(tier_name: str, color: str, org: str = "", year: str = "") -> str:
    """
    Generate an SVG badge for the given tier.
    If org and year are provided, they appear in the year slot.
    """
    display_year = year if year else "—"
    slug = tier_name.lower()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="80" role="img"
     aria-label="PTL {tier_name} Certified{' ' + year if year else ''}">
  <title>PTL {tier_name} Certified{' ' + year if year else ''}</title>
  <rect width="200" height="80" rx="6" ry="6"
        fill="#ffffff" stroke="{color}" stroke-width="1.5"/>
  <!-- Top label: PTL CERTIFIED -->
  <text x="100" y="20"
        font-family="'IBM Plex Mono', monospace"
        font-size="9" font-weight="400"
        fill="{color}" fill-opacity="0.7"
        text-anchor="middle" letter-spacing="2">PTL CERTIFIED</text>
  <!-- Tier name -->
  <text x="100" y="42"
        font-family="'IBM Plex Mono', monospace"
        font-size="18" font-weight="700"
        fill="{color}"
        text-anchor="middle" letter-spacing="1">{tier_name}</text>
  <!-- Year / org-year -->
  <text x="100" y="57"
        font-family="'IBM Plex Mono', monospace"
        font-size="10" font-weight="400"
        fill="#666666"
        text-anchor="middle">{display_year}</text>
  <!-- Divider -->
  <line x1="20" y1="63" x2="180" y2="63"
        stroke="{color}" stroke-opacity="0.2" stroke-width="1"/>
  <!-- URL -->
  <text x="100" y="74"
        font-family="'IBM Plex Mono', monospace"
        font-size="8" font-weight="400"
        fill="#999999"
        text-anchor="middle">plaintheory.org</text>
</svg>"""
    return svg


def main():
    generated = []

    # Six tier badges
    for tier in TIERS:
        name = tier["name"]
        color = tier["color"]
        filename = f"ptl-certified-{name.lower()}.svg"
        path = OUTPUT_DIR / filename
        svg = make_badge(name, color)
        path.write_text(svg, encoding="utf-8")
        generated.append(filename)
        print(f"  {filename}")

    # MIT Supercloud sample — MEASURED tier, 2022
    sample_tier = next(t for t in TIERS if t["name"] == "MEASURED")
    sample_svg = make_badge(
        tier_name="MEASURED",
        color=sample_tier["color"],
        org="MIT Supercloud",
        year="2022",
    )
    sample_filename = "ptl-certified-mit-supercloud-2022.svg"
    (OUTPUT_DIR / sample_filename).write_text(sample_svg, encoding="utf-8")
    generated.append(sample_filename)
    print(f"  {sample_filename}")

    print(f"\nGenerated {len(generated)} badges in {OUTPUT_DIR}")

    # Print BRONZE badge source for verification
    bronze_path = OUTPUT_DIR / "ptl-certified-bronze.svg"
    print("\n--- BRONZE badge SVG source ---")
    print(bronze_path.read_text(encoding="utf-8"))
    print("--- end ---")


if __name__ == "__main__":
    main()

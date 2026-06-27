from src.county_lookup import normalize_county_name
from src.disclaimers import BLT_URL


def build_comprehensive_report(
    lat: float | None,
    lon: float | None,
    county: str | None,
    crop_or_site: str,
    pula_summary: dict | None,
    pula_intersects: bool | None,
    hsg: str,
    resistance_summaries: list[str],
) -> str:
    location = f"{lat:.6f}, {lon:.6f}" if lat is not None and lon is not None else "Not selected"
    county_line = f"{normalize_county_name(county)} County" if county else "Not determined"

    crop_info = crop_or_site if crop_or_site else "Not entered"
    crop_implications = ""
    if crop_or_site:
        crop_implications = f"\n**Agronomist Note:** Selecting '{crop_or_site}' means you should focus on herbicide site-of-action rotation specific to this system. Ensure you are integrating multiple effective sites of action and adhering to state-specific 24(c) SLN labels for {crop_or_site}."

    lines = [
        "# Comprehensive Site Context Report",
        "",
        "This report is for planning and educational support only. **The label is the law.** It does not replace the pesticide label, EPA Bulletins Live! Two, state or local restrictions (including 24(c) SLN labels), or Extension guidance.",
        "",
        "## 1. Field Context",
        f"- **Location Checked:** {location}",
        f"- **County:** {county_line}",
        f"- **Crop or Managed Site:** {crop_info}{crop_implications}",
        f"- **Hydrologic Soil Group (HSG):** {hsg}",
        "",
        "**Agronomist Note:** The HSG (Hydrologic Soil Group) determines the runoff vulnerability of your field. For example, HSG C and D soils have higher runoff potential, requiring more mitigation points for products like Enlist.",
        "",
        "## 2. PULA Awareness (EPA BLT Context)",
    ]

    if pula_summary:
        lines.extend([
            f"- **Selected point inside cached PULA:** {'Yes' if pula_intersects else 'No'}",
            f"- **Nearest Cached PULA Distance:** {pula_summary.get('distance_miles', 'N/A'):.2f} miles",
            f"- **Nearest PULA ID:** {pula_summary.get('pula_id', 'Unknown')}",
            f"- **Event (Why it exists):** {pula_summary.get('event_name', 'Unknown')}",
            f"- **PULA Codes:** {pula_summary.get('codes', 'Unknown')}",
            f"- **Status:** {pula_summary.get('status', 'Unknown')}",
            f"- **Effective Date:** {pula_summary.get('effective_date', 'Unknown')}",
            "",
            "**Regulatory Specialist Note:** A PULA (Pesticide Use Limitation Area) polygon indicates where the EPA has identified potential risk to listed endangered species or critical habitats. You **MUST** check EPA Bulletins Live! Two (BLT) for your specific application month, as these polygons can change and this tool is only a snapshot.",
            f"**Verify here:** [EPA Bulletins Live! Two]({BLT_URL})"
        ])
    else:
        lines.extend([
            "- No cached PULA polygons were found near this location in the current snapshot.",
            "",
            "**Regulatory Specialist Note:** Even if no PULA appears here, you **MUST** verify your intended application on EPA Bulletins Live! Two (BLT) for the specific application month to remain compliant.",
            f"**Verify here:** [EPA Bulletins Live! Two]({BLT_URL})"
        ])

    lines.extend([
        "",
        "## 3. Nearby Herbicide Resistance Context",
        "The following are state-level reports of herbicide resistance from weedscience.org for the chosen crop system. *Note: This is not a confirmation of resistance in your specific field.*",
    ])

    if resistance_summaries:
        for summary in resistance_summaries:
            lines.append(f"- {summary}")
        lines.extend([
            "",
            "**Agronomist Note:** If you suspect resistance (e.g., patchy survival after an application made at the correct rate and timing), do not simply respray the same site of action. Contact your local Extension office for a site visit."
        ])
    else:
        lines.append("- No specific state-level resistance records found for this crop in the database snapshot.")

    lines.extend([
        "",
        "## 4. Invasive Weeds (EDDMapS Context)",
        "**Extension Specialist Note:** Always scout your fields. While we cannot provide a live list of invasive species coordinates here, you should use the EDDMapS distribution maps to understand what invasive threats (like Cogongrass or Palmer Amaranth) are moving into your county.",
        "",
        "## 5. Required Follow-Up",
        "- **Verify** the exact product, application month, and location in EPA Bulletins Live! Two.",
        "- **Read** the current pesticide label and any supplemental labeling (e.g., 24(c)).",
        "- **Contact** the appropriate ACES county office or Auburn/ACES Extension specialist for local interpretation."
    ])

    return "\n".join(lines)

from src.county_lookup import normalize_county_name


COUNTY_RUNOFF_VULNERABILITY = {
    "Autauga": "M", "Baldwin": "H", "Barbour": "M", "Bibb": "M",
    "Blount": "H", "Bullock": "H", "Butler": "H", "Calhoun": "M",
    "Chambers": "M", "Cherokee": "M", "Chilton": "M", "Choctaw": "H",
    "Clarke": "M", "Clay": "M", "Cleburne": "H", "Coffee": "M",
    "Colbert": "M", "Conecuh": "H", "Coosa": "M", "Covington": "M",
    "Crenshaw": "M", "Cullman": "M", "Dale": "M", "Dallas": "H",
    "DeKalb": "H", "Elmore": "M", "Escambia": "H", "Etowah": "M",
    "Fayette": "M", "Franklin": "M", "Geneva": "H", "Greene": "M",
    "Hale": "M", "Henry": "M", "Houston": "M", "Jackson": "H",
    "Jefferson": "M", "Lamar": "M", "Lauderdale": "M", "Lawrence": "H",
    "Lee": "M", "Limestone": "H", "Lowndes": "H", "Macon": "H",
    "Madison": "H", "Marengo": "H", "Marion": "M", "Marshall": "H",
    "Mobile": "H", "Monroe": "H", "Montgomery": "H", "Morgan": "H",
    "Perry": "H", "Pickens": "H", "Pike": "M", "Randolph": "M",
    "Russell": "M", "Shelby": "M", "St. Clair": "H", "Sumter": "H",
    "Talladega": "M", "Tallapoosa": "M", "Tuscaloosa": "M",
    "Walker": "H", "Washington": "H", "Wilcox": "H", "Winston": "M",
}

ACTIVE_ESA_PRODUCTS = [
    {
        "name": "Liberty ULTRA",
        "active_ingredient": "Glufosinate-P-ammonium",
        "group": "10",
        "epa_reg": "7969-500",
        "runoff_points": 3,
        "downwind_buffer_ft": 10,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Active Herbicide Strategy label; verify BLT and label before use.",
    },
    {
        "name": "Enlist One",
        "active_ingredient": "2,4-D choline salt",
        "group": "4",
        "epa_reg": "62719-695",
        "runoff_points": "4 on HSG A/B, 6 on HSG C/D",
        "downwind_buffer_ft": 30,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Enlist trait and label restrictions apply; BLT check is required.",
    },
    {
        "name": "Enlist Duo",
        "active_ingredient": "2,4-D choline salt + glyphosate",
        "group": "4+9",
        "epa_reg": "62719-649",
        "runoff_points": "4 on HSG A/B, 6 on HSG C/D",
        "downwind_buffer_ft": 30,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Enlist trait and label restrictions apply; BLT check is required.",
    },
]


def county_mitigation_context(county_name: str) -> dict | None:
    county = normalize_county_name(county_name)
    value = COUNTY_RUNOFF_VULNERABILITY.get(county)
    if not value:
        return None
    return {
        "county": county,
        "runoff_vulnerability": "High" if value == "H" else "Medium",
        "county_relief_points": 0 if value == "H" else 2,
    }


def active_esa_products_for_crop(crop_or_site: str) -> list[dict]:
    query = str(crop_or_site).strip().lower()
    if not query:
        return []
    matches = []
    for product in ACTIVE_ESA_PRODUCTS:
        tags = product["crop_tags"]
        if query in tags or any(query in tag or tag in query for tag in tags):
            matches.append(product)
    return matches


def enlist_runoff_points_for_hsg(hsg: str) -> int | None:
    value = str(hsg).strip().upper()
    if value in {"A", "B", "A/D", "B/D"}:
        return 4
    if value in {"C", "D", "C/D"}:
        return 6
    return None


def build_mitigation_report(
    lat: float | None,
    lon: float | None,
    county: str | None,
    crop_or_site: str,
) -> str:
    county_context = county_mitigation_context(county or "") if county else None
    products = active_esa_products_for_crop(crop_or_site)
    location = (
        f"{lat:.6f}, {lon:.6f}" if lat is not None and lon is not None else "Not selected"
    )
    county_line = (
        f"{county_context['county']} County"
        if county_context
        else (f"{normalize_county_name(county)} County" if county else "Not determined")
    )
    lines = [
        "# ESA Mitigation Planning Report",
        "",
        "This report is for planning and recordkeeping support only. It does not replace the pesticide label, EPA Bulletins Live! Two, EPA PALM, state or local restrictions, or Extension guidance.",
        "",
        "## Field Context",
        f"- Location checked: {location}",
        f"- County: {county_line}",
        f"- Crop or managed site: {crop_or_site or 'Not entered'}",
    ]
    if county_context:
        lines.extend(
            [
                f"- County runoff vulnerability: {county_context['runoff_vulnerability']}",
                f"- County relief points shown by calculator data: {county_context['county_relief_points']}",
            ]
        )
    else:
        lines.append("- County runoff vulnerability: not available until a county is determined")

    lines.extend(["", "## Active ESA-Labeled Product Examples"])
    if products:
        for product in products:
            lines.append(
                "- "
                f"{product['name']} | AI: {product['active_ingredient']} | "
                f"Group {product['group']} | EPA Reg. {product['epa_reg']} | "
                f"Runoff points: {product['runoff_points']} | "
                f"Downwind buffer: {product['downwind_buffer_ft']} ft"
            )
    else:
        lines.append("- No product example matched the entered crop/site in this integrated calculator snapshot.")

    lines.extend(
        [
            "",
            "## Recordkeeping Note",
            "The source Alabama ESA calculator treated filing a mitigation report with spray records as recordkeeping documentation for the EPA mitigation menu recordkeeping practice. Confirm current EPA PALM/menu language and the specific product label before relying on any mitigation point.",
            "",
            "## Required Follow-Up",
            "- Verify the exact product, application month, and location in EPA Bulletins Live! Two.",
            "- Verify the current pesticide label and any supplemental labeling.",
            "- Contact the appropriate ACES county office or Auburn/ACES Extension specialist for local interpretation.",
        ]
    )
    return "\n".join(lines)

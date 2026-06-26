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

MITIGATION_PRACTICES = [
    {
        "id": "recordkeeping",
        "name": "Recordkeeping of mitigation practices",
        "points": 1,
        "category": "Documentation",
    },
    {
        "id": "no-till",
        "name": "No-till or strip-till field management",
        "points": 2,
        "category": "Erosion/runoff",
    },
    {
        "id": "cover-crop",
        "name": "Cover crop or living cover",
        "points": 1,
        "category": "Erosion/runoff",
    },
    {
        "id": "vegetated-filter-strip",
        "name": "Vegetated filter strip",
        "points": 1,
        "category": "Edge-of-field",
    },
    {
        "id": "terrace-contour",
        "name": "Terraces, contour farming, or contour buffer strips",
        "points": 2,
        "category": "Erosion/runoff",
    },
    {
        "id": "grassed-waterway",
        "name": "Grassed waterway",
        "points": 1,
        "category": "Edge-of-field",
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


def product_by_name(product_name: str) -> dict | None:
    for product in ACTIVE_ESA_PRODUCTS:
        if product["name"] == product_name:
            return product
    return None


def enlist_runoff_points_for_hsg(hsg: str) -> int | None:
    value = str(hsg).strip().upper()
    if value in {"A", "B", "A/D", "B/D"}:
        return 4
    if value in {"C", "D", "C/D"}:
        return 6
    return None


def required_runoff_points(product: dict | None, hsg: str) -> int | None:
    if not product:
        return None
    if product["name"].startswith("Enlist"):
        return enlist_runoff_points_for_hsg(hsg)
    points = product.get("runoff_points")
    return points if isinstance(points, int) else None


def selected_practices(selected_practice_ids: list[str]) -> list[dict]:
    selected = set(selected_practice_ids)
    return [
        practice
        for practice in MITIGATION_PRACTICES
        if practice["id"] in selected and practice["id"] != "recordkeeping"
    ]


def calculate_mitigation_summary(
    county: str | None,
    product_name: str,
    hsg: str,
    selected_practice_ids: list[str],
    recordkeeping: bool,
) -> dict:
    product = product_by_name(product_name)
    county_context = county_mitigation_context(county or "") if county else None
    required = required_runoff_points(product, hsg)
    practices = selected_practices(selected_practice_ids)
    county_points = county_context["county_relief_points"] if county_context else 0
    practice_points = sum(int(practice["points"]) for practice in practices)
    recordkeeping_points = 1 if recordkeeping else 0
    total = county_points + practice_points + recordkeeping_points
    needs_hsg = bool(product and product["name"].startswith("Enlist") and required is None)
    return {
        "product": product,
        "county_context": county_context,
        "required_points": required,
        "county_relief_points": county_points,
        "selected_practices": practices,
        "practice_points": practice_points,
        "recordkeeping_points": recordkeeping_points,
        "total_points": total,
        "needs_hsg": needs_hsg,
        "meets_points": required is not None and total >= required,
    }


def build_mitigation_report(
    lat: float | None,
    lon: float | None,
    county: str | None,
    crop_or_site: str,
    product_name: str | None = None,
    hsg: str = "Unknown",
    selected_practice_ids: list[str] | None = None,
    recordkeeping: bool = False,
    pula_intersects: bool | None = None,
    nearest_pula: dict | None = None,
) -> str:
    county_context = county_mitigation_context(county or "") if county else None
    products = active_esa_products_for_crop(crop_or_site)
    selected_practice_ids = selected_practice_ids or []
    summary = (
        calculate_mitigation_summary(
            county=county,
            product_name=product_name,
            hsg=hsg,
            selected_practice_ids=selected_practice_ids,
            recordkeeping=recordkeeping,
        )
        if product_name
        else None
    )
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
    if pula_intersects is not None:
        lines.append(
            f"- Cached PULA status: {'Selected point appears inside a cached PULA polygon' if pula_intersects else 'No cached PULA polygon intersection found in this snapshot'}"
        )
    if nearest_pula:
        lines.extend(
            [
                f"- Nearest cached PULA ID: {nearest_pula.get('pula_id', 'unknown')}",
                f"- Nearest cached PULA distance: {nearest_pula.get('distance_miles', 0):.2f} miles",
                f"- Nearest PULA event/reason: {nearest_pula.get('event_name', 'unknown')}",
                f"- Nearest PULA codes: {nearest_pula.get('codes', 'unknown')}",
            ]
        )
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

    if summary:
        lines.extend(
            [
                "",
                "## Mitigation Point Calculation",
                f"- Selected product: {product_name}",
                f"- Hydrologic soil group: {hsg}",
                f"- Required runoff points: {summary['required_points'] if summary['required_points'] is not None else 'Needs HSG/product verification'}",
                f"- County relief points: {summary['county_relief_points']}",
                f"- Selected practice points: {summary['practice_points']}",
                f"- Recordkeeping points: {summary['recordkeeping_points']}",
                f"- Total planning points: {summary['total_points']}",
                f"- Planning status: {'Meets entered point target' if summary['meets_points'] else 'Needs review or more mitigation'}",
            ]
        )
        if summary["selected_practices"]:
            lines.append("- Selected practices:")
            for practice in summary["selected_practices"]:
                lines.append(f"  - [ ] {practice['name']} ({practice['points']} point(s))")
        lines.append(
            "- Note: mitigation point tracking here applies to the selected ESA-labeled product context. Other herbicides may have different or no current Herbicide Strategy mitigation requirements; always verify the specific label and BLT."
        )

    lines.extend(
        [
            "",
            "## Recordkeeping Note",
            "If recordkeeping is selected, print or save this worksheet with spray records and check the practices actually adopted. Confirm current EPA PALM/menu language and the specific product label before relying on any mitigation point.",
            "",
            "## Required Follow-Up",
            "- Verify the exact product, application month, and location in EPA Bulletins Live! Two.",
            "- Verify the current pesticide label and any supplemental labeling.",
            "- Contact the appropriate ACES county office or Auburn/ACES Extension specialist for local interpretation.",
        ]
    )
    return "\n".join(lines)

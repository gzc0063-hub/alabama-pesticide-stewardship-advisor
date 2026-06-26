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

LABEL_COVERAGE_NOTE = (
    "ESA label snapshot follows the source Alabama ESA calculator: Liberty ULTRA, "
    "Enlist One, and Enlist Duo are treated as active point-calculation products. "
    "Other listed products are planning/verification entries until their current "
    "label or BLT bulletin specifies a runoff point target."
)

HERBICIDE_PRODUCTS = [
    {
        "id": "liberty-ultra",
        "name": "Liberty ULTRA",
        "active_ingredient": "Glufosinate-P-ammonium",
        "group": "10",
        "epa_reg": "7969-500",
        "esa_status": "active",
        "runoff_points": 3,
        "downwind_buffer_ft": 10,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Active Herbicide Strategy label; verify BLT and label before use. Buffer may be reducible only when the label/menu conditions are met.",
    },
    {
        "id": "enlist-one",
        "name": "Enlist One",
        "active_ingredient": "2,4-D choline salt",
        "group": "4",
        "epa_reg": "62719-695",
        "esa_status": "active",
        "runoff_points": "4 on HSG A/B, 6 on HSG C/D",
        "downwind_buffer_ft": 30,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Enlist trait and label restrictions apply; BLT check is required.",
    },
    {
        "id": "enlist-duo",
        "name": "Enlist Duo",
        "active_ingredient": "2,4-D choline salt + glyphosate",
        "group": "4+9",
        "epa_reg": "62719-649",
        "esa_status": "active",
        "runoff_points": "4 on HSG A/B, 6 on HSG C/D",
        "downwind_buffer_ft": 30,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Enlist trait and label restrictions apply; BLT check is required.",
    },
    {
        "id": "roundup-powermax-3",
        "name": "Roundup PowerMAX 3",
        "active_ingredient": "Glyphosate",
        "group": "9",
        "epa_reg": "524-659",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "corn", "row crop", "pasture", "right-of-way"],
        "note": "Included so growers do not miss common glyphosate products. This snapshot does not assign a Herbicide Strategy point target; verify the current product label, BLT bulletin, and EPA PALM.",
    },
    {
        "id": "dual-ii-magnum",
        "name": "Dual II Magnum",
        "active_ingredient": "S-metolachlor",
        "group": "15",
        "epa_reg": "100-816",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "corn", "peanut", "row crop"],
        "note": "Common residual herbicide in the source calculator's pending/verification list. Use current label and BLT/PALM before application.",
    },
    {
        "id": "warrant",
        "name": "Warrant",
        "active_ingredient": "Acetochlor",
        "group": "15",
        "epa_reg": "524-591",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "corn", "row crop"],
        "note": "Source calculator carried this as awaiting product-specific ESA label review. Verify current label, BLT, and PALM.",
    },
    {
        "id": "zidua-sc",
        "name": "Zidua SC",
        "active_ingredient": "Pyroxasulfone",
        "group": "15",
        "epa_reg": "7969-374",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "corn", "peanut", "row crop"],
        "note": "Planning/verification entry only in this snapshot; confirm the current label and BLT/PALM.",
    },
    {
        "id": "valor-sx",
        "name": "Valor SX",
        "active_ingredient": "Flumioxazin",
        "group": "14",
        "epa_reg": "59639-99",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "peanut", "row crop"],
        "note": "Planning/verification entry from the source calculator. Do not infer a point target without the current label or BLT.",
    },
    {
        "id": "reflex",
        "name": "Reflex",
        "active_ingredient": "Fomesafen",
        "group": "14",
        "epa_reg": "100-1071",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "row crop"],
        "note": "Planning/verification entry only; check current label, BLT, crop restrictions, and rotational restrictions.",
    },
    {
        "id": "gramoxone-sl-3",
        "name": "Gramoxone SL 3.0",
        "active_ingredient": "Paraquat dichloride",
        "group": "22",
        "epa_reg": "100-1652",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "corn", "peanut", "row crop", "right-of-way"],
        "note": "Restricted-use product and verification entry. Follow current label, paraquat certification requirements, BLT, and PALM.",
    },
    {
        "id": "select-max",
        "name": "Select Max",
        "active_ingredient": "Clethodim",
        "group": "1",
        "epa_reg": "59639-135",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "peanut", "row crop"],
        "note": "Grass herbicide included as a verification entry; this snapshot does not calculate ESA points for it.",
    },
    {
        "id": "aatrex-4l",
        "name": "AAtrex 4L",
        "active_ingredient": "Atrazine",
        "group": "5",
        "epa_reg": "100-497",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["corn", "row crop"],
        "note": "Corn product carried by the source calculator as a high-priority verification entry. Check current atrazine label, BLT, and PALM.",
    },
    {
        "id": "other",
        "name": "Other / not listed product",
        "active_ingredient": "Enter exact product on label",
        "group": "Unknown",
        "epa_reg": "Unknown",
        "esa_status": "verify label/BLT",
        "runoff_points": None,
        "downwind_buffer_ft": None,
        "crop_tags": ["cotton", "soybean", "corn", "peanut", "pasture", "forage", "turf", "right-of-way", "aquatic site", "forestry", "row crop", "other"],
        "note": "Use this when the product is not listed. The correct decision path is product-specific label, BLT, EPA PALM, and Extension review.",
    },
]

ACTIVE_ESA_PRODUCTS = [
    product for product in HERBICIDE_PRODUCTS if product["esa_status"] == "active"
]

MITIGATION_PRACTICES = [
    {
        "id": "recordkeeping",
        "name": "Recordkeeping of mitigation practices",
        "points": 1,
        "category": "Mitigation relief and field characteristics",
        "description": "Maintain paper/electronic records of selected mitigation practices, BLT bulletins, and this report with spray records.",
    },
    {
        "id": "non-irrigated",
        "name": "Non-irrigated/dryland production",
        "points": 3,
        "category": "Mitigation relief and field characteristics",
        "description": "Field is not irrigated.",
    },
    {
        "id": "sandy-hsg-a",
        "name": "Sandy soil or HSG A field",
        "points": 3,
        "category": "Mitigation relief and field characteristics",
        "description": "Hydrologic Soil Group A or qualifying sandy soil condition; verify with USDA soil data or field records.",
    },
    {
        "id": "slope-under-3",
        "name": "Average field slope 3% or less",
        "points": 2,
        "category": "Mitigation relief and field characteristics",
        "description": "Average field slope is 3% or less.",
    },
    {
        "id": "eqip-cps-595",
        "name": "Active NRCS/EQIP pest-management plan",
        "points": 9,
        "category": "Mitigation relief and field characteristics",
        "description": "Qualifying NRCS conservation program or CPS 595 pest-management plan; confirm documentation.",
    },
    {
        "id": "no-till",
        "name": "No-till or strip-till field management",
        "points": 3,
        "category": "In-field conservation",
        "description": "No-till or strip-till with qualifying residue at planting.",
    },
    {
        "id": "reduced-till",
        "name": "Reduced or mulch tillage",
        "points": 2,
        "category": "In-field conservation",
        "description": "Reduced tillage/mulch tillage condition from the source calculator.",
    },
    {
        "id": "cover-crop",
        "name": "Annual cover crop",
        "points": 1,
        "category": "In-field conservation",
        "description": "Cover crop present at or after application as described by the mitigation menu.",
    },
    {
        "id": "cover-crop-no-till",
        "name": "Cover crop plus no-till for 3+ years",
        "points": 3,
        "category": "In-field conservation",
        "description": "Continuous cover crop plus no-till system for at least three consecutive years.",
    },
    {
        "id": "reservoir-tillage",
        "name": "Reservoir tillage or furrow diking",
        "points": 3,
        "category": "In-field conservation",
        "description": "Small dams/furrow diking or reservoir tillage that captures rainfall/runoff.",
    },
    {
        "id": "terrace-contour",
        "name": "Terraces, contour farming, or cross-slope tillage",
        "points": 2,
        "category": "In-field conservation",
        "description": "Rows, contour farming, terraces, or diversions that reduce runoff velocity or slope length.",
    },
    {
        "id": "grassed-waterway",
        "name": "Grassed waterway",
        "points": 1,
        "category": "In-field conservation",
        "description": "Grass-covered waterway in a natural drainage area.",
    },
    {
        "id": "filter-strip-10",
        "name": "Vegetative filter strip, 10-29 ft",
        "points": 1,
        "category": "Edge-of-field",
        "description": "Permanent vegetation at field edge, 10-29 feet wide.",
    },
    {
        "id": "filter-strip-30",
        "name": "Vegetative filter strip, 30-59 ft",
        "points": 2,
        "category": "Edge-of-field",
        "description": "Permanent vegetation at field edge, 30-59 feet wide.",
    },
    {
        "id": "filter-strip-60",
        "name": "Vegetative filter strip, 60+ ft",
        "points": 3,
        "category": "Edge-of-field",
        "description": "Permanent vegetation at field edge, 60 feet or wider.",
    },
    {
        "id": "field-border",
        "name": "Field border, 30+ ft",
        "points": 1,
        "category": "Edge-of-field",
        "description": "Perennial vegetation around the field perimeter.",
    },
    {
        "id": "riparian-herbaceous",
        "name": "Riparian herbaceous buffer, 30+ ft",
        "points": 2,
        "category": "Edge-of-field",
        "description": "Permanent grass/forb buffer adjacent to waterbody.",
    },
    {
        "id": "riparian-forest",
        "name": "Riparian forest buffer, 35+ ft",
        "points": 2,
        "category": "Edge-of-field",
        "description": "Trees/shrubs plus grass buffer adjacent to waterbody.",
    },
    {
        "id": "constructed-wetland",
        "name": "Constructed wetland",
        "points": 2,
        "category": "Edge-of-field",
        "description": "Engineered wetland treating field runoff.",
    },
    {
        "id": "vegetated-ditch",
        "name": "Vegetated ditch",
        "points": 1,
        "category": "Edge-of-field",
        "description": "Drainage ditch with established vegetation.",
    },
    {
        "id": "sediment-basin",
        "name": "Sediment basin or retention pond",
        "points": 1,
        "category": "Edge-of-field",
        "description": "Basin or pond capturing runoff before release.",
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
    return herbicide_products_for_crop(crop_or_site, include_verification=False)


def herbicide_products_for_crop(
    crop_or_site: str, include_verification: bool = True
) -> list[dict]:
    query = str(crop_or_site).strip().lower()
    if not query:
        return []
    matches = []
    for product in HERBICIDE_PRODUCTS:
        if not include_verification and product["esa_status"] != "active":
            continue
        tags = product["crop_tags"]
        if query in tags or any(query in tag or tag in query for tag in tags):
            matches.append(product)
    return matches


def product_by_name(product_name: str) -> dict | None:
    for product in HERBICIDE_PRODUCTS:
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
    if product.get("esa_status") != "active":
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
    needs_label_verification = bool(product and product.get("esa_status") != "active")
    return {
        "product": product,
        "esa_status": product.get("esa_status") if product else None,
        "county_context": county_context,
        "required_points": required,
        "county_relief_points": county_points,
        "selected_practices": practices,
        "practice_points": practice_points,
        "recordkeeping_points": recordkeeping_points,
        "total_points": total,
        "needs_hsg": needs_hsg,
        "needs_label_verification": needs_label_verification,
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
    products = herbicide_products_for_crop(crop_or_site)
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

    lines.extend(["", "## Product Decision Context"])
    lines.append(f"- Label snapshot: {LABEL_COVERAGE_NOTE}")
    if products:
        for product in products:
            lines.append(
                "- "
                f"{product['name']} | AI: {product['active_ingredient']} | "
                f"Group {product['group']} | EPA Reg. {product['epa_reg']} | "
                f"Status: {product['esa_status']} | "
                f"Runoff points: {product['runoff_points'] or 'verify label/BLT'} | "
                f"Downwind buffer: {str(product['downwind_buffer_ft']) + ' ft' if product['downwind_buffer_ft'] else 'verify label/BLT'}"
            )
    else:
        lines.append("- No product example matched the entered crop/site in this integrated calculator snapshot.")

    if summary:
        lines.extend(
            [
                "",
                "## Mitigation Point Calculation",
                f"- Selected product: {product_name}",
                f"- ESA calculation status: {summary['esa_status'] or 'unknown'}",
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
        if summary.get("needs_label_verification"):
            lines.append(
                "- Important: this selected product does not have a verified active point target in this app snapshot. Use the exact product label, EPA BLT, and EPA PALM before deciding whether points, buffers, or other restrictions apply."
            )
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

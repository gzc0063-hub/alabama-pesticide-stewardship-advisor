# PULA Awareness Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Alabama-first PULA Awareness Tool foundation with compliance-safe wording, Heap-attributed resistance context, Extension contact routing, and suspected-resistance report capture through private CSV plus optional email.

**Architecture:** Streamlit is the entry point, with focused modules under `src/` for disclaimers, spatial utilities, EPA/Heap data loading, Extension contacts, and report handling. Public source data and metadata live under `data/`, while private report outputs and uploads live under `data/private/` and are excluded from git.

**Tech Stack:** Python, Streamlit, Folium/streamlit-folium, GeoPandas, Shapely, PyProj, Pandas, Requests, BeautifulSoup4, Pytest.

---

## File Structure

- Create `README.md`: public overview, legal boundary, data sources, and development instructions.
- Create `PROJECT_PLAN.md`: cleaned version of the user's original project plan with updated product name and decisions.
- Create `requirements.txt`: pinned or bounded dependencies for the MVP.
- Create `.gitignore`: exclude Python artifacts, Streamlit secrets, private reports, and uploads.
- Create `.streamlit/config.toml`: Auburn-inspired but restrained theme.
- Create `app.py`: Streamlit UI shell, map area, panels, and report form.
- Create `src/__init__.py`: package marker.
- Create `src/disclaimers.py`: centralized disclaimer text, official links, and source attribution snippets.
- Create `src/reports.py`: suspected-resistance report schema, CSV append, routing selection, and optional email notification.
- Create `src/extension_contacts.py`: load/filter Extension contact records from CSV.
- Create `src/spatial.py`: point and distance utilities using EPSG:4326 input and EPSG:5070 distance calculations.
- Create `src/data_epa.py`: PULA snapshot loading and validation helpers.
- Create `src/data_heap.py`: resistance snapshot loading, Alabama filtering, and attribution helper.
- Create `data/snapshot_metadata.json`: dated placeholder metadata for initial local snapshots.
- Create `data/extension_contacts_alabama.csv`: verified-contact schema with seed rows or placeholders marked for verification.
- Create `docs/data_sources.md`: source documentation, attribution, and endpoint verification notes.
- Create `docs/methods.md`: plain-language methods and limitations.
- Create `tests/test_disclaimers.py`: wording guardrails.
- Create `tests/test_reports.py`: report schema, CSV append, and email-missing behavior.
- Create `tests/test_spatial.py`: projection and geometry behavior.

---

## Task 1: Repository Foundation And Public Documentation

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `.streamlit/config.toml`
- Create: `README.md`
- Create: `PROJECT_PLAN.md`
- Create: `docs/data_sources.md`
- Create: `docs/methods.md`

- [ ] **Step 1: Create ignore rules for private and generated files**

Write `.gitignore` with:

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
.env
.streamlit/secrets.toml
data/private/
data/**/*.tmp
docs/screenshots/*.png
```

- [ ] **Step 2: Add MVP dependencies**

Write `requirements.txt` with:

```text
streamlit>=1.36,<2
streamlit-folium>=0.20,<1
folium>=0.17,<1
pandas>=2.2,<3
geopandas>=1.0,<2
shapely>=2.0,<3
pyproj>=3.6,<4
requests>=2.32,<3
beautifulsoup4>=4.12,<5
pytest>=8.2,<9
```

- [ ] **Step 3: Add Streamlit theme**

Write `.streamlit/config.toml` with:

```toml
[theme]
primaryColor = "#DD550C"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F4F6F8"
textColor = "#0C2340"
font = "sans serif"
```

- [ ] **Step 4: Write README**

Write `README.md` with sections:

```markdown
# PULA Awareness Tool

An educational planning tool that helps users view EPA Pesticide Use Limitation Area context alongside herbicide-resistance context. The first release focuses on Alabama and is designed for later U.S. expansion.

## What This Is

- An educational map and decision-support aid.
- A way to route users to EPA Bulletins Live! Two, PALM, pesticide labels, and Extension professionals.
- A way to collect suspected herbicide-resistance reports for Extension follow-up.

## What This Is Not

- Not a compliance system.
- Not a substitute for EPA Bulletins Live! Two.
- Not pesticide label advice.
- Not confirmation of herbicide resistance.
- Not a herbicide recommendation engine.

## Required Official Checks

Applicators must verify official requirements in EPA Bulletins Live! Two for the product, location, and application month, and must follow the pesticide label and any state or local restrictions.

## Data Sources

- EPA Bulletins Live! Two and EPA Pesticide Use Limitation Area data.
- EPA PALM for mitigation planning.
- Heap, I. The International Herbicide-Resistant Weed Database. www.weedscience.org.
- Alabama Cooperative Extension System contact information from official Extension pages.

## Development

```powershell
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\streamlit run app.py
```
```

- [ ] **Step 5: Clean and update project plan**

Create `PROJECT_PLAN.md` by copying the important structure from `C:\Users\gzc0063\Downloads\PROJECT_PLAN pula.md`, replacing the project name with `PULA Awareness Tool`, removing encoding artifacts, and aligning the resistance-report and Extension-contact decisions with the approved spec.

- [ ] **Step 6: Document source posture**

Write `docs/data_sources.md` with:

```markdown
# Data Sources

## EPA Bulletins Live! Two

EPA Bulletins Live! Two is the official system users must consult when pesticide labels direct them to obtain a bulletin. This app links users to BLT and does not replace it.

Endpoint and schema notes will be updated after live endpoint verification.

## EPA PALM

EPA PALM is linked as the official mitigation planning tool. This app does not recreate PALM calculations.

## PULA Polygon Snapshots

Cached PULA data must include a snapshot date and source URL. If a schema or endpoint changes, refresh scripts must fail validation instead of silently producing output.

## Herbicide Resistance

Resistance context is attributed to:

Heap, I. The International Herbicide-Resistant Weed Database. www.weedscience.org.

Displayed resistance information is reported database context, not proof that a specific field has or does not have resistance.

## Extension Contacts

Contact records must come from official Alabama Extension or Auburn pages and include a verified-as-of date.
```

- [ ] **Step 7: Document methods and limitations**

Write `docs/methods.md` with:

```markdown
# Methods And Limitations

The PULA Awareness Tool displays cached EPA PULA polygon context and state-level herbicide-resistance context. These layers have different spatial precision and must not be interpreted as a single joined compliance result.

Location checks against cached polygons are educational. Users must verify official requirements in EPA Bulletins Live! Two for the specific product, location, and application month.

Resistance records are state-level reported cases from weedscience.org. They do not prove resistance in a specific field and they do not prove that an unlisted herbicide group will work.

Suspected resistance reports submitted through the app are not confirmations. Extension review, field history, sampling, greenhouse testing, or other diagnostic steps may be needed.
```

- [ ] **Step 8: Verify documentation files exist**

Run:

```powershell
Get-ChildItem README.md,PROJECT_PLAN.md,requirements.txt,.gitignore,docs\data_sources.md,docs\methods.md
```

Expected: all six files are listed without errors.

- [ ] **Step 9: Commit foundation docs**

Run:

```powershell
git add .gitignore requirements.txt .streamlit/config.toml README.md PROJECT_PLAN.md docs/data_sources.md docs/methods.md
git commit -m "chore: add project foundation"
```

---

## Task 2: Disclaimer And Attribution Guardrails

**Files:**
- Create: `src/__init__.py`
- Create: `src/disclaimers.py`
- Create: `tests/test_disclaimers.py`

- [ ] **Step 1: Write failing disclaimer tests**

Write `tests/test_disclaimers.py` with:

```python
from src.disclaimers import (
    BLT_URL,
    PALM_URL,
    HEAP_CITATION,
    get_primary_disclaimer,
    get_result_disclaimer,
)


def test_primary_disclaimer_names_official_systems():
    text = get_primary_disclaimer()
    assert "not a compliance system" in text.lower()
    assert "Bulletins Live! Two" in text
    assert "PALM" in text
    assert "pesticide label" in text
    assert BLT_URL.startswith("https://")
    assert PALM_URL.startswith("https://")


def test_result_disclaimer_uses_cautious_language():
    text = get_result_disclaimer(cached_pula_found=False)
    assert "No cached PULA was found" in text
    assert "Verify in EPA Bulletins Live! Two" in text
    assert "No PULA applies" not in text


def test_result_disclaimer_for_possible_intersection():
    text = get_result_disclaimer(cached_pula_found=True)
    assert "may intersect" in text
    assert "Verify in EPA Bulletins Live! Two" in text
    assert "compliance" not in text.lower()


def test_heap_citation_is_present():
    assert "Heap" in HEAP_CITATION
    assert "weedscience.org" in HEAP_CITATION
```

- [ ] **Step 2: Run failing tests**

Run:

```powershell
python -m pytest tests/test_disclaimers.py -v
```

Expected: FAIL because `src.disclaimers` does not exist.

- [ ] **Step 3: Implement disclaimer module**

Write `src/__init__.py` as an empty file.

Write `src/disclaimers.py` with:

```python
BLT_URL = "https://www.epa.gov/endangered-species/bulletins-live-two-view-bulletins"
PALM_URL = "https://www.epa.gov/pesticides/mitigation-menu"
HEAP_URL = "https://www.weedscience.org/Summary/Country.aspx?CountryID=45"
HEAP_CITATION = (
    "Heap, I. The International Herbicide-Resistant Weed Database. "
    "www.weedscience.org."
)


def get_primary_disclaimer() -> str:
    return (
        "The PULA Awareness Tool is an educational planning tool, not a "
        "compliance system. It does not replace EPA Bulletins Live! Two, "
        "EPA PALM, pesticide label requirements, state or local restrictions, "
        "or guidance from Extension professionals."
    )


def get_result_disclaimer(cached_pula_found: bool) -> str:
    if cached_pula_found:
        return (
            "A cached PULA polygon may intersect this point. Verify in EPA "
            "Bulletins Live! Two for your product, location, and application "
            "month before applying."
        )
    return (
        "No cached PULA was found in this educational snapshot. Verify in EPA "
        "Bulletins Live! Two for your product, location, and application month "
        "before applying."
    )


def get_resistance_disclaimer() -> str:
    return (
        "Resistance context is based on reported database records and does not "
        "confirm resistance in a specific field or prove that an unlisted "
        "herbicide group will be effective."
    )
```

- [ ] **Step 4: Run disclaimer tests**

Run:

```powershell
python -m pytest tests/test_disclaimers.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit disclaimer guardrails**

Run:

```powershell
git add src/__init__.py src/disclaimers.py tests/test_disclaimers.py
git commit -m "feat: add disclaimer guardrails"
```

---

## Task 3: Suspected Resistance Report Capture

**Files:**
- Create: `src/reports.py`
- Create: `tests/test_reports.py`

- [ ] **Step 1: Write failing report tests**

Write `tests/test_reports.py` with:

```python
import csv
from pathlib import Path

from src.reports import (
    REPORT_COLUMNS,
    build_email_message,
    save_report,
    select_report_recipient,
)


def valid_report():
    return {
        "reporter_role": "Grower",
        "contact_name": "Test Reporter",
        "contact_phone": "334-555-0100",
        "contact_email": "reporter@example.com",
        "permission_to_contact": "yes",
        "county": "Lee",
        "location_description": "Field edge near county road",
        "crop_or_site": "Soybean",
        "suspected_weed": "Palmer amaranth",
        "herbicide_product": "Example product",
        "active_ingredient": "Example active",
        "site_of_action": "Group 15",
        "application_date": "2026-06-01",
        "application_rate": "Label rate",
        "survivor_pattern": "Patchy",
        "prior_herbicide_history": "Group 9 used previously",
        "weather_notes": "Warm and dry",
        "photo_paths": "",
    }


def test_report_columns_include_contact_and_agronomic_fields():
    assert "contact_email" in REPORT_COLUMNS
    assert "crop_or_site" in REPORT_COLUMNS
    assert "suspected_weed" in REPORT_COLUMNS
    assert "survivor_pattern" in REPORT_COLUMNS


def test_save_report_appends_private_csv(tmp_path):
    report_path = tmp_path / "suspected_resistance_reports.csv"
    saved_path = save_report(valid_report(), report_path=report_path)
    assert saved_path == report_path

    with report_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert rows[0]["county"] == "Lee"
    assert rows[0]["suspected_weed"] == "Palmer amaranth"
    assert rows[0]["submission_status"] == "suspected"


def test_select_report_recipient_prefers_matching_specialty():
    contacts = [
        {
            "name": "Row Crop Specialist",
            "email": "row@example.com",
            "specialty_tags": "row crop;cotton;soybean",
        },
        {
            "name": "Forage Specialist",
            "email": "forage@example.com",
            "specialty_tags": "forage;pasture",
        },
    ]
    recipient = select_report_recipient("Soybean", contacts)
    assert recipient["email"] == "row@example.com"


def test_build_email_message_uses_suspected_language():
    message = build_email_message(valid_report(), {"email": "row@example.com"})
    assert "Suspected resistance report" in message["subject"]
    assert "not a confirmation" in message["body"]
    assert "Palmer amaranth" in message["body"]
```

- [ ] **Step 2: Run failing report tests**

Run:

```powershell
python -m pytest tests/test_reports.py -v
```

Expected: FAIL because `src.reports` does not exist.

- [ ] **Step 3: Implement report module**

Write `src/reports.py` with:

```python
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPORT_COLUMNS = [
    "submitted_at_utc",
    "submission_status",
    "reporter_role",
    "contact_name",
    "contact_phone",
    "contact_email",
    "permission_to_contact",
    "county",
    "location_description",
    "crop_or_site",
    "suspected_weed",
    "herbicide_product",
    "active_ingredient",
    "site_of_action",
    "application_date",
    "application_rate",
    "survivor_pattern",
    "prior_herbicide_history",
    "weather_notes",
    "photo_paths",
]


def normalize_report(report: dict) -> dict:
    normalized = {column: str(report.get(column, "")).strip() for column in REPORT_COLUMNS}
    normalized["submitted_at_utc"] = datetime.now(timezone.utc).isoformat()
    normalized["submission_status"] = "suspected"
    return normalized


def save_report(report: dict, report_path: Path | str = "data/private/suspected_resistance_reports.csv") -> Path:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = normalize_report(report)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return path


def select_report_recipient(crop_or_site: str, contacts: Iterable[dict]) -> dict:
    query = crop_or_site.lower()
    fallback = None
    for contact in contacts:
        if fallback is None:
            fallback = contact
        tags = contact.get("specialty_tags", "").lower()
        if any(part.strip() and part.strip() in query for part in tags.split(";")):
            return contact
    return fallback or {"name": "Extension contact", "email": ""}


def build_email_message(report: dict, recipient: dict) -> dict:
    subject = f"Suspected resistance report: {report.get('suspected_weed', 'unknown weed')}"
    body = (
        "A suspected herbicide-resistance report was submitted through the "
        "PULA Awareness Tool. This is not a confirmation of resistance.\n\n"
        f"Recipient: {recipient.get('name', '')} <{recipient.get('email', '')}>\n"
        f"Reporter: {report.get('contact_name', '')} ({report.get('reporter_role', '')})\n"
        f"Email: {report.get('contact_email', '')}\n"
        f"Phone: {report.get('contact_phone', '')}\n"
        f"County: {report.get('county', '')}\n"
        f"Crop or site: {report.get('crop_or_site', '')}\n"
        f"Suspected weed: {report.get('suspected_weed', '')}\n"
        f"Herbicide product: {report.get('herbicide_product', '')}\n"
        f"Active ingredient: {report.get('active_ingredient', '')}\n"
        f"Site of action: {report.get('site_of_action', '')}\n"
        f"Survivor pattern: {report.get('survivor_pattern', '')}\n"
        f"Notes: {report.get('weather_notes', '')}\n"
    )
    return {"subject": subject, "body": body}
```

- [ ] **Step 4: Run report tests**

Run:

```powershell
python -m pytest tests/test_reports.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit report capture**

Run:

```powershell
git add src/reports.py tests/test_reports.py
git commit -m "feat: add suspected resistance report capture"
```

---

## Task 4: Extension Contacts Data And Routing

**Files:**
- Create: `src/extension_contacts.py`
- Create: `data/extension_contacts_alabama.csv`
- Modify: `tests/test_reports.py`

- [ ] **Step 1: Add contact-loading tests**

Append to `tests/test_reports.py`:

```python
from src.extension_contacts import load_contacts, contacts_for_crop_or_site


def test_load_contacts_reads_expected_columns(tmp_path):
    path = tmp_path / "contacts.csv"
    path.write_text(
        "name,role,email,phone,specialty,crop_focus,specialty_tags,source_url,verified_as_of\n"
        "Specialist,Weed Scientist,specialist@example.com,334-555-0000,Row crops,Soybean,row crop;soybean,https://example.com,2026-06-25\n",
        encoding="utf-8",
    )
    contacts = load_contacts(path)
    assert contacts[0]["name"] == "Specialist"
    assert contacts[0]["verified_as_of"] == "2026-06-25"


def test_contacts_for_crop_or_site_filters_by_tags(tmp_path):
    path = tmp_path / "contacts.csv"
    path.write_text(
        "name,role,email,phone,specialty,crop_focus,specialty_tags,source_url,verified_as_of\n"
        "Row Specialist,Weed Scientist,row@example.com,334-555-0001,Row crops,Cotton,row crop;cotton;soybean,https://example.com,2026-06-25\n"
        "Forage Specialist,Weed Scientist,forage@example.com,334-555-0002,Forage,Pasture,forage;pasture,https://example.com,2026-06-25\n",
        encoding="utf-8",
    )
    contacts = contacts_for_crop_or_site("cotton", path)
    assert len(contacts) == 1
    assert contacts[0]["email"] == "row@example.com"
```

- [ ] **Step 2: Run failing contact tests**

Run:

```powershell
python -m pytest tests/test_reports.py -v
```

Expected: FAIL because `src.extension_contacts` does not exist.

- [ ] **Step 3: Implement contact loader**

Write `src/extension_contacts.py` with:

```python
import csv
from pathlib import Path


CONTACT_COLUMNS = [
    "name",
    "role",
    "email",
    "phone",
    "specialty",
    "crop_focus",
    "specialty_tags",
    "source_url",
    "verified_as_of",
]


def load_contacts(path: Path | str = "data/extension_contacts_alabama.csv") -> list[dict]:
    contact_path = Path(path)
    if not contact_path.exists():
        return []
    with contact_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contacts_for_crop_or_site(crop_or_site: str, path: Path | str = "data/extension_contacts_alabama.csv") -> list[dict]:
    query = crop_or_site.lower()
    matches = []
    for contact in load_contacts(path):
        tags = contact.get("specialty_tags", "").lower().split(";")
        if any(tag.strip() and tag.strip() in query for tag in tags):
            matches.append(contact)
    return matches
```

- [ ] **Step 4: Add initial contact CSV schema**

Write `data/extension_contacts_alabama.csv` with this header and verification-needed seed row:

```csv
name,role,email,phone,specialty,crop_focus,specialty_tags,source_url,verified_as_of
Alabama Extension County Office Lookup,County Extension Office Lookup,,,"Local county support","All crops and managed sites","county;local;unknown","https://www.aces.edu/counties/",2026-06-25
```

Before public launch, replace or supplement this row with verified current specialist records from official Alabama Extension or Auburn pages.

- [ ] **Step 5: Run report and contact tests**

Run:

```powershell
python -m pytest tests/test_reports.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit contact routing**

Run:

```powershell
git add src/extension_contacts.py data/extension_contacts_alabama.csv tests/test_reports.py
git commit -m "feat: add extension contact routing"
```

---

## Task 5: Spatial Utilities

**Files:**
- Create: `src/spatial.py`
- Create: `tests/test_spatial.py`

- [ ] **Step 1: Write failing spatial tests**

Write `tests/test_spatial.py` with:

```python
import geopandas as gpd
from shapely.geometry import Point, Polygon

from src.spatial import nearest_feature_distance_miles, point_in_polygons


def sample_gdf():
    polygon = Polygon([(-86.7, 32.5), (-86.6, 32.5), (-86.6, 32.6), (-86.7, 32.6)])
    return gpd.GeoDataFrame({"name": ["sample"]}, geometry=[polygon], crs="EPSG:4326")


def test_point_in_polygons_detects_inside_point():
    result = point_in_polygons(32.55, -86.65, sample_gdf())
    assert len(result) == 1
    assert result.iloc[0]["name"] == "sample"


def test_point_in_polygons_returns_empty_for_outside_point():
    result = point_in_polygons(33.0, -87.0, sample_gdf())
    assert result.empty


def test_nearest_feature_distance_uses_projected_units():
    distance = nearest_feature_distance_miles(32.7, -86.65, sample_gdf())
    assert distance > 5
    assert distance < 15
```

- [ ] **Step 2: Run failing spatial tests**

Run:

```powershell
python -m pytest tests/test_spatial.py -v
```

Expected: FAIL because `src.spatial` does not exist.

- [ ] **Step 3: Implement spatial utilities**

Write `src/spatial.py` with:

```python
import geopandas as gpd
from shapely.geometry import Point


WGS84 = "EPSG:4326"
CONUS_ALBERS = "EPSG:5070"
METERS_PER_MILE = 1609.344


def _point_gdf(lat: float, lon: float) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame({"id": [1]}, geometry=[Point(lon, lat)], crs=WGS84)


def point_in_polygons(lat: float, lon: float, polygons: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if polygons.empty:
        return polygons
    point = Point(lon, lat)
    source = polygons
    if source.crs is None:
        source = source.set_crs(WGS84)
    return source[source.geometry.contains(point)]


def nearest_feature_distance_miles(lat: float, lon: float, polygons: gpd.GeoDataFrame) -> float | None:
    if polygons.empty:
        return None
    source = polygons
    if source.crs is None:
        source = source.set_crs(WGS84)
    projected_polygons = source.to_crs(CONUS_ALBERS)
    projected_point = _point_gdf(lat, lon).to_crs(CONUS_ALBERS).geometry.iloc[0]
    meters = projected_polygons.geometry.distance(projected_point).min()
    return float(meters / METERS_PER_MILE)
```

- [ ] **Step 4: Run spatial tests**

Run:

```powershell
python -m pytest tests/test_spatial.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit spatial utilities**

Run:

```powershell
git add src/spatial.py tests/test_spatial.py
git commit -m "feat: add spatial utilities"
```

---

## Task 6: Data Loading And Snapshot Metadata

**Files:**
- Create: `src/data_epa.py`
- Create: `src/data_heap.py`
- Create: `data/snapshot_metadata.json`
- Create: `tests/test_data.py`

- [ ] **Step 1: Write failing data tests**

Write `tests/test_data.py` with:

```python
import json

import pandas as pd

from src.data_epa import load_snapshot_metadata, validate_metadata
from src.data_heap import filter_resistance_by_state, heap_attribution


def test_validate_metadata_requires_dates_and_sources(tmp_path):
    path = tmp_path / "snapshot_metadata.json"
    path.write_text(
        json.dumps(
            {
                "pula_date": "2026-06-25",
                "heap_date": "2026-06-25",
                "source_urls": {
                    "blt": "https://www.epa.gov/endangered-species/bulletins-live-two-view-bulletins",
                    "heap": "https://www.weedscience.org/Summary/Country.aspx?CountryID=45",
                },
            }
        ),
        encoding="utf-8",
    )
    metadata = load_snapshot_metadata(path)
    assert validate_metadata(metadata) is True


def test_filter_resistance_by_state_matches_state_name():
    frame = pd.DataFrame(
        [
            {"State": "Alabama", "Common Name": "Palmer amaranth", "Site of Action": "Group 9"},
            {"State": "Georgia", "Common Name": "Horseweed", "Site of Action": "Group 2"},
        ]
    )
    result = filter_resistance_by_state(frame, "Alabama")
    assert len(result) == 1
    assert result.iloc[0]["Common Name"] == "Palmer amaranth"


def test_heap_attribution_names_source():
    text = heap_attribution()
    assert "Heap" in text
    assert "weedscience.org" in text
```

- [ ] **Step 2: Run failing data tests**

Run:

```powershell
python -m pytest tests/test_data.py -v
```

Expected: FAIL because `src.data_epa` and `src.data_heap` do not exist.

- [ ] **Step 3: Implement EPA metadata loader**

Write `src/data_epa.py` with:

```python
import json
from pathlib import Path

import geopandas as gpd


REQUIRED_METADATA_KEYS = {"pula_date", "heap_date", "source_urls"}


def load_snapshot_metadata(path: Path | str = "data/snapshot_metadata.json") -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_metadata(metadata: dict) -> bool:
    if not REQUIRED_METADATA_KEYS.issubset(metadata):
        return False
    source_urls = metadata.get("source_urls", {})
    return bool(metadata.get("pula_date") and metadata.get("heap_date") and source_urls.get("blt") and source_urls.get("heap"))


def load_pula_geojson(path: Path | str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    return gdf
```

- [ ] **Step 4: Implement Heap loader helpers**

Write `src/data_heap.py` with:

```python
from pathlib import Path

import pandas as pd

from src.disclaimers import HEAP_CITATION


def load_resistance_csv(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path)


def filter_resistance_by_state(frame: pd.DataFrame, state: str) -> pd.DataFrame:
    if "State" not in frame.columns:
        return frame.iloc[0:0].copy()
    return frame[frame["State"].astype(str).str.lower() == state.lower()].copy()


def heap_attribution() -> str:
    return HEAP_CITATION
```

- [ ] **Step 5: Add initial snapshot metadata**

Write `data/snapshot_metadata.json` with:

```json
{
  "pula_date": "not-yet-fetched",
  "heap_date": "not-yet-fetched",
  "source_urls": {
    "blt": "https://www.epa.gov/endangered-species/bulletins-live-two-view-bulletins",
    "palm": "https://www.epa.gov/pesticides/mitigation-menu",
    "heap": "https://www.weedscience.org/Summary/Country.aspx?CountryID=45"
  },
  "notes": "Initial metadata placeholder. Replace dates after verified data snapshots are fetched."
}
```

- [ ] **Step 6: Run data tests**

Run:

```powershell
python -m pytest tests/test_data.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit data loaders**

Run:

```powershell
git add src/data_epa.py src/data_heap.py data/snapshot_metadata.json tests/test_data.py
git commit -m "feat: add data loading helpers"
```

---

## Task 7: Streamlit MVP Shell

**Files:**
- Create: `app.py`
- Modify: `src/reports.py`

- [ ] **Step 1: Add optional email helper to reports module**

Append to `src/reports.py`:

```python
import smtplib
from email.message import EmailMessage


def send_email_notification(message: dict, smtp_settings: dict | None) -> bool:
    if not smtp_settings:
        return False
    required = ["host", "port", "username", "password", "sender", "recipient"]
    if any(not smtp_settings.get(key) for key in required):
        return False

    email = EmailMessage()
    email["Subject"] = message["subject"]
    email["From"] = smtp_settings["sender"]
    email["To"] = smtp_settings["recipient"]
    email.set_content(message["body"])

    with smtplib.SMTP_SSL(smtp_settings["host"], int(smtp_settings["port"])) as smtp:
        smtp.login(smtp_settings["username"], smtp_settings["password"])
        smtp.send_message(email)
    return True
```

- [ ] **Step 2: Create Streamlit app shell**

Write `app.py` with:

```python
from pathlib import Path

import folium
import streamlit as st
from streamlit_folium import st_folium

from src.data_epa import load_snapshot_metadata, validate_metadata
from src.data_heap import heap_attribution
from src.disclaimers import (
    BLT_URL,
    HEAP_URL,
    PALM_URL,
    get_primary_disclaimer,
    get_resistance_disclaimer,
    get_result_disclaimer,
)
from src.extension_contacts import contacts_for_crop_or_site, load_contacts
from src.reports import build_email_message, save_report, select_report_recipient, send_email_notification


st.set_page_config(page_title="PULA Awareness Tool", layout="wide")


def smtp_settings_from_secrets() -> dict | None:
    if "smtp" not in st.secrets:
        return None
    smtp = st.secrets["smtp"]
    return {
        "host": smtp.get("host"),
        "port": smtp.get("port"),
        "username": smtp.get("username"),
        "password": smtp.get("password"),
        "sender": smtp.get("sender"),
        "recipient": smtp.get("recipient"),
    }


st.title("PULA Awareness Tool")
st.warning(get_primary_disclaimer())

metadata = load_snapshot_metadata()
if validate_metadata(metadata):
    st.caption(f"PULA data as of: {metadata['pula_date']} | Resistance data as of: {metadata['heap_date']}")
else:
    st.caption("Data snapshots are not yet verified.")

link_cols = st.columns(3)
link_cols[0].link_button("EPA Bulletins Live! Two", BLT_URL)
link_cols[1].link_button("EPA PALM", PALM_URL)
link_cols[2].link_button("weedscience.org", HEAP_URL)

left, right = st.columns([2, 1])

with left:
    st.subheader("Map")
    m = folium.Map(location=[32.8067, -86.7911], zoom_start=7, tiles="CartoDB positron")
    folium.Marker([32.8067, -86.7911], tooltip="Alabama center").add_to(m)
    map_state = st_folium(m, height=520, use_container_width=True)

    clicked = map_state.get("last_clicked") if map_state else None
    if clicked:
        st.info(get_result_disclaimer(cached_pula_found=False))
        st.write(f"Clicked location: {clicked['lat']:.5f}, {clicked['lng']:.5f}")
    else:
        st.info("Click the map to start an educational cached-PULA check.")

with right:
    st.subheader("Resistance Context")
    st.caption(heap_attribution())
    st.write(get_resistance_disclaimer())
    st.write("Alabama resistance records will appear here after the verified snapshot is loaded.")

    st.subheader("Local Support")
    crop_or_site = st.text_input("Crop or managed site", placeholder="Example: soybean, cotton, pasture")
    matching_contacts = contacts_for_crop_or_site(crop_or_site) if crop_or_site else load_contacts()
    if matching_contacts:
        for contact in matching_contacts:
            st.write(f"**{contact.get('name', '')}**")
            st.write(contact.get("specialty", ""))
            if contact.get("email"):
                st.write(contact["email"])
            if contact.get("phone"):
                st.write(contact["phone"])
            if contact.get("source_url"):
                st.link_button("Official contact page", contact["source_url"])
    else:
        st.write("Use the Alabama Extension county office lookup for local routing.")

st.divider()
st.subheader("Report Suspected Resistance")
st.caption("Submissions are suspected cases only and are not confirmations of resistance.")

with st.form("suspected_resistance_report"):
    reporter_role = st.selectbox("Reporter role", ["Grower", "Consultant", "Extension agent", "Applicator", "Researcher", "Other"])
    contact_name = st.text_input("Contact name")
    contact_phone = st.text_input("Contact phone")
    contact_email = st.text_input("Contact email")
    permission_to_contact = st.checkbox("I give Extension permission to contact me about this suspected case.")
    county = st.text_input("County")
    location_description = st.text_area("Field or location description")
    crop_or_site_report = st.text_input("Crop or managed site for this report")
    suspected_weed = st.text_input("Suspected weed species")
    herbicide_product = st.text_input("Herbicide product")
    active_ingredient = st.text_input("Active ingredient, if known")
    site_of_action = st.text_input("Site of action/group, if known")
    application_date = st.text_input("Application date")
    application_rate = st.text_input("Application rate")
    survivor_pattern = st.selectbox("Surviving weed pattern", ["Unknown", "Patchy", "Widespread", "Field-wide", "Along edges", "Other"])
    prior_herbicide_history = st.text_area("Prior herbicide history, if known")
    weather_notes = st.text_area("Weather or application notes")
    submitted = st.form_submit_button("Submit suspected resistance report")

if submitted:
    report = {
        "reporter_role": reporter_role,
        "contact_name": contact_name,
        "contact_phone": contact_phone,
        "contact_email": contact_email,
        "permission_to_contact": "yes" if permission_to_contact else "no",
        "county": county,
        "location_description": location_description,
        "crop_or_site": crop_or_site_report,
        "suspected_weed": suspected_weed,
        "herbicide_product": herbicide_product,
        "active_ingredient": active_ingredient,
        "site_of_action": site_of_action,
        "application_date": application_date,
        "application_rate": application_rate,
        "survivor_pattern": survivor_pattern,
        "prior_herbicide_history": prior_herbicide_history,
        "weather_notes": weather_notes,
        "photo_paths": "",
    }
    saved_path = save_report(report)
    contacts = load_contacts()
    recipient = select_report_recipient(crop_or_site_report, contacts)
    message = build_email_message(report, recipient)
    email_sent = send_email_notification(message, smtp_settings_from_secrets())
    st.success(f"Report saved to {Path(saved_path).name}.")
    if email_sent:
        st.success("Email notification sent.")
    else:
        st.info("Email notification is not configured. The report was saved for follow-up.")
```

- [ ] **Step 3: Run syntax check**

Run:

```powershell
python -m py_compile app.py src/disclaimers.py src/reports.py src/extension_contacts.py src/spatial.py src/data_epa.py src/data_heap.py
```

Expected: no output and exit code 0.

- [ ] **Step 4: Run all tests**

Run:

```powershell
python -m pytest tests -v
```

Expected: PASS.

- [ ] **Step 5: Commit Streamlit shell**

Run:

```powershell
git add app.py src/reports.py
git commit -m "feat: add streamlit mvp shell"
```

---

## Task 8: Local Run Verification

**Files:**
- No code files required unless verification reveals a defect.

- [ ] **Step 1: Start Streamlit**

Run:

```powershell
streamlit run app.py
```

Expected: local URL appears and the app starts without import errors.

- [ ] **Step 2: Verify first screen**

Open the local URL and confirm:

- The first screen says `PULA Awareness Tool`.
- The disclaimer is visible without scrolling.
- BLT, PALM, and weedscience.org buttons are visible.
- The map renders centered on Alabama.
- Resistance context cites Heap.
- Local Support panel appears.
- Report Suspected Resistance form appears.

- [ ] **Step 3: Submit a test suspected-resistance report**

Use non-real test data:

```text
Reporter role: Grower
Contact name: Test User
Contact phone: 334-555-0100
Contact email: test@example.com
County: Lee
Crop or managed site: soybean
Suspected weed species: Palmer amaranth
Surviving weed pattern: Patchy
```

Expected:

- App shows report saved.
- If SMTP secrets are absent, app says email notification is not configured.
- `data/private/suspected_resistance_reports.csv` exists locally.
- `git status --short` does not show the private CSV because `.gitignore` excludes it.

- [ ] **Step 4: Stop Streamlit**

Stop the server with `Ctrl+C`.

- [ ] **Step 5: Commit any verification fixes**

If fixes were required, run:

```powershell
git add <changed-public-files>
git commit -m "fix: address mvp verification issues"
```

If no fixes were required, do not create an empty commit.

---

## Task 9: External Data Verification Preparation

**Files:**
- Modify: `docs/data_sources.md`
- Optionally create: `tools/verify_sources.py`

- [ ] **Step 1: Add explicit live-verification checklist**

Append to `docs/data_sources.md`:

```markdown
## Live Verification Checklist

Before publishing a public demo:

- Verify the current BLT route or workflow for product/location/month checks.
- Verify the EPA PULA polygon source endpoint and schema.
- Verify the EPA PULA limitations CSV source and schema if used.
- Verify the current weedscience.org U.S. resistance table structure.
- Verify Alabama Extension specialist contact records from official pages.
- Record verification dates in `data/snapshot_metadata.json` or the contact CSV.
```

- [ ] **Step 2: Commit verification notes**

Run:

```powershell
git add docs/data_sources.md
git commit -m "docs: add live source verification checklist"
```

---

## Final Verification

- [ ] **Run syntax checks**

```powershell
python -m py_compile app.py src/disclaimers.py src/reports.py src/extension_contacts.py src/spatial.py src/data_epa.py src/data_heap.py
```

Expected: no output and exit code 0.

- [ ] **Run test suite**

```powershell
python -m pytest tests -v
```

Expected: all tests pass.

- [ ] **Check git status**

```powershell
git status --short
```

Expected: no unexpected public files. `data/private/` should not appear.


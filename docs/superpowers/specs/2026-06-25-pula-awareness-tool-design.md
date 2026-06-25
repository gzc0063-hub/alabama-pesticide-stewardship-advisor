# PULA Awareness Tool Design

## Purpose

The PULA Awareness Tool is an educational, decision-support web app that helps users view U.S. EPA Pesticide Use Limitation Area context alongside herbicide-resistance context. The tool starts with Alabama and is designed to expand to the full United States after the Alabama workflow is validated.

The tool does not make compliance determinations. It routes users to EPA Bulletins Live! Two, PALM, pesticide labels, and Extension professionals for official or site-specific decisions.

## Product Decisions

- Public name: **PULA Awareness Tool**.
- First release scope: Alabama MVP.
- Expansion scope: whole-USA support after Alabama data retrieval, map behavior, reporting, and validation are working.
- Primary framing: educational planning and resistance context, not compliance or herbicide recommendation.
- Required tone: cautious, precise, and source-attributed throughout the interface and documentation.

## Compliance And Legal Boundary

The app must show disclaimer language on first load and in every result panel. Outputs must not say that a user is compliant, non-compliant, officially inside a PULA, or officially outside a PULA.

Allowed phrasing:

- "A cached PULA polygon may intersect this point. Verify in EPA Bulletins Live! Two for your product, location, and application month."
- "No cached PULA was found in this educational snapshot. Verify in EPA Bulletins Live! Two before applying."
- "This tool is not a substitute for EPA Bulletins Live! Two, PALM, pesticide labels, state/local restrictions, or Extension guidance."

Disallowed phrasing:

- "You are in compliance."
- "No PULA applies."
- "This product is legal to spray."
- "This is the recommended herbicide."

## Data Sources

### EPA PULA Data

The app will use cached EPA PULA polygon snapshots for map display and point checks. Each snapshot must include a visible "data as of" date and links to live EPA systems.

The app must document exact EPA endpoints in `docs/data_sources.md` after verification. The implementation must treat endpoint or schema changes as validation failures instead of silently producing stale or malformed data.

### Heap / weedscience.org Resistance Data

Resistance context comes from the International Herbicide-Resistant Weed Database at weedscience.org. The app must cite Heap wherever this data appears in the interface, README, methods documentation, and data-source documentation.

The app may use scraped resistance data during development and for displayed context, but it must not imply ownership of the database. Permission should still be requested before broad public redistribution of copied datasets.

The resistance panel must frame data as reported resistance records, not as complete proof that a site has or does not have resistance.

## Extension Support

The Alabama MVP must include a Local Support panel. The panel should provide verified Alabama Extension contacts where available, including names, roles, crop/site specialties, phone numbers, emails, and official profile or office links.

The app should distinguish specialist routing from county routing:

- Crop/site-specific specialist contacts for row crops, forage/pasture, turf/ornamentals, aquatic/invasive plants, and other relevant categories.
- County Extension office lookup or county contact routing for local support.

Contact information changes over time, so contacts must be stored in a data file with source URLs and "verified as of" metadata. The app must avoid hard-coding contacts directly into UI code.

## Suspected Resistance Reporting

The app will include a "Report Suspected Resistance" workflow. Reports are suspected cases only and must not be labeled confirmed resistance.

The form must collect:

- Reporter role.
- Contact name, phone, and email.
- Permission to be contacted by Extension.
- County.
- Optional field/location description.
- Crop or managed site.
- Suspected weed species.
- Herbicide product, active ingredient, and site of action if known.
- Application date, rate, and timing details if known.
- Surviving weed pattern.
- Prior herbicide history if known.
- Weather or application notes.
- Optional photo attachment if feasible in the selected deployment environment.

Each submission must be saved to a private CSV for project tracking. The CSV must be excluded from git if it contains personal contact details, exact field descriptions, or uploaded-file references.

Each submission must also trigger an email notification when email settings are configured. Routing should prefer crop/site-specific specialists when the report category maps cleanly to a specialty. Otherwise, it should route to a default Extension contact or county office lookup path.

If email is not configured, the app must still save the CSV and show a clear message that the report was saved but email notification is not active.

## User Interface

The MVP should use Streamlit with Folium/Leaflet mapping. The first screen should be the actual working tool, not a marketing landing page.

Core interface areas:

- Header with app name, data freshness badge, and disclaimer.
- Map focused on Alabama PULA polygons.
- Location input through map click first, with address/manual coordinate support if practical.
- Result panel with cautious PULA-awareness language and BLT/PALM links.
- Resistance context panel with Heap citation and reported resistant species/sites of action.
- Local Support panel with Extension contacts and county routing.
- Report Suspected Resistance form.

## Architecture

Planned repo structure:

```text
app.py
requirements.txt
README.md
PROJECT_PLAN.md
.gitignore
.streamlit/config.toml
src/
  __init__.py
  disclaimers.py
  data_epa.py
  data_heap.py
  extension_contacts.py
  reports.py
  spatial.py
data/
  snapshot_metadata.json
  extension_contacts_alabama.csv
docs/
  data_sources.md
  methods.md
tests/
  test_disclaimers.py
  test_reports.py
  test_spatial.py
```

Private runtime outputs:

```text
data/private/suspected_resistance_reports.csv
data/private/uploads/
```

Private runtime outputs must be listed in `.gitignore`.

## Testing And Validation

Phase 0 validation must prove that source endpoints and local schemas are understood before UI work depends on them.

Required early tests:

- Disclaimer text contains BLT/PALM/legal-boundary language.
- Report CSV writing preserves expected columns and appends records safely.
- Email notification can be built without credentials being hard-coded.
- Spatial utilities use projected distance calculations for nearest-PULA logic.

Phase 1 validation must compare at least 20 Alabama test points against official BLT behavior before making any confidence claims in the README.

## Open Implementation Notes

Email sending should use Streamlit secrets or environment variables. The repo must include documented secret names but no actual credentials.

The current project plan file from Downloads contains encoding artifacts. The repo version should be cleaned before it becomes public documentation.

The Alabama MVP should be useful even if live data fetching is temporarily unavailable by using dated cached snapshots with clear source and freshness labels.

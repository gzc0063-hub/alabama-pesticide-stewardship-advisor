# PULA Awareness Tool

An educational, decision-support web map that pairs U.S. EPA Pesticide Use Limitation Area awareness with state-level herbicide-resistance context and routes users to EPA Bulletins Live! Two for official compliance checks.

> **This tool is not a compliance system.** It does not replace EPA Bulletins Live! Two, EPA PALM, pesticide labels, state or local restrictions, or Extension guidance. Applicators must verify official requirements in BLT for their product, location, and application month before applying.

## 1. Why This Exists

EPA Bulletins Live! Two provides official pesticide use limitation bulletins. EPA PALM supports mitigation planning. weedscience.org provides reported herbicide-resistance records. This project sits between regulatory awareness and agronomic context without replacing any official system.

The tool is designed to help users ask better questions:

- Could a cached PULA polygon be relevant near this location?
- What herbicide-resistance records have been reported in this state?
- Which Extension specialist or county office should a user contact for local interpretation?
- How can a suspected resistance case be reported for follow-up?

## 2. Locked Scope Decisions

1. **Education, not compliance.** Every output routes users to BLT, PALM, labels, and Extension.
2. **Alabama first, United States later.** The MVP validates the workflow in Alabama before national expansion.
3. **Careful resistance framing.** Resistance data is attributed to Heap/weedscience.org and shown as reported context, not field confirmation or herbicide advice.
4. **Extension routing.** The app provides Extension contacts by crop/site specialty and county lookup where possible.
5. **Suspected resistance reporting.** Reports are saved privately to CSV and emailed when notification settings are configured.
6. **Dated snapshots.** Cached data carries visible freshness metadata and links to live official sources.

## 3. Architecture And Stack

- **Frontend/host:** Streamlit with `streamlit-folium`.
- **Map:** Folium/Leaflet basemap with Alabama-focused PULA awareness.
- **Spatial logic:** GeoPandas, Shapely, and PyProj. Distances use EPSG:5070, not raw latitude/longitude.
- **Data handling:** Cached source snapshots with metadata and validation checks.
- **Reports:** Private CSV storage under `data/private/` plus optional SMTP email notification through Streamlit secrets or environment settings.

## 4. Planned Repository Structure

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

Private runtime outputs are excluded from git:

```text
data/private/suspected_resistance_reports.csv
data/private/uploads/
```

## 5. Phase Plan

### Phase 0: Setup And Source Validation

- Initialize the repo with clean documentation and dependency files.
- Document BLT, PALM, PULA, Heap, and Extension data-source posture.
- Add centralized disclaimer language.
- Add report storage and notification plumbing.
- Add early tests for wording, report handling, and spatial behavior.

### Phase 1: Alabama MVP

- Render a Streamlit map centered on Alabama.
- Show cautious cached-PULA awareness result language after map interaction.
- Show resistance context with Heap citation.
- Show Extension routing panel.
- Support suspected resistance reports saved to private CSV and email when configured.

### Phase 2: Verified Data Integration

- Fetch and validate Alabama PULA snapshots.
- Fetch or prepare resistance context with visible Heap attribution.
- Verify at least 20 Alabama test points against official BLT behavior before public confidence claims.
- Replace placeholder contacts with verified current Extension specialist records.

### Phase 3: Public Demo

- Deploy to Streamlit Community Cloud.
- Add screenshots and demo materials.
- Add refresh automation only after source validation is stable.

### Phase 4: United States Expansion

- Expand PULA and resistance context nationally.
- Add state-scoped loading, geometry simplification, or tiling if needed.
- Add stronger automation and freshness monitoring.

## 6. Non-Negotiable Language Rules

Allowed result language:

- "A cached PULA polygon may intersect this point. Verify in EPA Bulletins Live! Two for your product, location, and application month."
- "No cached PULA was found in this educational snapshot. Verify in EPA Bulletins Live! Two before applying."

Disallowed result language:

- "You are in compliance."
- "No PULA applies."
- "This product is legal to spray."
- "This is the recommended herbicide."

## 7. Definition Of Done For Alabama MVP Foundation

- Streamlit app starts locally.
- Disclaimer is visible on load.
- BLT, PALM, and weedscience.org links are visible.
- Report form saves suspected resistance reports to a private CSV.
- Email notification path exists and safely no-ops when SMTP settings are missing.
- Early tests pass.
- Private report outputs are excluded from git.

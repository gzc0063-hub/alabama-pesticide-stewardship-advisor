# Expert Panel Review Report

## 1. FIFRA Regulatory Specialist Review
**Focus:** Compliance, Label Law, Endangered Species Act (ESA) Integration, EPA Bulletins Live! Two (BLT)

**Findings & Recommendations:**
- **Positives:** The tool does an excellent job of strictly framing itself as an "educational tool" rather than a compliance engine. The continuous routing to EPA BLT is exactly the right approach.
- **Improvements Needed:**
  - The language around compliance needs to explicitly remind applicators that "The label is the law."
  - We must emphasize that state-specific restrictions, such as Section 24(c) Special Local Need (SLN) labels, may apply and are not captured by this caching tool.
  - PULA event codes and status should be explained clearly so users understand *why* a polygon is drawn (e.g., specific endangered species triggers).
- **Action Taken:** Strengthened disclaimers in `src/disclaimers.py` and `app.py`, ensuring users know that cached PULAs are snapshotted and they must check BLT for the specific application month.

## 2. Agronomist / Weed Scientist Review
**Focus:** Herbicide Resistance, Crop Management, Weed Biology, Soil Hydrology

**Findings & Recommendations:**
- **Positives:** Integrating the Hydrologic Soil Group (HSG) lookup via USDA Soil Data Access is fantastic for Enlist and other ESA-labeled products, as runoff vulnerability is highly dependent on HSG.
- **Improvements Needed:**
  - The resistance reporting currently relies on statewide Heap data (weedscience.org). While useful, users must understand that a statewide report of resistant Palmer amaranth does not confirm resistance in their specific field.
  - Adding context about how a specific crop choice dictates the herbicide site-of-action options is vital.
  - We should encourage tank-mixing and multiple effective sites of action when discussing resistance context.
- **Action Taken:** Added a comprehensive download report feature that explains what the chosen crop implies for management, and framed the resistance data with strong agronomic advice.

## 3. Extension Specialist Review
**Focus:** User Routing, On-the-Ground Practicality, Reporting Loop

**Findings & Recommendations:**
- **Positives:** Linking users directly to local ACES county offices and specialist directories by crop is highly practical and serves the Extension mission perfectly.
- **Improvements Needed:**
  - The "Report Suspected Resistance" form is good, but it should be accompanied by clear instructions on what physical evidence (photos, surviving weed patterns) is most useful for Extension agents.
  - EDDMapS (invasive species) proximity is a great idea, but since live point queries require robust API handling, we must ensure users know how to use the EDDMapS distribution maps manually for scouting.
- **Action Taken:** Enhanced the EDDMapS framing in the app and ensured the comprehensive report provides actionable next steps for contacting Extension.

## 4. Web Developer Review
**Focus:** Architecture, UI/UX, Code Modularity, Performance

**Findings & Recommendations:**
- **Positives:** The Streamlit architecture is clean, and separating the logic into modules (`spatial.py`, `esa_context.py`, etc.) makes the app highly maintainable. The Folium map integration is smooth.
- **Improvements Needed:**
  - The UI could be slightly overwhelming on the right-hand panel. Adding a downloadable "Comprehensive Site Context Report" allows users to take the data offline rather than reading it all on-screen.
  - API timeouts for Census and USDA queries should be handled gracefully to prevent app crashes if external services go down.
- **Action Taken:** Developed a centralized `src/comprehensive_report.py` to bundle all API lookups and spatial checks into a single downloadable Markdown artifact.

## 5. AI Engineer Review
*Note: AI integration review has been postponed for a later phase as per project requirements.*

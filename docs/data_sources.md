# Data Sources

## EPA Bulletins Live! Two

EPA Bulletins Live! Two is the official system users must consult when pesticide labels direct them to obtain a bulletin. This app links users to BLT and does not replace it.

Endpoint and schema notes will be updated after live endpoint verification.

## EPA PALM

EPA PALM is linked as the official mitigation planning tool. This app does not recreate PALM calculations.

## PULA Polygon Snapshots

Cached PULA data must include a snapshot date and source URL. If a schema or endpoint changes, refresh scripts must fail validation instead of silently producing output.

The Alabama MVP uses EPA's BLT ArcGIS MapServer item:

- Item title: Bulletins Live! Two Pesticide Use Limitation Areas (PULAs)
- Service URL: `https://blt.epa.gov/arcgis/rest/services/BLT/PesticideUsageLimitationAreas/MapServer`
- Polygon layer: `Effective Pulas`, layer `0`
- Alabama snapshot: `data/pula_alabama.geojson`
- Simplified display layer: `data/pula_alabama_display.geojson`

The snapshot is spatially filtered by an Alabama bounding envelope, so it may include polygons crossing or near the state boundary. Results remain educational and must be verified in BLT.

## Herbicide Resistance

Resistance context is attributed to:

Heap, I. The International Herbicide-Resistant Weed Database. www.weedscience.org.

Displayed resistance information is reported database context, not proof that a specific field has or does not have resistance.

## Extension Contacts

Contact records must come from official Alabama Extension or Auburn pages and include a verified-as-of date.

The MVP contact list uses visible information from the ACES staff directory and county-office directory. ACES profile pages protect email addresses behind a "Get address" interaction, so this app links to official profiles rather than scraping or reconstructing email addresses.

Primary source links:

- ACES County Offices: `https://www.aces.edu/counties/`
- ACES Agronomic Crops directory: `https://ssl.acesag.auburn.edu/directory-new/programAgentSearch.php?program=1`
- Individual ACES profile pages listed in `data/extension_contacts_alabama.csv`

## Live Verification Checklist

Before publishing a public demo:

- Verify the current BLT route or workflow for product/location/month checks.
- Verify the EPA PULA polygon source endpoint and schema.
- Verify the EPA PULA limitations CSV source and schema if used.
- Verify the current weedscience.org U.S. resistance table structure.
- Verify Alabama Extension specialist contact records from official pages.
- Record verification dates in `data/snapshot_metadata.json` or the contact CSV.

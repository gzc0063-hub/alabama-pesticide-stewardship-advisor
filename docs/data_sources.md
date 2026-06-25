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

## Live Verification Checklist

Before publishing a public demo:

- Verify the current BLT route or workflow for product/location/month checks.
- Verify the EPA PULA polygon source endpoint and schema.
- Verify the EPA PULA limitations CSV source and schema if used.
- Verify the current weedscience.org U.S. resistance table structure.
- Verify Alabama Extension specialist contact records from official pages.
- Record verification dates in `data/snapshot_metadata.json` or the contact CSV.

# PULA Awareness Tool

Working broader review name: **Alabama Pesticide Stewardship Advisor**.

An educational planning tool that helps users view EPA Pesticide Use Limitation Area context alongside ESA mitigation planning, USDA soil/HSG context, herbicide-resistance context, weed/invasive occurrence context, and Alabama Extension routing. The first release focuses on Alabama and is designed for later U.S. expansion.

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
- USDA Soil Data Access for hydrologic soil group context.
- Heap, I. The International Herbicide-Resistant Weed Database. www.weedscience.org.
- EDDMapS distribution maps for linked weed/invasive occurrence context. The app does not yet ingest EDDMapS proximity records directly.
- Alabama Cooperative Extension System contact information from official Extension pages.

## Development

```powershell
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\streamlit run app.py
```

## Hosting

GitHub Pages can host the static project page in `docs/index.html` from the `docs/` folder. The interactive Streamlit app requires a Python-capable host such as Streamlit Community Cloud; after deployment, update the `Open App` link in `docs/index.html` to the live Streamlit URL.

See `DEPLOYMENT.md` for the recommended GitHub Pages plus Streamlit Community Cloud review setup.

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

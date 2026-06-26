# Deployment Guide

## Recommended Public Review Setup

Use two public links:

1. GitHub Pages hosts the static review/landing page from `docs/index.html`.
2. Streamlit Community Cloud hosts the interactive Python app from `app.py`.

GitHub Pages cannot run the Streamlit app by itself because Streamlit needs a Python server.

## Suggested Repository Name

Recommended public-facing name:

**Alabama Pesticide Stewardship Advisor**

The current app can keep `PULA Awareness Tool` during review, but the broader name better reflects the full scope: PULA awareness, ESA mitigation planning, USDA soil/HSG lookup, resistance context, EDDMapS occurrence context, Extension routing, and suspected resistance reporting.

Suggested GitHub repository slug:

`alabama-pesticide-stewardship-advisor`

## GitHub Pages

After the repository is pushed to GitHub:

1. Open the repository on GitHub.
2. Go to `Settings` -> `Pages`.
3. Set source to `Deploy from a branch`.
4. Choose the main branch and `/docs` folder.
5. Save.

The Pages URL will look like:

`https://gzc0063-hub.github.io/alabama-pesticide-stewardship-advisor/`

## Streamlit Community Cloud

1. Go to `https://share.streamlit.io/`.
2. Connect the GitHub repository.
3. Set the app entrypoint to `app.py`.
4. Use the repository root as the working directory.
5. Deploy.

After deployment, update the `Open App` link in `docs/index.html` to the Streamlit Cloud URL.

## Before Sharing Broadly

- Verify the EPA BLT source and snapshot date.
- Verify USDA Soil Data Access lookup behavior.
- Verify current ACES/Auburn Extension contact records.
- Keep EDDMapS labeled as occurrence context only until a stable approved proximity data source is integrated.
- Keep all pesticide and resistance language framed as educational planning context, not compliance or label advice.

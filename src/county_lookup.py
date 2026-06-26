from urllib.parse import quote_plus

import requests


CENSUS_GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"


def normalize_county_name(county_name: str) -> str:
    cleaned = " ".join(str(county_name).strip().split())
    if cleaned.lower().endswith(" county"):
        cleaned = cleaned[:-7]
    return cleaned.strip().title()


def county_contact_links(county_name: str) -> dict:
    county = normalize_county_name(county_name)
    slug = county.lower().replace(" ", "-")
    office = quote_plus(f"{county} County Office")
    return {
        "county": county,
        "office_url": f"https://www.aces.edu/counties/{slug}",
        "contact_url": f"https://www.aces.edu/contact-extension/?office={office}",
    }


def county_from_coordinates(lat: float, lon: float, timeout: int = 10) -> str | None:
    params = {
        "x": lon,
        "y": lat,
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "layers": "Counties",
        "format": "json",
    }
    response = requests.get(CENSUS_GEOCODER_URL, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    geographies = data.get("result", {}).get("geographies", {})
    counties = geographies.get("Counties", [])
    if not counties:
        return None
    return normalize_county_name(counties[0].get("NAME", ""))

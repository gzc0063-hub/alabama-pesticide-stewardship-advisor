import requests


USDA_SDA_URL = "https://sdmdataaccess.nrcs.usda.gov/tabular/post.rest"
ALABAMA_LAT_RANGE = (30.0, 35.5)
ALABAMA_LON_RANGE = (-89.0, -84.5)


def coordinates_in_alabama(lat: float, lon: float) -> bool:
    return (
        ALABAMA_LAT_RANGE[0] <= lat <= ALABAMA_LAT_RANGE[1]
        and ALABAMA_LON_RANGE[0] <= lon <= ALABAMA_LON_RANGE[1]
    )


def build_hsg_query(lat: float, lon: float) -> str:
    return f"""
SELECT TOP 1 hydgrp FROM mapunit mu
INNER JOIN component co ON co.mukey = mu.mukey
WHERE mu.mukey IN (
  SELECT * FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('POINT({lon} {lat})')
) AND co.comppct_r = (
  SELECT MAX(comppct_r) FROM component WHERE mukey = mu.mukey
)
""".strip()


def parse_hsg_response(data: dict) -> str | None:
    table = data.get("Table") or []
    if not table:
        return None
    first = table[0]
    if isinstance(first, dict):
        value = first.get("hydgrp") or first.get("hydgrpdcd") or next(iter(first.values()), None)
    elif isinstance(first, list) and first:
        value = first[0]
    else:
        value = None
    if not value:
        return None
    return str(value).strip().upper()


def lookup_hydrologic_soil_group(
    lat: float,
    lon: float,
    timeout: int = 15,
) -> dict:
    if not coordinates_in_alabama(lat, lon):
        return {
            "hsg": None,
            "source": "USDA Soil Data Access",
            "error": "Coordinates are outside the Alabama lookup range.",
        }
    query = build_hsg_query(lat, lon)
    try:
        response = requests.post(
            USDA_SDA_URL,
            data={"query": query, "format": "JSON"},
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return {
            "hsg": None,
            "source": "USDA Soil Data Access",
            "error": f"USDA soil lookup failed: {exc}",
        }

    hsg = parse_hsg_response(response.json())
    if not hsg:
        return {
            "hsg": None,
            "source": "USDA Soil Data Access",
            "error": "No hydrologic soil group was returned for this point.",
        }
    return {"hsg": hsg, "source": "USDA Soil Data Access", "error": None}

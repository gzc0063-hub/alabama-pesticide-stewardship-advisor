import json
from pathlib import Path
from datetime import datetime, timezone

import geopandas as gpd
from shapely.geometry import Point

from src.spatial import CONUS_ALBERS, METERS_PER_MILE, WGS84


REQUIRED_METADATA_KEYS = {"pula_date", "heap_date", "source_urls"}


def load_snapshot_metadata(path: Path | str = "data/snapshot_metadata.json") -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_metadata(metadata: dict) -> bool:
    if not REQUIRED_METADATA_KEYS.issubset(metadata):
        return False
    source_urls = metadata.get("source_urls", {})
    return bool(
        metadata.get("pula_date")
        and metadata.get("heap_date")
        and source_urls.get("blt")
        and source_urls.get("heap")
    )


def load_pula_geojson(path: Path | str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    return gdf


def pula_snapshot_summary(pulas: gpd.GeoDataFrame) -> dict:
    if pulas.empty:
        return {"feature_count": 0, "unique_pula_count": 0, "status_values": []}
    unique_count = (
        int(pulas["pula_id"].nunique())
        if "pula_id" in pulas.columns
        else int(len(pulas))
    )
    statuses = (
        sorted(str(value) for value in pulas["status"].dropna().unique())
        if "status" in pulas.columns
        else []
    )
    return {
        "feature_count": int(len(pulas)),
        "unique_pula_count": unique_count,
        "status_values": statuses,
    }


def _native_value(value):
    if hasattr(value, "item"):
        return value.item()
    return value


def format_epoch_or_text_date(value) -> str:
    value = _native_value(value)
    if value in (None, "", "nan"):
        return ""
    if isinstance(value, (int, float)):
        timestamp = value / 1000 if value > 10000000000 else value
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()
    return str(value)


def nearest_pula_summary(lat: float, lon: float, pulas: gpd.GeoDataFrame) -> dict | None:
    if pulas.empty:
        return None
    source = pulas
    if source.crs is None:
        source = source.set_crs(WGS84)
    projected = source.to_crs(CONUS_ALBERS)
    point = gpd.GeoSeries([Point(lon, lat)], crs=WGS84).to_crs(CONUS_ALBERS).iloc[0]
    distances = projected.geometry.distance(point)
    nearest_index = distances.idxmin()
    nearest = source.loc[nearest_index]
    distance_miles = float(distances.loc[nearest_index] / METERS_PER_MILE)
    return {
        "pula_id": _native_value(nearest.get("pula_id", "")),
        "event_name": _native_value(nearest.get("event_name", "")),
        "status": _native_value(nearest.get("status", "")),
        "codes": _native_value(nearest.get("codes", "")),
        "effective_date": format_epoch_or_text_date(nearest.get("effective_date", "")),
        "published_time_stamp": format_epoch_or_text_date(nearest.get("published_time_stamp", "")),
        "distance_miles": distance_miles,
    }

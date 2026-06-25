import json
from pathlib import Path

import geopandas as gpd


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

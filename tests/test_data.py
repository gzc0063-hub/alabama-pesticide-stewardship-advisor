import json

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from src.data_epa import (
    format_epoch_or_text_date,
    load_snapshot_metadata,
    nearest_pula_summary,
    pula_snapshot_summary,
    validate_metadata,
)
from src.data_heap import filter_resistance_by_state, heap_attribution


def test_validate_metadata_requires_dates_and_sources(tmp_path):
    path = tmp_path / "snapshot_metadata.json"
    path.write_text(
        json.dumps(
            {
                "pula_date": "2026-06-25",
                "heap_date": "2026-06-25",
                "source_urls": {
                    "blt": "https://www.epa.gov/endangered-species/bulletins-live-two-view-bulletins",
                    "heap": "https://www.weedscience.org/Summary/Country.aspx?CountryID=45",
                },
            }
        ),
        encoding="utf-8",
    )
    metadata = load_snapshot_metadata(path)
    assert validate_metadata(metadata) is True


def test_filter_resistance_by_state_matches_state_name():
    frame = pd.DataFrame(
        [
            {"State": "Alabama", "Common Name": "Palmer amaranth", "Site of Action": "Group 9"},
            {"State": "Georgia", "Common Name": "Horseweed", "Site of Action": "Group 2"},
        ]
    )
    result = filter_resistance_by_state(frame, "Alabama")
    assert len(result) == 1
    assert result.iloc[0]["Common Name"] == "Palmer amaranth"


def test_heap_attribution_names_source():
    text = heap_attribution()
    assert "Heap" in text
    assert "weedscience.org" in text


def test_pula_snapshot_summary_counts_features():
    frame = gpd.GeoDataFrame(
        {
            "pula_id": [101, 102],
            "event_name": ["Event A", "Event B"],
            "status": ["effective", "effective"],
        },
        geometry=[
            Polygon([(-86.7, 32.5), (-86.6, 32.5), (-86.6, 32.6), (-86.7, 32.6)]),
            Polygon([(-86.2, 32.8), (-86.1, 32.8), (-86.1, 32.9), (-86.2, 32.9)]),
        ],
        crs="EPSG:4326",
    )

    summary = pula_snapshot_summary(frame)

    assert summary["feature_count"] == 2
    assert summary["unique_pula_count"] == 2
    assert summary["status_values"] == ["effective"]


def test_nearest_pula_summary_returns_distance_and_attributes():
    frame = gpd.GeoDataFrame(
        {
            "pula_id": [101],
            "event_name": ["Nearest event"],
            "status": ["effective"],
            "codes": ["ESA_TEST"],
            "effective_date": ["2026-01-01"],
        },
        geometry=[
            Polygon([(-86.7, 32.5), (-86.6, 32.5), (-86.6, 32.6), (-86.7, 32.6)]),
        ],
        crs="EPSG:4326",
    )

    result = nearest_pula_summary(32.7, -86.65, frame)

    assert result is not None
    assert result["pula_id"] == 101
    assert result["event_name"] == "Nearest event"
    assert result["codes"] == "ESA_TEST"
    assert result["effective_date"] == "2026-01-01"
    assert result["distance_miles"] > 5
    assert result["distance_miles"] < 15


def test_format_epoch_or_text_date_converts_milliseconds():
    assert format_epoch_or_text_date(1770595200000) == "2026-02-09"
    assert format_epoch_or_text_date("2026-01-01") == "2026-01-01"

import json

import pandas as pd

from src.data_epa import load_snapshot_metadata, validate_metadata
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

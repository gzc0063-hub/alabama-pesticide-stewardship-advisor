from src.resistance_context import (
    load_alabama_resistance_context,
    resistance_context_for_crop,
    summarize_resistance_records,
)


def test_load_alabama_resistance_context_reads_snapshot():
    rows = load_alabama_resistance_context()

    assert len(rows) >= 10
    assert any(row["common_name"] == "Palmer Amaranth" for row in rows)


def test_resistance_context_for_crop_prioritizes_crop_tags():
    rows = [
        {
            "common_name": "Palmer Amaranth",
            "site_of_action": "EPSPS inhibitors (Group 9)",
            "first_year": "2008",
            "crop_tags": "cotton;soybean",
        },
        {
            "common_name": "Annual Bluegrass",
            "site_of_action": "PSII inhibitors (Group 5)",
            "first_year": "1980",
            "crop_tags": "turf",
        },
    ]

    matches = resistance_context_for_crop("cotton", rows)

    assert [match["common_name"] for match in matches] == ["Palmer Amaranth"]


def test_summarize_resistance_records_mentions_what_to_what():
    rows = [
        {
            "common_name": "Horseweed",
            "site_of_action": "EPSPS inhibitors (Group 9)",
            "first_year": "2013",
            "crop_tags": "cotton;soybean",
        }
    ]

    summary = summarize_resistance_records(rows)

    assert "Horseweed" in summary[0]
    assert "EPSPS inhibitors (Group 9)" in summary[0]

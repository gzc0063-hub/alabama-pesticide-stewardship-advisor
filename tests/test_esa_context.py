from src.esa_context import (
    active_esa_products_for_crop,
    build_mitigation_report,
    calculate_mitigation_summary,
    county_mitigation_context,
    enlist_runoff_points_for_hsg,
)


def test_county_mitigation_context_returns_vulnerability_and_points():
    context = county_mitigation_context("Baldwin County")

    assert context["county"] == "Baldwin"
    assert context["runoff_vulnerability"] == "High"
    assert context["county_relief_points"] == 0


def test_county_mitigation_context_gives_medium_county_relief():
    context = county_mitigation_context("Lee")

    assert context["runoff_vulnerability"] == "Medium"
    assert context["county_relief_points"] == 2


def test_active_esa_products_for_crop_matches_row_crops():
    products = active_esa_products_for_crop("cotton")

    assert {product["name"] for product in products} >= {
        "Liberty ULTRA",
        "Enlist One",
        "Enlist Duo",
    }


def test_enlist_runoff_points_for_hsg():
    assert enlist_runoff_points_for_hsg("A") == 4
    assert enlist_runoff_points_for_hsg("D") == 6


def test_build_mitigation_report_includes_recordkeeping_and_disclaimer():
    report = build_mitigation_report(
        lat=32.6,
        lon=-85.5,
        county="Lee",
        crop_or_site="cotton",
        pula_intersects=True,
        nearest_pula={
            "pula_id": 123,
            "distance_miles": 0.25,
            "event_name": "Test species event",
            "codes": "ABC",
        },
    )

    assert "Lee County" in report
    assert "32.600000, -85.500000" in report
    assert "Selected point appears inside a cached PULA polygon" in report
    assert "Test species event" in report
    assert "Liberty ULTRA" in report
    assert "recordkeeping" in report.lower()
    assert "planning" in report.lower()


def test_calculate_mitigation_summary_counts_county_practices_and_recordkeeping():
    summary = calculate_mitigation_summary(
        county="Lee",
        product_name="Liberty ULTRA",
        hsg="A",
        selected_practice_ids=["no-till", "vegetated-filter-strip"],
        recordkeeping=True,
    )

    assert summary["required_points"] == 3
    assert summary["county_relief_points"] == 2
    assert summary["practice_points"] == 3
    assert summary["recordkeeping_points"] == 1
    assert summary["total_points"] == 6
    assert summary["meets_points"] is True


def test_calculate_mitigation_summary_needs_hsg_for_enlist():
    summary = calculate_mitigation_summary(
        county="Baldwin",
        product_name="Enlist One",
        hsg="Unknown",
        selected_practice_ids=[],
        recordkeeping=False,
    )

    assert summary["required_points"] is None
    assert summary["needs_hsg"] is True

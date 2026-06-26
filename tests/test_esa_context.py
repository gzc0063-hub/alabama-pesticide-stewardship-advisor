from src.esa_context import (
    active_esa_products_for_crop,
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

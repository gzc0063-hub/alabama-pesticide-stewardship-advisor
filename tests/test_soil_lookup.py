from src.soil_lookup import (
    build_hsg_query,
    coordinates_in_alabama,
    lookup_hydrologic_soil_group,
    parse_hsg_response,
)


def test_coordinates_in_alabama_bounds():
    assert coordinates_in_alabama(32.6, -85.5) is True
    assert coordinates_in_alabama(36.0, -85.5) is False


def test_build_hsg_query_contains_point_coordinates():
    query = build_hsg_query(32.6, -85.5)

    assert "POINT(-85.5 32.6)" in query
    assert "hydgrp" in query


def test_parse_hsg_response_accepts_dict_table():
    hsg = parse_hsg_response({"Table": [{"hydgrpdcd": "b/d"}]})

    assert hsg == "B/D"


def test_lookup_hydrologic_soil_group_uses_usda_post(monkeypatch):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"Table": [{"hydgrpdcd": "C"}]}

    calls = {}

    def fake_post(url, data, timeout):
        calls["url"] = url
        calls["data"] = data
        calls["timeout"] = timeout
        return Response()

    monkeypatch.setattr("src.soil_lookup.requests.post", fake_post)

    result = lookup_hydrologic_soil_group(32.6, -85.5)

    assert result["hsg"] == "C"
    assert result["error"] is None
    assert calls["data"]["format"] == "JSON"

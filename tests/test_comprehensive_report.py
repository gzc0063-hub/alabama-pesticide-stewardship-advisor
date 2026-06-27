from src.comprehensive_report import build_comprehensive_report


def test_comprehensive_report_includes_pula_status_and_reason():
    report = build_comprehensive_report(
        lat=32.8067,
        lon=-86.7911,
        county="Autauga",
        crop_or_site="cotton",
        pula_summary={
            "distance_miles": 0.27,
            "pula_id": 121,
            "event_name": "Dicamba 2026",
            "codes": "DC125",
            "status": "effective",
            "effective_date": "2026-02-09",
        },
        pula_intersects=False,
        hsg="C",
        resistance_summaries=["Palmer amaranth: reported resistant to Group 9."],
    )

    assert "Selected point inside cached PULA:** No" in report
    assert "Dicamba 2026" in report
    assert "DC125" in report
    assert "2026-02-09" in report

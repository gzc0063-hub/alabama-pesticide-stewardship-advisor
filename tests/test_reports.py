import csv

from src.reports import (
    REPORT_COLUMNS,
    build_email_message,
    save_report,
    select_report_recipient,
)


def valid_report():
    return {
        "reporter_role": "Grower",
        "contact_name": "Test Reporter",
        "contact_phone": "334-555-0100",
        "contact_email": "reporter@example.com",
        "permission_to_contact": "yes",
        "county": "Lee",
        "location_description": "Field edge near county road",
        "crop_or_site": "Soybean",
        "suspected_weed": "Palmer amaranth",
        "herbicide_product": "Example product",
        "active_ingredient": "Example active",
        "site_of_action": "Group 15",
        "application_date": "2026-06-01",
        "application_rate": "Label rate",
        "survivor_pattern": "Patchy",
        "prior_herbicide_history": "Group 9 used previously",
        "weather_notes": "Warm and dry",
        "photo_paths": "",
    }


def test_report_columns_include_contact_and_agronomic_fields():
    assert "contact_email" in REPORT_COLUMNS
    assert "crop_or_site" in REPORT_COLUMNS
    assert "suspected_weed" in REPORT_COLUMNS
    assert "survivor_pattern" in REPORT_COLUMNS


def test_save_report_appends_private_csv(tmp_path):
    report_path = tmp_path / "suspected_resistance_reports.csv"
    saved_path = save_report(valid_report(), report_path=report_path)
    assert saved_path == report_path

    with report_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 1
    assert rows[0]["county"] == "Lee"
    assert rows[0]["suspected_weed"] == "Palmer amaranth"
    assert rows[0]["submission_status"] == "suspected"


def test_select_report_recipient_prefers_matching_specialty():
    contacts = [
        {
            "name": "Row Crop Specialist",
            "email": "row@example.com",
            "specialty_tags": "row crop;cotton;soybean",
        },
        {
            "name": "Forage Specialist",
            "email": "forage@example.com",
            "specialty_tags": "forage;pasture",
        },
    ]
    recipient = select_report_recipient("Soybean", contacts)
    assert recipient["email"] == "row@example.com"


def test_build_email_message_uses_suspected_language():
    message = build_email_message(valid_report(), {"email": "row@example.com"})
    assert "Suspected resistance report" in message["subject"]
    assert "not a confirmation" in message["body"]
    assert "Palmer amaranth" in message["body"]

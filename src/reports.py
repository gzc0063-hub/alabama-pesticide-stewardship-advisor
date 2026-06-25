import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPORT_COLUMNS = [
    "submitted_at_utc",
    "submission_status",
    "reporter_role",
    "contact_name",
    "contact_phone",
    "contact_email",
    "permission_to_contact",
    "county",
    "location_description",
    "crop_or_site",
    "suspected_weed",
    "herbicide_product",
    "active_ingredient",
    "site_of_action",
    "application_date",
    "application_rate",
    "survivor_pattern",
    "prior_herbicide_history",
    "weather_notes",
    "photo_paths",
]


def normalize_report(report: dict) -> dict:
    normalized = {column: str(report.get(column, "")).strip() for column in REPORT_COLUMNS}
    normalized["submitted_at_utc"] = datetime.now(timezone.utc).isoformat()
    normalized["submission_status"] = "suspected"
    return normalized


def save_report(
    report: dict,
    report_path: Path | str = "data/private/suspected_resistance_reports.csv",
) -> Path:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = normalize_report(report)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return path


def select_report_recipient(crop_or_site: str, contacts: Iterable[dict]) -> dict:
    query = crop_or_site.lower()
    fallback = None
    for contact in contacts:
        if fallback is None:
            fallback = contact
        tags = contact.get("specialty_tags", "").lower()
        if any(part.strip() and part.strip() in query for part in tags.split(";")):
            return contact
    return fallback or {"name": "Extension contact", "email": ""}


def build_email_message(report: dict, recipient: dict) -> dict:
    subject = f"Suspected resistance report: {report.get('suspected_weed', 'unknown weed')}"
    body = (
        "A suspected herbicide-resistance report was submitted through the "
        "PULA Awareness Tool. This is not a confirmation of resistance.\n\n"
        f"Recipient: {recipient.get('name', '')} <{recipient.get('email', '')}>\n"
        f"Reporter: {report.get('contact_name', '')} ({report.get('reporter_role', '')})\n"
        f"Email: {report.get('contact_email', '')}\n"
        f"Phone: {report.get('contact_phone', '')}\n"
        f"County: {report.get('county', '')}\n"
        f"Crop or site: {report.get('crop_or_site', '')}\n"
        f"Suspected weed: {report.get('suspected_weed', '')}\n"
        f"Herbicide product: {report.get('herbicide_product', '')}\n"
        f"Active ingredient: {report.get('active_ingredient', '')}\n"
        f"Site of action: {report.get('site_of_action', '')}\n"
        f"Survivor pattern: {report.get('survivor_pattern', '')}\n"
        f"Notes: {report.get('weather_notes', '')}\n"
    )
    return {"subject": subject, "body": body}

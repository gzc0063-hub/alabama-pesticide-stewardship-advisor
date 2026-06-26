import csv
from pathlib import Path


RESISTANCE_CONTEXT_PATH = Path("data/alabama_resistance_context.csv")


def load_alabama_resistance_context(
    path: Path | str = RESISTANCE_CONTEXT_PATH,
) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resistance_context_for_crop(crop_or_site: str, rows: list[dict]) -> list[dict]:
    query = str(crop_or_site).strip().lower()
    if not query:
        return rows
    matches = []
    for row in rows:
        tags = [tag.strip().lower() for tag in row.get("crop_tags", "").split(";")]
        if query in tags or any(query in tag or tag in query for tag in tags if tag):
            matches.append(row)
    return matches or rows


def summarize_resistance_records(rows: list[dict], limit: int = 6) -> list[str]:
    summaries = []
    for row in rows[:limit]:
        common = row.get("common_name", "Unknown weed")
        scientific = row.get("species", "")
        site = row.get("site_of_action", "unknown site of action")
        first_year = row.get("first_year", "")
        name = f"{common} ({scientific})" if scientific else common
        year_text = f", first reported {first_year}" if first_year else ""
        summaries.append(f"{name}: reported resistant to {site}{year_text}.")
    return summaries


def nearby_resistance_note() -> str:
    return (
        "Nearby field-level resistance reports are not available in this snapshot. "
        "The records shown are Alabama state-level reports from the International "
        "Herbicide-Resistant Weed Database, so they are context for scouting and "
        "Extension follow-up, not confirmation for this field."
    )

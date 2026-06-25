import csv
from pathlib import Path


CONTACT_COLUMNS = [
    "name",
    "role",
    "email",
    "phone",
    "specialty",
    "crop_focus",
    "specialty_tags",
    "source_url",
    "verified_as_of",
]


def load_contacts(path: Path | str = "data/extension_contacts_alabama.csv") -> list[dict]:
    contact_path = Path(path)
    if not contact_path.exists():
        return []
    with contact_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contacts_for_crop_or_site(
    crop_or_site: str,
    path: Path | str = "data/extension_contacts_alabama.csv",
) -> list[dict]:
    query = crop_or_site.lower()
    matches = []
    for contact in load_contacts(path):
        tags = contact.get("specialty_tags", "").lower().split(";")
        if any(tag.strip() and tag.strip() in query for tag in tags):
            matches.append(contact)
    return matches

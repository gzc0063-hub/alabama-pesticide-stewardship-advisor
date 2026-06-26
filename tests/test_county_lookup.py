from src.county_lookup import county_contact_links, normalize_county_name


def test_normalize_county_name_removes_county_suffix():
    assert normalize_county_name("Lee County") == "Lee"
    assert normalize_county_name("  Madison county  ") == "Madison"


def test_county_contact_links_builds_aces_urls():
    links = county_contact_links("Lee County")

    assert links["county"] == "Lee"
    assert links["office_url"] == "https://www.aces.edu/counties/lee"
    assert links["contact_url"] == "https://www.aces.edu/contact-extension/?office=Lee+County+Office"

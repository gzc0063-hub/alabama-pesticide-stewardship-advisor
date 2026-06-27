from src.disclaimers import (
    BLT_URL,
    PALM_URL,
    HEAP_CITATION,
    get_primary_disclaimer,
    get_result_disclaimer,
)


def test_primary_disclaimer_names_official_systems():
    text = get_primary_disclaimer()
    assert "not a compliance system" in text.lower()
    assert "label is the law" in text.lower()
    assert "Bulletins Live! Two" in text
    assert "PALM" in text
    assert "pesticide label" in text
    assert "24(c)" in text
    assert BLT_URL.startswith("https://")
    assert PALM_URL.startswith("https://")


def test_result_disclaimer_uses_cautious_language():
    text = get_result_disclaimer(cached_pula_found=False)
    assert "No cached PULA was found" in text
    assert "verify official requirements in EPA Bulletins Live! Two" in text
    assert "No PULA applies" not in text


def test_result_disclaimer_for_possible_intersection():
    text = get_result_disclaimer(cached_pula_found=True)
    assert "may intersect" in text
    assert "verify official requirements in EPA Bulletins Live! Two" in text
    assert "compliance" not in text.lower()


def test_heap_citation_is_present():
    assert "Heap" in HEAP_CITATION
    assert "weedscience.org" in HEAP_CITATION

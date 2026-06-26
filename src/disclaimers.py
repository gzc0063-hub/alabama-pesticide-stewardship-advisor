BLT_URL = "https://www.epa.gov/endangered-species/bulletins-live-two-view-bulletins"
PALM_URL = "https://www.epa.gov/pesticides/mitigation-menu"
HEAP_URL = "https://www.weedscience.org/Summary/Country.aspx?CountryID=45"
HEAP_CITATION = (
    "Heap, I. The International Herbicide-Resistant Weed Database. "
    "www.weedscience.org."
)


def get_primary_disclaimer() -> str:
    return (
        "The PULA Awareness Tool is an educational planning tool, not a "
        "compliance system. It does not replace EPA Bulletins Live! Two, "
        "EPA PALM, pesticide label requirements, state or local restrictions, "
        "or guidance from Extension professionals."
    )


def get_result_disclaimer(cached_pula_found: bool) -> str:
    if cached_pula_found:
        return (
            "A cached PULA polygon may intersect this point. Verify in EPA "
            "Bulletins Live! Two for your product, location, and application "
            "month before applying."
        )
    return (
        "No cached PULA was found in this educational snapshot. Verify in EPA "
        "Bulletins Live! Two for your product, location, and application month "
        "before applying."
    )


def get_resistance_disclaimer() -> str:
    return "Reported records only; not field confirmation."

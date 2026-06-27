from pathlib import Path
import base64
import json

import folium
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

from src.county_lookup import county_contact_links, county_from_coordinates
from src.data_epa import (
    load_pula_geojson,
    load_snapshot_metadata,
    nearest_pula_summary,
    pula_snapshot_summary,
    validate_metadata,
)
from src.data_heap import heap_attribution
from src.disclaimers import (
    BLT_URL,
    HEAP_URL,
    EDDMAPS_URL,
    PALM_URL,
    get_primary_disclaimer,
    get_resistance_disclaimer,
    get_result_disclaimer,
)
from src.esa_context import (
    LABEL_COVERAGE_NOTE,
    MITIGATION_PRACTICES,
    build_mitigation_report,
    calculate_mitigation_summary,
    county_mitigation_context,
    herbicide_products_for_crop,
)
from src.extension_contacts import contacts_for_crop_or_site, load_contacts
from src.pdf_report import build_text_pdf
from src.reports import (
    build_email_message,
    save_report,
    select_report_recipient,
    send_email_notification,
)
from src.resistance_context import (
    load_alabama_resistance_context,
    nearby_resistance_note,
    resistance_context_for_crop,
    summarize_resistance_records,
)
from src.soil_lookup import lookup_hydrologic_soil_group
from src.spatial import point_in_polygons
from src.comprehensive_report import build_comprehensive_report


st.set_page_config(page_title="LookAround", layout="wide")

PULA_FULL_PATH = Path("data/pula_alabama.geojson")
PULA_DISPLAY_PATH = Path("data/pula_alabama_display.geojson")
ASSETS_DIR = Path("assets")
AU_LOGO_PATH = ASSETS_DIR / "auburn-logo.png"
ACES_LOGO_PATH = ASSETS_DIR / "aces-logo.png"
ACES_COUNTIES_URL = "https://www.aces.edu/counties/"
ACES_DIRECTORY_URL = "https://ssl.acesag.auburn.edu/directory-new/programAgentSearch.php?program=1"
ALABAMA_MAP_BOUNDS = [[30.1, -88.55], [35.05, -84.85]]
ALABAMA_MAP_CENTER = [32.8067, -86.7911]
CROP_SITE_OPTIONS = [
    "",
    "Cotton",
    "Soybean",
    "Corn",
    "Peanut",
    "Pasture",
    "Forage",
    "Turf",
    "Right-of-way",
    "Aquatic site",
    "Forestry",
    "Other",
]

DEFAULT_LAT = 32.8067
DEFAULT_LON = -86.7911


def get_selected_location() -> tuple[float | None, float | None]:
    lat = st.session_state.get("selected_lat")
    lon = st.session_state.get("selected_lon")
    if lat is None or lon is None:
        return None, None
    return float(lat), float(lon)


def set_selected_location(lat: float, lon: float, source: str) -> None:
    st.session_state["selected_lat"] = float(lat)
    st.session_state["selected_lon"] = float(lon)
    st.session_state["selected_location_source"] = source


def pula_meaning_text(nearest: dict | None, intersects: bool | None) -> str:
    if not nearest:
        return "No cached PULA feature is available for this location snapshot."
    event = nearest.get("event_name") or "an EPA PULA event"
    distance = nearest.get("distance_miles")
    distance_text = f"{distance:.2f} miles away" if isinstance(distance, (int, float)) else "nearby"
    if intersects:
        return (
            f"The selected point appears inside a cached PULA for {event}. "
            "This means EPA BLT may list product-, timing-, or site-specific limitations here."
        )
    return (
        f"The nearest cached PULA is {distance_text} and is tied to {event}. "
        "It does not automatically mean your field is restricted, but it tells you what to verify in BLT."
    )


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
          --auburn-navy: #0c2340;
          --auburn-orange: #dd550c;
          --auburn-blue: #1b365d;
          --ink: #152238;
          --muted: #667085;
          --line: #d9e1ea;
          --wash: #f5f7fa;
        }
        .block-container {
          padding-top: 1.4rem;
          padding-bottom: 2rem;
          max-width: 1440px;
        }
        div[data-testid="stAppViewContainer"] {
          background: linear-gradient(180deg, #ffffff 0%, #f6f8fb 58%, #ffffff 100%);
        }
        h1, h2, h3 {
          color: var(--auburn-navy);
          letter-spacing: 0;
        }
        .au-hero {
          background: linear-gradient(135deg, #0c2340 0%, #14365f 72%, #1b365d 100%);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 8px;
          padding: 22px 26px;
          color: white;
          box-shadow: 0 18px 45px rgba(12,35,64,.18);
          margin-bottom: 18px;
        }
        .au-brand-row {
          display:flex;
          justify-content:space-between;
          gap:18px;
          align-items:center;
        }
        .au-title {
          font-size: 34px;
          line-height: 1.1;
          font-weight: 760;
          margin: 0 0 8px 0;
        }
        .au-subtitle {
          color: #dce7f3;
          font-size: 15px;
          max-width: 840px;
        }
        .au-lockup {
          display:flex;
          flex-direction: column;
          gap: 9px;
          align-items:center;
          min-width: 250px;
          justify-content:flex-end;
        }
        .logo-card {
          border-radius: 8px;
          display:flex;
          align-items:center;
          justify-content:center;
          width: 210px;
          min-height: 48px;
          padding: 9px 12px;
        }
        .logo-card.auburn {
          border: 1px solid rgba(255,255,255,.25);
          background: rgba(255,255,255,.05);
        }
        .logo-card.aces {
          border: 1px solid rgba(255,255,255,.58);
          background: rgba(255,255,255,.96);
        }
        .logo-card img {
          max-width: 100%;
          max-height: 44px;
          display:block;
        }
        .au-accent {
          width: 46px;
          height: 4px;
          border-radius: 3px;
          background: var(--auburn-orange);
          margin-top: 14px;
        }
        .metric-strip {
          display:grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 10px;
          margin: 10px 0 12px;
        }
        .metric-tile {
          background: white;
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 13px 14px;
        }
        .metric-label {
          color: var(--muted);
          font-size: 12px;
          text-transform: uppercase;
          font-weight: 700;
        }
        .metric-value {
          color: var(--auburn-navy);
          font-size: 22px;
          font-weight: 780;
          margin-top: 4px;
        }
        .panel {
          background: white;
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 16px 17px;
          box-shadow: 0 12px 30px rgba(12,35,64,.08);
          margin-bottom: 14px;
        }
        .panel-title {
          color: var(--auburn-navy);
          font-weight: 760;
          font-size: 16px;
          margin-bottom: 6px;
        }
        .soft-note {
          color: var(--muted);
          font-size: 13px;
          line-height: 1.45;
        }
        .info-grid {
          display:grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 10px;
          margin: 0 0 12px;
        }
        .info-cell {
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 12px;
          background: #fbfcfe;
        }
        .info-kicker {
          color: var(--auburn-orange);
          font-size: 12px;
          font-weight: 800;
          text-transform: uppercase;
        }
        .report-cta {
          border: 1px solid #bf4b0a;
          border-radius: 8px;
          padding: 15px;
          background: #fff7f1;
          margin-bottom: 14px;
        }
        .contact-card {
          border-top: 1px solid var(--line);
          padding: 10px 0;
        }
        .contact-name {
          color: var(--auburn-navy);
          font-weight: 760;
        }
        .contact-meta {
          color: var(--muted);
          font-size: 13px;
        }
        div.stButton > button, div.stDownloadButton > button {
          border-radius: 8px;
          border: 1px solid #bf4b0a;
          background: #dd550c;
          color: white;
          font-weight: 700;
        }
        div.stButton > button:hover {
          border-color: #0c2340;
          background: #c64d0b;
          color: white;
        }
        div[data-testid="stAlert"] {
          border-radius: 8px;
        }
        .resource-strip {
          display:grid;
          grid-template-columns: repeat(6, minmax(0, 1fr));
          gap: 12px;
          margin: 12px 0 14px;
        }
        .resource-link {
          display:flex;
          align-items:center;
          justify-content:center;
          min-height: 44px;
          border: 1px solid #c9d3df;
          border-radius: 8px;
          background: #ffffff;
          color: var(--auburn-navy) !important;
          text-decoration: none !important;
          font-weight: 650;
          text-align:center;
          padding: 8px 10px;
          box-shadow: 0 1px 2px rgba(12,35,64,.04);
        }
        .resource-link:hover {
          border-color: var(--auburn-orange);
          color: var(--auburn-orange) !important;
        }
        div[data-testid="stIFrame"] iframe {
          border: 1px solid var(--line);
          border-radius: 8px;
          box-shadow: 0 10px 24px rgba(12,35,64,.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_display_geojson(path: str) -> dict | None:
    display_path = Path(path)
    if not display_path.exists():
        return None
    return json.loads(display_path.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_pulas(path: str):
    if not Path(path).exists():
        return None
    return load_pula_geojson(path)


@st.cache_data(show_spinner=False)
def load_resistance_rows() -> list[dict]:
    return load_alabama_resistance_context()


@st.cache_data(show_spinner=False)
def cached_soil_lookup(lat: float, lon: float) -> dict:
    return lookup_hydrologic_soil_group(lat, lon)


def smtp_settings_from_secrets() -> dict | None:
    try:
        if "smtp" not in st.secrets:
            return None
        smtp = st.secrets["smtp"]
    except StreamlitSecretNotFoundError:
        return None
    return {
        "host": smtp.get("host"),
        "port": smtp.get("port"),
        "username": smtp.get("username"),
        "password": smtp.get("password"),
        "sender": smtp.get("sender"),
        "recipient": smtp.get("recipient"),
    }


def set_view(view: str) -> None:
    st.session_state["view"] = view


@st.cache_data(show_spinner=False)
def image_data_uri(path: str) -> str:
    file_path = Path(path)
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_header(metadata: dict, summary: dict) -> None:
    auburn_logo = image_data_uri(str(AU_LOGO_PATH)) if AU_LOGO_PATH.exists() else ""
    aces_logo = image_data_uri(str(ACES_LOGO_PATH)) if ACES_LOGO_PATH.exists() else ""
    auburn_markup = (
        f'<img src="{auburn_logo}" alt="Auburn University logo">'
        if auburn_logo
        else "Auburn"
    )
    aces_markup = (
        f'<img src="{aces_logo}" alt="Alabama Cooperative Extension System logo">'
        if aces_logo
        else "ACES"
    )
    st.markdown(
        f"""
        <div class="au-hero">
          <div class="au-brand-row">
            <div style="display: flex; gap: 20px; align-items: center;">
              <svg width="64" height="64" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Outer magnifying glass / compass ring -->
                <circle cx="50" cy="45" r="35" fill="none" stroke="#dd550c" stroke-width="8"/>
                <!-- Magnifying glass handle -->
                <line x1="75" y1="70" x2="90" y2="85" stroke="#dd550c" stroke-width="10" stroke-linecap="round"/>
                <!-- Map Pin inner -->
                <path d="M50 25 C41 25, 34 32, 34 41 C34 52, 50 63, 50 63 C50 63, 66 52, 66 41 C66 32, 59 25, 50 25 Z" fill="#ffffff"/>
                <!-- Pin dot -->
                <circle cx="50" cy="38" r="6" fill="#1b365d"/>
              </svg>
              <div>
                <div class="au-title">LookAround</div>
                <div class="au-subtitle">
                  Alabama-focused pesticide limitation awareness with resistance context and Extension routing.
                  Official compliance decisions still belong in EPA Bulletins Live! Two.
                </div>
                <div class="au-accent"></div>
              </div>
            </div>
            <div class="au-lockup">
              <div class="logo-card auburn">{auburn_markup}</div>
              <div class="logo-card aces">{aces_markup}</div>
            </div>
          </div>
        </div>
        <div class="metric-strip">
          <div class="metric-tile"><div class="metric-label">Cached PULA features</div><div class="metric-value">{summary.get("feature_count", 0)}</div></div>
          <div class="metric-tile"><div class="metric-label">PULA snapshot</div><div class="metric-value">{metadata.get("pula_date", "unverified")}</div></div>
          <div class="metric-tile"><div class="metric-label">Scope</div><div class="metric-value">Alabama</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.warning(get_primary_disclaimer())


def render_links() -> None:
    links = [
        (
            "EPA BLT",
            BLT_URL,
            "EPA Bulletins Live! Two: verify product, location, and application-month pesticide limitations.",
        ),
        (
            "EPA PALM",
            PALM_URL,
            "EPA pesticide mitigation menu: review runoff, erosion, and spray-drift mitigation options.",
        ),
        (
            "weedscience.org",
            HEAP_URL,
            "International Herbicide-Resistant Weed Database: source for reported resistance records.",
        ),
        (
            "EDDMapS",
            EDDMAPS_URL,
            "EDDMapS distribution maps: reported weed and invasive species occurrence context.",
        ),
        (
            "ACES Counties",
            ACES_COUNTIES_URL,
            "Find your local Alabama Cooperative Extension county office.",
        ),
        (
            "ACES Directory",
            ACES_DIRECTORY_URL,
            "Search ACES agents and specialists by program area.",
        ),
    ]
    markup = '<div class="resource-strip">'
    for label, url, tooltip in links:
        markup += (
            f'<a class="resource-link" href="{url}" target="_blank" '
            f'rel="noopener noreferrer" title="{tooltip}">{label}</a>'
        )
    markup += "</div>"
    st.markdown(markup, unsafe_allow_html=True)


def add_pula_layer(m: folium.Map, display_geojson: dict | None) -> None:
    if not display_geojson:
        return
    folium.GeoJson(
        display_geojson,
        name="Cached Alabama PULAs",
        style_function=lambda _: {
            "fillColor": "#dd550c",
            "color": "#8a3a08",
            "weight": 1.2,
            "fillOpacity": 0.32,
        },
        highlight_function=lambda _: {
            "fillColor": "#ff8a3d",
            "color": "#0c2340",
            "weight": 2,
            "fillOpacity": 0.5,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["pula_id", "event_name", "status"],
            aliases=["PULA ID", "Event", "Status"],
            sticky=False,
        ),
    ).add_to(m)


def add_selected_location_layer(
    m: folium.Map,
    lat: float | None,
    lon: float | None,
    pulas,
    nearest: dict | None,
) -> None:
    if lat is None or lon is None:
        return
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color="#0c2340",
        weight=3,
        fill=True,
        fill_color="#dd550c",
        fill_opacity=0.95,
        tooltip="Selected field/location",
    ).add_to(m)
    folium.Marker(
        location=[lat, lon],
        tooltip=f"Selected location: {lat:.5f}, {lon:.5f}",
    ).add_to(m)
    if pulas is None or not nearest or not nearest.get("pula_id"):
        return
    matched = pulas[pulas["pula_id"] == nearest["pula_id"]]
    if matched.empty:
        return
    centroid = matched.geometry.iloc[0].centroid
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=10,
        color="#0c2340",
        weight=3,
        fill=True,
        fill_color="#1b365d",
        fill_opacity=0.72,
        tooltip=(
            f"Nearest cached PULA {nearest.get('pula_id', '')}: "
            f"{nearest.get('event_name', '')}"
        ),
    ).add_to(m)
    folium.PolyLine(
        locations=[[lat, lon], [centroid.y, centroid.x]],
        color="#0c2340",
        weight=2,
        opacity=0.7,
        dash_array="8,6",
        tooltip="Selected location to nearest cached PULA",
    ).add_to(m)


def render_report_cta() -> None:
    st.markdown(
        """
        <div class="report-cta">
          <div class="panel-title">Report Suspected Herbicide Resistance</div>
          <div class="soft-note">
            Use this when a weed population survives an appropriate application and you want Extension follow-up.
            The report is saved as a private CSV record and can notify the appropriate specialist when email is configured.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button("Report suspected resistance", on_click=set_view, args=("report",))


def render_map_context() -> None:
    st.markdown(
        """
        <div class="info-grid">
          <div class="info-cell">
            <div class="info-kicker">PULA</div>
            <div class="soft-note">
              A Pesticide Use Limitation Area is an EPA geography where BLT may add pesticide use limits for listed species or critical habitat.
            </div>
          </div>
          <div class="info-cell">
            <div class="info-kicker">Why Alabama</div>
            <div class="soft-note">
              Alabama's crops, aquatic systems, and protected-species habitats make field-level bulletin checks important before application.
            </div>
          </div>
          <div class="info-cell">
            <div class="info-kicker">Crop or Site</div>
            <div class="soft-note">
              The crop/site box helps route you to relevant Auburn/ACES specialists and filters resistance and ESA
              planning context for crops such as cotton, soybean, corn, pasture, or rights-of-way.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def location_result(lat: float, lon: float, pulas) -> tuple[bool, dict | None]:
    if pulas is None:
        return False, None
    intersects = not point_in_polygons(lat, lon, pulas).empty
    return intersects, nearest_pula_summary(lat, lon, pulas)


def selected_county(lat: float | None, lon: float | None) -> str | None:
    if lat is None or lon is None:
        return None
    try:
        return county_from_coordinates(lat, lon)
    except Exception:
        return None


def render_result_panel(lat: float | None, lon: float | None, pulas) -> None:
    st.markdown('<div class="panel"><div class="panel-title">Step 1: PULA Meaning for This Location</div>', unsafe_allow_html=True)
    if lat is None or lon is None:
        st.markdown(
            '<div class="soft-note">Enter coordinates, use browser location, or click the map. The selected point and nearest cached PULA will be highlighted on the map.</div></div>',
            unsafe_allow_html=True,
        )
        return

    intersects, nearest = location_result(lat, lon, pulas)
    st.info(get_result_disclaimer(cached_pula_found=intersects))
    st.markdown(f"**Plain-language meaning:** {pula_meaning_text(nearest, intersects)}")
    if intersects:
        st.error("This selected point appears to fall inside at least one cached Alabama-intersecting PULA polygon. Treat this as a prompt to verify the exact product, month, and use site in EPA BLT.")
    st.write(f"Location checked: `{lat:.5f}, {lon:.5f}`")
    if nearest:
        st.metric("Nearest cached PULA distance", f"{nearest['distance_miles']:.2f} miles")
        st.write(f"**Nearest PULA ID:** {nearest.get('pula_id', '')}")
        if nearest.get("event_name"):
            st.write(f"**Event:** {nearest['event_name']}")
            st.caption("The event name is EPA source metadata describing why the PULA polygon exists in the cached layer.")
        if nearest.get("codes"):
            st.write(f"**PULA reason/codes:** {nearest['codes']}")
            st.caption("Codes are EPA bulletin/source codes. They must be interpreted in the current BLT bulletin for the exact product and application month.")
        if nearest.get("status"):
            st.write(f"**Status:** {nearest['status']}")
        if nearest.get("effective_date"):
            st.write(f"**Effective date:** {nearest['effective_date']}")
        if nearest.get("published_time_stamp"):
            st.write(f"**Published:** {nearest['published_time_stamp']}")
    st.link_button("Verify this location in EPA BLT", BLT_URL)
    st.markdown("</div>", unsafe_allow_html=True)


def render_contacts(crop_or_site: str) -> None:
    st.markdown('<div class="panel"><div class="panel-title">Local Extension Support</div>', unsafe_allow_html=True)
    st.caption("Open only when you need specialist names and official ACES profile links.")
    with st.expander("Show Extension specialists"):
        matching_contacts = contacts_for_crop_or_site(crop_or_site) if crop_or_site else load_contacts()
        for contact in matching_contacts[:5]:
            st.markdown(
                f"""
                <div class="contact-card">
                  <div class="contact-name">{contact.get('name', '')}</div>
                  <div class="contact-meta">{contact.get('role', '')}</div>
                  <div class="contact-meta">{contact.get('specialty', '')}</div>
                  <div class="contact-meta">{contact.get('phone', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if contact.get("source_url"):
                st.link_button(f"Official profile: {contact.get('name', 'contact')}", contact["source_url"])
        st.caption("Email addresses are shown through official ACES profile pages when ACES exposes them.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_county_support(county: str | None) -> None:
    st.markdown('<div class="panel"><div class="panel-title">County Extension Office</div>', unsafe_allow_html=True)
    st.caption("Open if you need the responsible local county office.")
    with st.expander("Show county office"):
        st.caption("Location-to-county lookup uses the U.S. Census geocoder and sends only the selected coordinates.")
        if county:
            links = county_contact_links(county)
            st.write(f"**Responsible county office:** {links['county']} County")
            county_cols = st.columns(2)
            county_cols[0].link_button("County office page", links["office_url"])
            county_cols[1].link_button("Contact county office", links["contact_url"])
        else:
            st.write("Choose a location to identify the nearest county Extension office.")
            st.link_button("Find your county office", ACES_COUNTIES_URL)
    st.markdown("</div>", unsafe_allow_html=True)


def render_resistance_context(crop_or_site: str, lat: float | None, lon: float | None) -> None:
    rows = load_resistance_rows()
    matching_rows = resistance_context_for_crop(crop_or_site, rows)
    st.markdown(
        f"""
        <div class="panel">
          <div class="panel-title">Nearby Herbicide Resistance Context</div>
          <div class="soft-note">{get_resistance_disclaimer()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(heap_attribution())
    st.markdown(
        """
        <div class="report-cta">
          <div class="panel-title">Reviewer Note</div>
          <div class="soft-note">
            This section can be improved as finer-scale Alabama resistance observations and Auburn/ACES weed science
            guidance become available. Especially with a review from Dr. Scott McElroy, our resident
            <strong>malherbologist</strong>.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Show resistance records and notes"):
        if lat is not None and lon is not None:
            st.write(f"Location checked for context: `{lat:.5f}, {lon:.5f}`")
        st.info(nearby_resistance_note())
        for line in summarize_resistance_records(matching_rows, limit=5):
            st.write(f"- {line}")
        if crop_or_site and matching_rows == rows:
            st.caption("No exact crop/site tag match was found, so the statewide Alabama resistance context is shown.")
        st.link_button("Open weedscience.org source", HEAP_URL)
    st.markdown("</div>", unsafe_allow_html=True)


def render_eddmaps_context(lat: float | None, lon: float | None) -> None:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-title">Nearby Weed / Invasive Occurrence Context</div>
          <div class="soft-note">EDDMapS reported occurrence context; not field confirmation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Source: EDDMapS distribution maps, University of Georgia Center for Invasive Species and Ecosystem Health.")
    with st.expander("Show EDDMapS context"):
        radius = st.radio(
            "Review radius",
            ["1 mile", "5 miles", "10 miles"],
            horizontal=True,
            help="1 mile is the default field-neighborhood view; broaden only if no useful context is available.",
        )
        if lat is not None and lon is not None:
            st.write(f"Selected location: `{lat:.5f}, {lon:.5f}`")
            st.info(
                f"This review placeholder is set to {radius}. EDDMapS does not currently expose a verified proximity endpoint in this app, so the app is not automatically listing invasive plant/species records yet. A future integration should show the nearest public EDDMapS occurrence records within this radius when a reliable endpoint or approved dataset is available."
            )
            # Add a dynamic link to EDDMapS distribution map if lat/lon is available.
            # While EDDMaps doesn't have a simple URL scheme for point radius, we can explain how to use the site.
            st.write("**Extension Note:** When using EDDMapS, search your county to see what invasive weeds have been reported locally.")
        else:
            st.write("Choose a location to prepare the EDDMapS proximity review.")
        st.write(
            "Use this as weed/invasive occurrence context only. EDDMapS reports do not confirm a species is present in the selected field and do not confirm herbicide resistance."
        )
        st.link_button("Open EDDMapS distribution maps", EDDMAPS_URL)
    st.markdown("</div>", unsafe_allow_html=True)


def render_esa_context(
    county: str | None,
    lat: float | None,
    lon: float | None,
    pula_intersects: bool | None,
    nearest_pula: dict | None,
) -> str:
    st.markdown('<div class="panel"><div class="panel-title">ESA Mitigation Point Calculator</div>', unsafe_allow_html=True)
    st.caption("Step 2 after location/PULA review. Choose a crop/site only if you want product-specific ESA planning.")
    crop_choice = st.selectbox(
        "Crop or managed site for this ESA decision",
        CROP_SITE_OPTIONS,
        format_func=lambda value: "Skip ESA crop/product planning" if value == "" else value,
        key="crop_or_site",
    )
    crop_or_site = crop_choice.lower()
    if crop_choice == "Other":
        crop_or_site = st.text_input(
            "Enter other crop or managed site",
            placeholder="Example: roadside, nursery, specialty crop",
            key="crop_or_site_other",
        ).strip().lower()
    st.caption(
        "Crop/site selection filters product examples, resistance context, reports, and Auburn/ACES contacts. "
        "You can still download a location/PULA report without choosing a crop."
    )
    if county:
        context = county_mitigation_context(county)
        if context:
            st.write(
                f"**{context['county']} County runoff vulnerability:** "
                f"{context['runoff_vulnerability']} | county relief points: {context['county_relief_points']}"
            )
    else:
        st.write("Choose a location to show county runoff-vulnerability context from the Alabama ESA calculator.")

    auto_hsg = "Unknown"

    products = herbicide_products_for_crop(crop_or_site)
    product_name = None
    hsg = "Unknown"
    selected_ids = []
    recordkeeping = False
    if not crop_or_site:
        st.info("Enter a crop/site above if you want the mitigation point calculator.")
    elif not products:
        st.write("No herbicide product example in the integrated calculator matched this crop/site.")
    else:
        if lat is not None and lon is not None:
            with st.spinner("Checking USDA soil survey for hydrologic soil group..."):
                soil_result = cached_soil_lookup(round(float(lat), 6), round(float(lon), 6))
            if soil_result.get("hsg"):
                auto_hsg = soil_result["hsg"]
                st.session_state["last_hsg"] = auto_hsg
                st.success(f"USDA Soil Data Access HSG lookup: {auto_hsg}")
            elif soil_result.get("error"):
                st.caption(f"USDA HSG lookup: {soil_result['error']}")
        st.info(LABEL_COVERAGE_NOTE)
        product_name = st.selectbox(
            "Herbicide product for ESA planning",
            [product["name"] for product in products],
            format_func=lambda name: (
                f"{name} - active point calculator"
                if next(
                    product for product in products if product["name"] == name
                )["esa_status"]
                == "active"
                else f"{name} - verify label/BLT"
            ),
        )
        selected_product = next(product for product in products if product["name"] == product_name)
        is_active_esa = selected_product.get("esa_status") == "active"
        st.write(
            f"**{selected_product['name']}** | AI: {selected_product['active_ingredient']} | "
            f"Group {selected_product['group']} | EPA Reg. {selected_product['epa_reg']}"
        )
        if is_active_esa:
            st.caption(
                f"Runoff target: {selected_product['runoff_points']} | "
                f"Downwind buffer: {selected_product['downwind_buffer_ft']} ft. {selected_product['note']}"
            )
        else:
            st.warning(
                "This product is included for planning awareness, but this app does not have a verified active "
                "Herbicide Strategy point target for it. Check the current product label, EPA BLT, and EPA PALM "
                "before deciding whether runoff points, buffers, or other restrictions apply."
            )
            st.caption(selected_product["note"])
        hsg_options = ["Unknown", "A", "B", "C", "D", "A/D", "B/D", "C/D"]
        hsg_index = hsg_options.index(auto_hsg) if auto_hsg in hsg_options else 0
        hsg = st.selectbox(
            "Hydrologic soil group",
            hsg_options,
            index=hsg_index,
            help="Required for Enlist products because the runoff point target changes by HSG.",
        )
        if auto_hsg != "Unknown":
            st.caption("Prefilled from USDA Soil Data Access using the selected coordinates; adjust if you have better field-specific soil information.")
        practice_labels = {
            practice["id"]: f"{practice['name']} (+{practice['points']})"
            for practice in MITIGATION_PRACTICES
            if practice["id"] != "recordkeeping"
        }
        selected_ids = st.multiselect(
            "Mitigation practices planned",
            options=list(practice_labels),
            format_func=lambda practice_id: practice_labels[practice_id],
        )
        recordkeeping = st.checkbox(
            "Maintain mitigation records with spray records (+1 point)",
            value=True,
        )
        summary = calculate_mitigation_summary(
            county=county,
            product_name=product_name,
            hsg=hsg,
            selected_practice_ids=selected_ids,
            recordkeeping=recordkeeping,
        )
        if summary["needs_label_verification"]:
            metric_cols = st.columns(2)
            metric_cols[0].metric("Known point target", "Verify")
            metric_cols[1].metric("Planning points selected", summary["total_points"])
            st.info(
                "Use the selected practices as a worksheet only. The final decision depends on the exact label, "
                "EPA Bulletins Live! Two, and EPA PALM for the product and application site."
            )
        else:
            metric_cols = st.columns(3)
            metric_cols[0].metric(
                "Required",
                "Needs HSG" if summary["required_points"] is None else summary["required_points"],
            )
            metric_cols[1].metric("Entered points", summary["total_points"])
            metric_cols[2].metric("County relief", summary["county_relief_points"])
            if summary["needs_hsg"]:
                st.warning("Choose a hydrologic soil group to calculate Enlist runoff points.")
            elif summary["meets_points"]:
                st.success("The entered planning practices meet or exceed the selected product's point target.")
            else:
                st.warning("The entered planning practices do not meet the selected product's point target yet.")

    if product_name:
        report = build_mitigation_report(
            lat,
            lon,
            county,
            crop_or_site,
            product_name=product_name,
            hsg=hsg,
            selected_practice_ids=selected_ids,
            recordkeeping=recordkeeping,
            pula_intersects=pula_intersects,
            nearest_pula=nearest_pula,
        )
        pdf_report = build_text_pdf(report, "ESA Mitigation Planning Report")
        st.download_button(
            "Download mitigation planning PDF",
            data=pdf_report,
            file_name="esa-mitigation-planning-report.pdf",
            mime="application/pdf",
        )
    else:
        st.caption("The mitigation report will appear after you enter a crop/site and select a product.")
    with st.expander("Show source calculator link"):
        st.link_button("Open Alabama ESA calculator", "https://gzc0063-hub.github.io/alabama-esa-calculator")
    st.markdown("</div>", unsafe_allow_html=True)
    return crop_or_site


def render_report_form() -> None:
    st.markdown(
        """
        <div class="au-hero">
          <div class="au-title">Report Suspected Resistance</div>
          <div class="au-subtitle">
            Submit a suspected case for Extension follow-up. This is not a confirmation of herbicide resistance.
          </div>
          <div class="au-accent"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button("Back to map", on_click=set_view, args=("map",))

    st.caption("Submissions are suspected cases only and are not confirmations of resistance.")
    with st.form("suspected_resistance_report"):
        col_a, col_b = st.columns(2)
        with col_a:
            reporter_role = st.selectbox(
                "Reporter role",
                ["Grower", "Consultant", "Extension agent", "Applicator", "Researcher", "Other"],
            )
            contact_name = st.text_input("Contact name")
            contact_phone = st.text_input("Contact phone")
            contact_email = st.text_input("Contact email")
            county = st.text_input("County")
            crop_or_site_report = st.text_input("Crop or managed site for this report")
            suspected_weed = st.text_input("Suspected weed species")
        with col_b:
            herbicide_product = st.text_input("Herbicide product")
            active_ingredient = st.text_input("Active ingredient, if known")
            site_of_action = st.text_input("Site of action/group, if known")
            application_date = st.text_input("Application date")
            application_rate = st.text_input("Application rate")
            survivor_pattern = st.selectbox(
                "Surviving weed pattern",
                ["Unknown", "Patchy", "Widespread", "Field-wide", "Along edges", "Other"],
            )
        permission_to_contact = st.checkbox(
            "I give Extension permission to contact me about this suspected case."
        )
        location_description = st.text_area("Field or location description")
        prior_herbicide_history = st.text_area("Prior herbicide history, if known")
        weather_notes = st.text_area("Weather or application notes")
        submitted = st.form_submit_button("Submit suspected resistance report")

    if submitted:
        report = {
            "reporter_role": reporter_role,
            "contact_name": contact_name,
            "contact_phone": contact_phone,
            "contact_email": contact_email,
            "permission_to_contact": "yes" if permission_to_contact else "no",
            "county": county,
            "location_description": location_description,
            "crop_or_site": crop_or_site_report,
            "suspected_weed": suspected_weed,
            "herbicide_product": herbicide_product,
            "active_ingredient": active_ingredient,
            "site_of_action": site_of_action,
            "application_date": application_date,
            "application_rate": application_rate,
            "survivor_pattern": survivor_pattern,
            "prior_herbicide_history": prior_herbicide_history,
            "weather_notes": weather_notes,
            "photo_paths": "",
        }
        saved_path = save_report(report)
        contacts = load_contacts()
        recipient = select_report_recipient(crop_or_site_report, contacts)
        message = build_email_message(report, recipient)
        email_sent = send_email_notification(message, smtp_settings_from_secrets())
        st.success(f"Report saved to {Path(saved_path).name}.")
        if email_sent:
            st.success("Email notification sent.")
        else:
            st.info("Email notification is not configured. The report was saved for follow-up.")


def render_main_app() -> None:
    metadata = load_snapshot_metadata()
    pulas = load_pulas(str(PULA_FULL_PATH))
    display_geojson = load_display_geojson(str(PULA_DISPLAY_PATH))
    summary = pula_snapshot_summary(pulas) if pulas is not None else {}
    selected_lat, selected_lon = get_selected_location()
    pula_intersects, nearest_pula = (
        location_result(selected_lat, selected_lon, pulas)
        if selected_lat is not None and selected_lon is not None
        else (None, None)
    )
    county = selected_county(selected_lat, selected_lon)

    render_header(metadata if validate_metadata(metadata) else {}, summary)
    render_links()

    location = None
    left, right = st.columns([1.8, 1], gap="large")

    with left:
        st.markdown('<div class="panel"><div class="panel-title">Alabama Cached PULA Map</div>', unsafe_allow_html=True)
        render_map_context()
        m = folium.Map(
            location=ALABAMA_MAP_CENTER,
            zoom_start=7,
            tiles="CartoDB positron",
            min_zoom=6,
            max_zoom=12,
            min_lat=ALABAMA_MAP_BOUNDS[0][0],
            max_lat=ALABAMA_MAP_BOUNDS[1][0],
            min_lon=ALABAMA_MAP_BOUNDS[0][1],
            max_lon=ALABAMA_MAP_BOUNDS[1][1],
            max_bounds=True,
            control_scale=True,
            prefer_canvas=True,
            zoom_control="topright",
        )
        m.fit_bounds(ALABAMA_MAP_BOUNDS)
        add_pula_layer(m, display_geojson)
        add_selected_location_layer(m, selected_lat, selected_lon, pulas, nearest_pula)
        folium.LayerControl(collapsed=True).add_to(m)
        map_state = st_folium(
            m,
            height=500,
            use_container_width=True,
            returned_objects=["last_clicked"],
            key="alabama_pula_map",
        )
        st.caption("Map is bounded to Alabama for faster navigation. Orange regions are cached EPA PULA polygons intersecting Alabama; always verify official requirements in BLT.")
        st.markdown("</div>", unsafe_allow_html=True)

    clicked = map_state.get("last_clicked") if map_state else None
    if clicked and clicked.get("lat") is not None and clicked.get("lng") is not None:
        clicked_lat = float(clicked["lat"])
        clicked_lon = float(clicked["lng"])
        if clicked_lat != selected_lat or clicked_lon != selected_lon:
            set_selected_location(clicked_lat, clicked_lon, "map click")
            st.rerun()

    with right:
        st.markdown('<div class="panel"><div class="panel-title">Check a Location</div>', unsafe_allow_html=True)
        st.caption("Start here. After a location is set, the map highlights the point and nearest cached PULA.")
        if st.button("Use my browser location"):
            st.session_state["request_browser_location"] = True
        if st.session_state.get("request_browser_location"):
            location = streamlit_geolocation()
        if location and location.get("latitude") is not None and location.get("longitude") is not None:
            set_selected_location(float(location["latitude"]), float(location["longitude"]), "browser location")
            st.session_state["request_browser_location"] = False
            st.rerun()
        manual_lat = st.number_input("Latitude", value=selected_lat or DEFAULT_LAT, format="%.6f")
        manual_lon = st.number_input("Longitude", value=selected_lon or DEFAULT_LON, format="%.6f")
        if st.button("Use entered coordinates"):
            set_selected_location(manual_lat, manual_lon, "entered coordinates")
            st.rerun()
        if selected_lat is not None and selected_lon is not None:
            source = st.session_state.get("selected_location_source", "selected location")
            st.success(f"Using {source}: {selected_lat:.5f}, {selected_lon:.5f}")
            if county:
                st.write(f"**County:** {county} County")
        else:
            st.info("No location selected yet. Coordinates are required before PULA and ESA context become meaningful.")
        st.markdown("</div>", unsafe_allow_html=True)

        render_result_panel(selected_lat, selected_lon, pulas)
        crop_or_site = render_esa_context(county, selected_lat, selected_lon, pula_intersects, nearest_pula)

    with left:
        st.markdown('<div class="panel"><div class="panel-title">Step 3: Nearby Area Details</div>', unsafe_allow_html=True)
        st.caption("These are context layers for scouting and follow-up. They do not replace BLT, the product label, or field diagnosis.")
        st.markdown("</div>", unsafe_allow_html=True)
        render_resistance_context(crop_or_site, selected_lat, selected_lon)
        render_eddmaps_context(selected_lat, selected_lon)

        st.markdown('<div class="panel"><div class="panel-title">Step 4: Crop and Extension Support</div>', unsafe_allow_html=True)
        if crop_or_site:
            st.write("Contacts below are filtered by the selected crop/site where possible.")
        else:
            st.info("Choose a crop/site in the ESA panel if you want crop-focused specialist routing. County office lookup still works from location alone.")
        st.markdown("</div>", unsafe_allow_html=True)
        render_county_support(county)
        render_contacts(crop_or_site)

        st.markdown('<div class="panel"><div class="panel-title">Step 5: Download Report</div>', unsafe_allow_html=True)
        st.write("Download a site-context report even if you skipped ESA point planning. If you selected a product above, use the ESA PDF button for mitigation-point details.")

        intersects, nearest = False, None
        auto_hsg = st.session_state.get("last_hsg", "Unknown")

        if selected_lat is not None and selected_lon is not None:
            intersects, nearest = location_result(selected_lat, selected_lon, pulas)

        rows = load_resistance_rows()
        matching_rows = resistance_context_for_crop(crop_or_site, rows)
        res_summaries = summarize_resistance_records(matching_rows, limit=5)

        comp_report = build_comprehensive_report(
            selected_lat, selected_lon, county, crop_or_site, nearest, intersects, auto_hsg, res_summaries
        )
        st.download_button(
            "Download Comprehensive Site Context Report",
            data=comp_report,
            file_name="comprehensive-site-context-report.md",
            mime="text/markdown",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        render_report_cta()


apply_theme()
if "view" not in st.session_state:
    st.session_state["view"] = "map"

if st.session_state["view"] == "report":
    render_report_form()
else:
    render_main_app()

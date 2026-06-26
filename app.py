from pathlib import Path
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
    PALM_URL,
    get_primary_disclaimer,
    get_resistance_disclaimer,
    get_result_disclaimer,
)
from src.extension_contacts import contacts_for_crop_or_site, load_contacts
from src.reports import (
    build_email_message,
    save_report,
    select_report_recipient,
    send_email_notification,
)
from src.spatial import point_in_polygons


st.set_page_config(page_title="PULA Awareness Tool", layout="wide")

PULA_FULL_PATH = Path("data/pula_alabama.geojson")
PULA_DISPLAY_PATH = Path("data/pula_alabama_display.geojson")
ACES_COUNTIES_URL = "https://www.aces.edu/counties/"
ACES_DIRECTORY_URL = "https://ssl.acesag.auburn.edu/directory-new/programAgentSearch.php?program=1"


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
          gap: 10px;
          align-items:center;
          min-width: 250px;
          justify-content:flex-end;
        }
        .au-mark {
          border: 1px solid rgba(255,255,255,.3);
          border-radius: 8px;
          padding: 10px 12px;
          color: white;
          font-weight: 760;
          line-height: 1;
          background: rgba(255,255,255,.08);
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


def render_header(metadata: dict, summary: dict) -> None:
    st.markdown(
        f"""
        <div class="au-hero">
          <div class="au-brand-row">
            <div>
              <div class="au-title">PULA Awareness Tool</div>
              <div class="au-subtitle">
                Alabama-focused pesticide limitation awareness with resistance context and Extension routing.
                Official compliance decisions still belong in EPA Bulletins Live! Two.
              </div>
              <div class="au-accent"></div>
            </div>
            <div class="au-lockup">
              <div class="au-mark">AU</div>
              <div class="au-mark">ACES</div>
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
    link_cols = st.columns(5)
    link_cols[0].link_button("EPA BLT", BLT_URL)
    link_cols[1].link_button("EPA PALM", PALM_URL)
    link_cols[2].link_button("weedscience.org", HEAP_URL)
    link_cols[3].link_button("ACES Counties", ACES_COUNTIES_URL)
    link_cols[4].link_button("ACES Directory", ACES_DIRECTORY_URL)


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


def location_result(lat: float, lon: float, pulas) -> tuple[bool, dict | None]:
    if pulas is None:
        return False, None
    intersects = not point_in_polygons(lat, lon, pulas).empty
    return intersects, nearest_pula_summary(lat, lon, pulas)


def render_result_panel(lat: float | None, lon: float | None, pulas) -> None:
    st.markdown('<div class="panel"><div class="panel-title">Nearest Cached PULA</div>', unsafe_allow_html=True)
    if lat is None or lon is None:
        st.markdown(
            '<div class="soft-note">Use browser location, map click, or coordinates to check the nearest cached PULA.</div></div>',
            unsafe_allow_html=True,
        )
        return

    intersects, nearest = location_result(lat, lon, pulas)
    st.info(get_result_disclaimer(cached_pula_found=intersects))
    st.write(f"Location checked: `{lat:.5f}, {lon:.5f}`")
    if nearest:
        st.metric("Nearest cached PULA distance", f"{nearest['distance_miles']:.2f} miles")
        st.write(f"**Nearest PULA ID:** {nearest.get('pula_id', '')}")
        if nearest.get("event_name"):
            st.write(f"**Event:** {nearest['event_name']}")
        if nearest.get("status"):
            st.write(f"**Status:** {nearest['status']}")
    st.link_button("Verify this location in EPA BLT", BLT_URL)
    st.markdown("</div>", unsafe_allow_html=True)


def render_contacts() -> None:
    st.markdown('<div class="panel"><div class="panel-title">Local Extension Support</div>', unsafe_allow_html=True)
    crop_or_site = st.text_input(
        "Crop or managed site",
        placeholder="Example: soybean, cotton, pasture, right-of-way",
    )
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
    st.link_button("Find your county Extension office", ACES_COUNTIES_URL)
    st.markdown("</div>", unsafe_allow_html=True)


def render_county_support(lat: float | None, lon: float | None) -> None:
    st.markdown('<div class="panel"><div class="panel-title">County Extension Office</div>', unsafe_allow_html=True)
    st.caption("Location-to-county lookup uses the U.S. Census geocoder and sends only the selected coordinates.")
    county = None
    if lat is not None and lon is not None:
        try:
            county = county_from_coordinates(lat, lon)
        except Exception:
            county = None
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

    render_header(metadata if validate_metadata(metadata) else {}, summary)
    render_links()

    location = None
    left, right = st.columns([1.8, 1], gap="large")

    with left:
        st.markdown('<div class="panel"><div class="panel-title">Alabama Cached PULA Map</div>', unsafe_allow_html=True)
        m = folium.Map(location=[32.8067, -86.7911], zoom_start=7, tiles="CartoDB positron")
        add_pula_layer(m, display_geojson)
        folium.LayerControl(collapsed=True).add_to(m)
        map_state = st_folium(m, height=590, use_container_width=True)
        st.caption("Orange regions are cached EPA PULA polygons intersecting Alabama. Always verify official requirements in BLT.")
        st.markdown("</div>", unsafe_allow_html=True)

    clicked = map_state.get("last_clicked") if map_state else None
    selected_lat = clicked.get("lat") if clicked else None
    selected_lon = clicked.get("lng") if clicked else None

    with right:
        st.markdown('<div class="panel"><div class="panel-title">Check a Location</div>', unsafe_allow_html=True)
        st.caption("Allow browser location, click the map, or enter coordinates manually.")
        if st.button("Use my browser location"):
            st.session_state["request_browser_location"] = True
        if st.session_state.get("request_browser_location"):
            location = streamlit_geolocation()
        if location and location.get("latitude") is not None and location.get("longitude") is not None:
            selected_lat = float(location["latitude"])
            selected_lon = float(location["longitude"])
        manual_lat = st.number_input("Latitude", value=selected_lat or 32.8067, format="%.6f")
        manual_lon = st.number_input("Longitude", value=selected_lon or -86.7911, format="%.6f")
        if st.button("Use entered coordinates"):
            selected_lat = manual_lat
            selected_lon = manual_lon
        st.markdown("</div>", unsafe_allow_html=True)

        render_result_panel(selected_lat, selected_lon, pulas)
        render_county_support(selected_lat, selected_lon)

        st.markdown('<div class="panel"><div class="panel-title">Resistance Context</div>', unsafe_allow_html=True)
        st.caption(heap_attribution())
        st.write(get_resistance_disclaimer())
        st.write("Alabama resistance records will appear here after the verified resistance snapshot is loaded.")
        st.markdown("</div>", unsafe_allow_html=True)

        render_contacts()

        st.button("Report suspected resistance", on_click=set_view, args=("report",))


apply_theme()
if "view" not in st.session_state:
    st.session_state["view"] = "map"

if st.session_state["view"] == "report":
    render_report_form()
else:
    render_main_app()

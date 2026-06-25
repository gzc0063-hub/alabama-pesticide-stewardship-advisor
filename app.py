from pathlib import Path

import folium
import streamlit as st
from streamlit_folium import st_folium

from src.data_epa import load_snapshot_metadata, validate_metadata
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


st.set_page_config(page_title="PULA Awareness Tool", layout="wide")


def smtp_settings_from_secrets() -> dict | None:
    if "smtp" not in st.secrets:
        return None
    smtp = st.secrets["smtp"]
    return {
        "host": smtp.get("host"),
        "port": smtp.get("port"),
        "username": smtp.get("username"),
        "password": smtp.get("password"),
        "sender": smtp.get("sender"),
        "recipient": smtp.get("recipient"),
    }


st.title("PULA Awareness Tool")
st.warning(get_primary_disclaimer())

metadata = load_snapshot_metadata()
if validate_metadata(metadata):
    st.caption(
        f"PULA data as of: {metadata['pula_date']} | "
        f"Resistance data as of: {metadata['heap_date']}"
    )
else:
    st.caption("Data snapshots are not yet verified.")

link_cols = st.columns(3)
link_cols[0].link_button("EPA Bulletins Live! Two", BLT_URL)
link_cols[1].link_button("EPA PALM", PALM_URL)
link_cols[2].link_button("weedscience.org", HEAP_URL)

left, right = st.columns([2, 1])

with left:
    st.subheader("Map")
    m = folium.Map(location=[32.8067, -86.7911], zoom_start=7, tiles="CartoDB positron")
    folium.Marker([32.8067, -86.7911], tooltip="Alabama center").add_to(m)
    map_state = st_folium(m, height=520, use_container_width=True)

    clicked = map_state.get("last_clicked") if map_state else None
    if clicked:
        st.info(get_result_disclaimer(cached_pula_found=False))
        st.write(f"Clicked location: {clicked['lat']:.5f}, {clicked['lng']:.5f}")
    else:
        st.info("Click the map to start an educational cached-PULA check.")

with right:
    st.subheader("Resistance Context")
    st.caption(heap_attribution())
    st.write(get_resistance_disclaimer())
    st.write("Alabama resistance records will appear here after the verified snapshot is loaded.")

    st.subheader("Local Support")
    crop_or_site = st.text_input("Crop or managed site", placeholder="Example: soybean, cotton, pasture")
    matching_contacts = contacts_for_crop_or_site(crop_or_site) if crop_or_site else load_contacts()
    if matching_contacts:
        for contact in matching_contacts:
            st.write(f"**{contact.get('name', '')}**")
            st.write(contact.get("specialty", ""))
            if contact.get("email"):
                st.write(contact["email"])
            if contact.get("phone"):
                st.write(contact["phone"])
            if contact.get("source_url"):
                st.link_button("Official contact page", contact["source_url"])
    else:
        st.write("Use the Alabama Extension county office lookup for local routing.")

st.divider()
st.subheader("Report Suspected Resistance")
st.caption("Submissions are suspected cases only and are not confirmations of resistance.")

with st.form("suspected_resistance_report"):
    reporter_role = st.selectbox(
        "Reporter role",
        ["Grower", "Consultant", "Extension agent", "Applicator", "Researcher", "Other"],
    )
    contact_name = st.text_input("Contact name")
    contact_phone = st.text_input("Contact phone")
    contact_email = st.text_input("Contact email")
    permission_to_contact = st.checkbox(
        "I give Extension permission to contact me about this suspected case."
    )
    county = st.text_input("County")
    location_description = st.text_area("Field or location description")
    crop_or_site_report = st.text_input("Crop or managed site for this report")
    suspected_weed = st.text_input("Suspected weed species")
    herbicide_product = st.text_input("Herbicide product")
    active_ingredient = st.text_input("Active ingredient, if known")
    site_of_action = st.text_input("Site of action/group, if known")
    application_date = st.text_input("Application date")
    application_rate = st.text_input("Application rate")
    survivor_pattern = st.selectbox(
        "Surviving weed pattern",
        ["Unknown", "Patchy", "Widespread", "Field-wide", "Along edges", "Other"],
    )
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

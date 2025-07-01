
import streamlit as st
from PIL import Image
import qrcode
from datetime import datetime
import base64
from io import BytesIO

# QR code generation
def generate_qr_code(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{qr_b64}"

# HTML card template
def generate_template(name, occasion, date, time, venue, msg, qr_data_uri):
    html = f"""
    <div style="padding:20px; background:#F0F8FF; border:2px solid #4682B4; border-radius:15px; width:600px; font-family:Georgia; position:relative;">
        <h2 style="color:#4682B4;">{occasion} Invitation</h2>
        <p>Dear <b>{name}</b>,</p>
        <p>{msg}</p>
        <p><b>Date:</b> {date}</p>
        <p><b>Time:</b> {time}</p>
        <p><b>Venue:</b> {venue}</p>
        <p>We look forward to your presence!</p>
        <img src='{qr_data_uri}' width='100' style="position:absolute; bottom:20px; right:20px;" />
        <p style="font-size:12px; color:gray; position:absolute; bottom:5px; right:20px;">Scan to RSVP</p>
    </div>
    """
    return html

# Streamlit UI
st.title("🎨 Invitation Card Generator")
st.markdown("Generate and share event invitation cards with custom info and QR RSVP.")

with st.form("form"):
    name = st.text_input("Invitee's Name:")
    occasion = st.selectbox("Occasion:", ["Wedding", "Birthday", "Anniversary", "Housewarming", "Other"])
    date = st.date_input("Event Date:")
    time = st.time_input("Event Time:")
    venue = st.text_input("Venue:")
    msg = st.text_area("Custom Message:", "You're cordially invited to join us.")
    rsvp_link = st.text_input("RSVP Link:", "https://forms.gle/exampleRSVP")
    submitted = st.form_submit_button("🎉 Generate Card")

if submitted and name.strip() and venue.strip():
    qr_uri = generate_qr_code(rsvp_link)
    formatted_date = date.strftime("%d %B %Y")
    formatted_time = time.strftime("%I:%M %p")
    html = generate_template(name, occasion, formatted_date, formatted_time, venue, msg, qr_uri)

    st.success("✅ Your invitation card is ready!")
    st.components.v1.html(html, height=520, scrolling=False)
else:
    if submitted:
        st.warning("Please fill all required fields.")

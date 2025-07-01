
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

# Template 1 - Elegant Blue
def template_blue(name, occasion, date, time, venue, msg, qr_data_uri):
    return f"""
    <div style="padding:25px; background:linear-gradient(135deg,#E0F7FA,#E1F5FE); border:2px solid #0277BD; border-radius:20px; width:600px; font-family:'Georgia'; position:relative; box-shadow: 5px 5px 15px rgba(0,0,0,0.2);">
        <h2 style="color:#01579B;">{occasion} Invitation</h2>
        <p>Dear <b>{name}</b>,</p>
        <p>{msg}</p>
        <p><b>Date:</b> {date}</p>
        <p><b>Time:</b> {time}</p>
        <p><b>Venue:</b> {venue}</p>
        <img src='{qr_data_uri}' width='100' style="position:absolute; bottom:20px; right:20px;" />
        <p style="font-size:12px; color:gray; position:absolute; bottom:5px; right:20px;">Scan to RSVP</p>
    </div>
    """

# Template 2 - Romantic Pink
def template_pink(name, occasion, date, time, venue, msg, qr_data_uri):
    return f"""
    <div style="padding:25px; background:linear-gradient(135deg,#FFF0F5,#FCE4EC); border:2px dashed #D81B60; border-radius:20px; width:600px; font-family:'Comic Sans MS'; position:relative; box-shadow: 5px 5px 15px rgba(255,105,180,0.3);">
        <h2 style="color:#AD1457;">{occasion} Invitation</h2>
        <p>Hey <b>{name}</b> 💖</p>
        <p>{msg}</p>
        <p><b>Date:</b> {date}</p>
        <p><b>Time:</b> {time}</p>
        <p><b>Venue:</b> {venue}</p>
        <img src='{qr_data_uri}' width='100' style="position:absolute; bottom:20px; right:20px;" />
        <p style="font-size:12px; color:#AD1457; position:absolute; bottom:5px; right:20px;">Scan to RSVP</p>
    </div>
    """

# Template 3 - Nature Green
def template_green(name, occasion, date, time, venue, msg, qr_data_uri):
    return f"""
    <div style="padding:25px; background:#E8F5E9; border:3px double #388E3C; border-radius:20px; width:600px; font-family:'Verdana'; position:relative; box-shadow: 0 0 10px #81C784;">
        <h2 style="color:#2E7D32;">{occasion} Invitation</h2>
        <p>Dear <b>{name}</b>,</p>
        <p>{msg}</p>
        <p><b>Date:</b> {date}</p>
        <p><b>Time:</b> {time}</p>
        <p><b>Venue:</b> {venue}</p>
        <img src='{qr_data_uri}' width='100' style="position:absolute; bottom:20px; right:20px;" />
        <p style="font-size:12px; color:#388E3C; position:absolute; bottom:5px; right:20px;">Scan to RSVP</p>
    </div>
    """

# Streamlit UI
st.title("🎨 Invitation Card Generator with Themes")
st.markdown("Create & download personalized event invitations with **QR code** and beautiful styles.")

templates = {
    "Elegant Blue": template_blue,
    "Romantic Pink": template_pink,
    "Nature Green": template_green,
}

with st.form("form"):
    name = st.text_input("Invitee's Name:")
    occasion = st.selectbox("Occasion:", ["Wedding", "Birthday", "Anniversary", "Housewarming", "Other"])
    date = st.date_input("Event Date:")
    time = st.time_input("Event Time:")
    venue = st.text_input("Venue:")
    msg = st.text_area("Custom Message:", "You're cordially invited to join us.")
    rsvp_link = st.text_input("RSVP Link:", "https://forms.gle/exampleRSVP")
    template_choice = st.selectbox("Choose a Theme Template:", list(templates.keys()))
    submitted = st.form_submit_button("🎉 Generate Card")

if submitted and name.strip() and venue.strip():
    qr_uri = generate_qr_code(rsvp_link)
    formatted_date = date.strftime("%d %B %Y")
    formatted_time = time.strftime("%I:%M %p")
    html = templates[template_choice](name, occasion, formatted_date, formatted_time, venue, msg, qr_uri)

    st.success("✅ Your invitation card is ready!")
    st.components.v1.html(html, height=550, scrolling=False)

    # Provide download button
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="invitation.html">📥 Download as HTML</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    if submitted:
        st.warning("Please fill all required fields.")

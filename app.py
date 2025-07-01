import streamlit as st
from PIL import Image
import qrcode
from datetime import datetime
import base64
from io import BytesIO

def generate_qr_code(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

def modern_template(name, occasion, date, time, venue, msg, qr_data_uri, photo_uri):
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap');
    .card {{
        font-family: 'Playfair Display', serif;
        background: linear-gradient(to bottom right, #fffefc, #f9f4f0);
        padding: 30px;
        border: 1px solid #d3cfc9;
        border-radius: 15px;
        max-width: 600px;
        margin: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        position: relative;
        color: #333;
    }}
    .title {{
        font-size: 26px;
        color: #6d4c41;
        margin-bottom: 20px;
        text-align: center;
    }}
    .content {{
        font-size: 18px;
        line-height: 1.6;
    }}
    .footer {{
        font-size: 12px;
        text-align: right;
        color: #888;
        margin-top: 20px;
    }}
    .photo {{
        border-radius: 50%;
        width: 80px;
        height: 80px;
        object-fit: cover;
        position: absolute;
        top: 20px;
        right: 20px;
        border: 2px solid #e0d7d1;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }}
    .qr {{
        position: absolute;
        bottom: 20px;
        right: 20px;
        width: 80px;
    }}
    </style>
    <div class="card">
        <div class="title">{occasion} Invitation</div>
        <div class="content">
            <p>Dear <strong>{name}</strong>,</p>
            <p>{msg}</p>
            <p><strong>Date:</strong> {date}<br/>
               <strong>Time:</strong> {time}<br/>
               <strong>Venue:</strong> {venue}</p>
        </div>
        {"<img src='" + photo_uri + "' class='photo'/>" if photo_uri else ""}
        <img src="{qr_data_uri}" class="qr"/>
        <div class="footer">Scan to RSVP</div>
    </div>
    """

st.set_page_config(page_title="Elegant Invitation Card", layout="centered")
st.title("💌 Elegant Invitation Card Generator")

with st.form("form"):
    name = st.text_input("Invitee's Name:")
    occasion = st.selectbox("Occasion:", ["Wedding", "Birthday", "Anniversary", "Housewarming", "Other"])
    date = st.date_input("Event Date:")
    time = st.time_input("Event Time:")
    venue = st.text_input("Venue:")
    msg = st.text_area("Custom Message:", "You're cordially invited to join us on this special occasion.")
    rsvp_link = st.text_input("RSVP Link:", "https://forms.gle/exampleRSVP")
    uploaded_photo = st.file_uploader("Upload Your Photo (Optional)", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("🎨 Generate Card")

if submitted and name.strip() and venue.strip():
    qr_uri = generate_qr_code(rsvp_link)
    formatted_date = date.strftime("%d %B %Y")
    formatted_time = time.strftime("%I:%M %p")
    
    if uploaded_photo:
        photo_b64 = base64.b64encode(uploaded_photo.read()).decode()
        photo_uri = f"data:image/png;base64,{photo_b64}"
    else:
        photo_uri = None

    html = modern_template(name, occasion, formatted_date, formatted_time, venue, msg, qr_uri, photo_uri)
    st.success("✅ Your elegant invitation card is ready!")
    st.components.v1.html(html, height=600, scrolling=False)

    # Download
    b64 = base64.b64encode(html.encode()).decode()
    download_link = f'<a href="data:text/html;base64,{b64}" download="invitation_card.html">📥 Download as HTML</a>'
    st.markdown(download_link, unsafe_allow_html=True)
else:
    if submitted:
        st.warning("Please fill all required fields.")

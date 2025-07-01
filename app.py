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

# Template with blinking text, shining border, and flower background
def animated_flower_template(name, occasion, date, time, venue, msg, qr_data_uri, photo_uri):
    return f\"\"\"
    <style>
    @keyframes blink {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
        100% {{ opacity: 1; }}
    }}
    @keyframes shine {{
        0% {{ box-shadow: 0 0 10px pink; }}
        50% {{ box-shadow: 0 0 30px hotpink; }}
        100% {{ box-shadow: 0 0 10px pink; }}
    }}
    .invitation-card {{
        padding: 25px;
        background: url('https://i.ibb.co/GVT9ygR/flowers-bg.jpg');
        background-size: cover;
        border: 5px solid deeppink;
        border-radius: 25px;
        width: 650px;
        font-family: 'Comic Sans MS', cursive;
        color: #6A1B9A;
        animation: shine 2s infinite;
        position: relative;
        margin: auto;
    }}
    .blinker {{
        animation: blink 1.5s infinite;
        color: #D81B60;
    }}
    </style>

    <div class="invitation-card">
        <h2 class="blinker">{occasion} Invitation</h2>
        <p>Dear <b>{name}</b>,</p>
        <p>{msg}</p>
        <p><b>Date:</b> {date}</p>
        <p><b>Time:</b> {time}</p>
        <p><b>Venue:</b> {venue}</p>
        {f"<img src='{photo_uri}' width='100' style='position:absolute; top:20px; right:20px; border-radius:50%; border:2px solid white;' />" if photo_uri else ""}
        <img src="{qr_data_uri}" width="100" style="position:absolute; bottom:20px; right:20px;" />
        <p style="font-size:12px; color:#AD1457; position:absolute; bottom:5px; right:20px;">Scan to RSVP</p>
    </div>
    \"\"\"

# Streamlit UI
st.set_page_config(page_title="Shiny Invitation Card Generator", layout="centered")
st.title("🌸 Animated Invitation Card Generator with Shine, Blink & Flowers")
st.markdown("Design and download beautiful, animated event invitations with floral effects and custom photo!")

with st.form("form"):
    name = st.text_input("Invitee's Name:")
    occasion = st.selectbox("Occasion:", ["Wedding", "Birthday", "Anniversary", "Housewarming", "Other"])
    date = st.date_input("Event Date:")
    time = st.time_input("Event Time:")
    venue = st.text_input("Venue:")
    msg = st.text_area("Custom Message:", "You're cordially invited to join us.")
    rsvp_link = st.text_input("RSVP Link:", "https://forms.gle/exampleRSVP")
    uploaded_photo = st.file_uploader("Upload Your Photo (Optional)", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("🌟 Generate Shiny Card")

if submitted and name.strip() and venue.strip():
    qr_uri = generate_qr_code(rsvp_link)
    formatted_date = date.strftime("%d %B %Y")
    formatted_time = time.strftime("%I:%M %p")

    # Process photo
    if uploaded_photo:
        img_bytes = uploaded_photo.read()
        photo_b64 = base64.b64encode(img_bytes).decode()
        photo_uri = f"data:image/png;base64,{photo_b64}"
    else:
        photo_uri = None

    html = animated_flower_template(name, occasion, formatted_date, formatted_time, venue, msg, qr_uri, photo_uri)

    st.success("✅ Your shiny invitation card is ready!")
    st.components.v1.html(html, height=600, scrolling=False)

    # Download HTML file
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="animated_invitation.html">📥 Download Shiny Invitation (HTML)</a>'
    st.markdown(href, unsafe_allow_html=True)
else:
    if submitted:
        st.warning("Please fill all required fields.")
'''

# Overwrite app.py with ultimate version
ultimate_app_path = "/mnt/data/app.py"
with open(ultimate_app_path, "w") as f:
    f.write(ultimate_app_code)

ultimate_app_path

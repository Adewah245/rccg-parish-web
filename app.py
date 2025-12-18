import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image

# ================== CONFIG ==================
PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"
ADMIN_PASSWORD = "sunriseadmin"  # 🔐 CHANGE THIS LATER

DATA_DIR = "data"
UPLOAD_DIR = "uploads"
PHOTO_DIR = os.path.join(UPLOAD_DIR, "photos")
LOGO_DIR = os.path.join(UPLOAD_DIR, "logo")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")

# ================== SETUP ==================
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(LOGO_DIR, exist_ok=True)

if not os.path.exists(MEMBERS_FILE):
    with open(MEMBERS_FILE, "w") as f:
        json.dump([], f)

def load_members():
    with open(MEMBERS_FILE, "r") as f:
        return json.load(f)

def save_members(members):
    with open(MEMBERS_FILE, "w") as f:
        json.dump(members, f, indent=4)

# ================== PAGE STYLE ==================
st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="wide")

st.markdown("""
<style>
body { background-color: #fafafa; }
h1, h2, h3 { color: #1f4e79; }
.stButton button {
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
}
.card {
    padding: 1rem;
    border-radius: 12px;
    background: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ================== LOGIN ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("## 🔐 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Welcome Admin 🌅")
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ================== HEADER ==================
logo_files = os.listdir(LOGO_DIR)
cols = st.columns([1, 4])
with cols[0]:
    if logo_files:
        st.image(os.path.join(LOGO_DIR, logo_files[0]), width=120)
with cols[1]:
    st.markdown(f"# {PARISH_NAME}")
    st.markdown("### Admin Dashboard ✨")

st.divider()

# ================== LOGO UPLOAD ==================
st.subheader("🖼️ Parish Logo")
logo = st.file_uploader("Upload / Change Logo", type=["png", "jpg", "jpeg"])
if logo:
    logo_path = os.path.join(LOGO_DIR, logo.name)
    with open(logo_path, "wb") as f:
        f.write(logo.read())
    st.success("Logo updated successfully 🌟")
    st.rerun()

# ================== MEMBERS ==================
members = load_members()
members = sorted(members, key=lambda x: x["name"].lower())

st.divider()
st.subheader("➕ Add New Member")

with st.form("add_member"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")
    dob = st.date_input("Date of Birth")
    photo = st.file_uploader("Photo", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Add Member")

    if submitted and name:
        photo_path = ""
        if photo:
            photo_path = os.path.join(PHOTO_DIR, photo.name)
            with open(photo_path, "wb") as f:
                f.write(photo.read())

        members.append({
            "id": datetime.now().timestamp(),
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "birthday": dob.strftime("%d-%m-%Y"),
            "photo": photo_path,
            "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_members(members)
        st.success("Member added 💯")
        st.rerun()

# ================== LIST MEMBERS ==================
st.divider()
st.subheader("👥 Members List")

search = st.text_input("🔍 Search by name or phone").lower()

for m in members:
    if search and search not in m["name"].lower() and search not in m["phone"]:
        continue

    st.markdown('<div class="card">', unsafe_allow_html=True)
    cols = st.columns([1, 3, 1])
    with cols[0]:
        if m["photo"] and os.path.exists(m["photo"]):
            st.image(m["photo"], width=100)
        else:
            st.write("📷 No photo")
    with cols[1]:
        st.markdown(f"### {m['name']}")
        st.write(f"📞 {m['phone']}")
        st.write(f"📧 {m['email']}")
        st.write(f"🏠 {m['address']}")
        st.write(f"🎂 {m['birthday']}")
    with cols[2]:
        if st.button("❌ Delete", key=str(m["id"])):
            members = [x for x in members if x["id"] != m["id"]]
            save_members(members)
            st.warning("Member deleted")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

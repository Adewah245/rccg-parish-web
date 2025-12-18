import streamlit as st
import json
import os
from datetime import datetime

# ================== CONFIG ==================
PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"
ADMIN_PASSWORD = "sunriseadmin"  # ⚠️ CHANGE THIS TO A STRONG PASSWORD LATER!

DATA_DIR = "data"
UPLOAD_DIR = "uploads"
PHOTO_DIR = os.path.join(UPLOAD_DIR, "photos")
LOGO_DIR = os.path.join(UPLOAD_DIR, "logo")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")

# ================== SETUP DIRECTORIES ==================
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(LOGO_DIR, exist_ok=True)

def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r") as f:
        return json.load(f)

def save_members(members):
    with open(MEMBERS_FILE, "w") as f:
        json.dump(members, f, indent=4)

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="Admin • " + PARISH_NAME, page_icon="🔐", layout="centered")

# ================== LOGIN ==================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("# 🔐 Admin Login")
    st.markdown("### Enter password to access admin panel")
    
    password = st.text_input("Password", type="password", placeholder="Type here...")
    
    col1, col2, col3 = st.columns([1,1,2])
    with col2:
        if st.button("Login", use_container_width=True):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful! Welcome Admin 🌅")
                st.rerun()
            else:
                st.error("❌ Wrong password")
    st.stop()

# ================== ADMIN DASHBOARD (After Login) ==================
st.markdown(f"# 🌅 {PARISH_NAME}")
st.markdown("### Admin Dashboard")

# Show logo if exists
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.image(os.path.join(LOGO_DIR, logo_files[0]), width=150)

st.markdown("---")

# ================== UPLOAD LOGO ==================
st.subheader("🖼️ Upload / Change Parish Logo")
logo_upload = st.file_uploader("Choose a logo image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="logo")
if logo_upload:
    # Clear old logos (optional - keeps only one)
    for old in os.listdir(LOGO_DIR):
        os.remove(os.path.join(LOGO_DIR, old))
    # Save new
    logo_path = os.path.join(LOGO_DIR, logo_upload.name)
    with open(logo_path, "wb") as f:
        f.write(logo_upload.getbuffer())
    st.success("Logo updated successfully!")
    st.rerun()

st.markdown("---")

# ================== ADD NEW MEMBER ==================
st.subheader("➕ Add New Member")

current_year = datetime.now().year
years = list(range(1950, current_year + 2))[::-1]  # 1950 to next year

with st.form("add_member_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", placeholder="e.g. John Adebayo")
        phone = st.text_input("Phone Number *", placeholder="e.g. 08012345678")
        email = st.text_input("Email (optional)", placeholder="john@example.com")
    
    with col2:
        address = st.text_input("Address (optional)", placeholder="e.g. Makurdi, Benue")
        birth_year = st.selectbox("Birth Year *", years)
        birth_month = st.selectbox("Birth Month *", list(range(1, 13)))
        birth_day = st.selectbox("Birth Day *", list(range(1, 32)))
    
    photo = st.file_uploader("Upload Photo (optional)", type=["png", "jpg", "jpeg"], key="photo")
    
    submitted = st.form_submit_button("Add Member", use_container_width=True)
    
    if submitted:
        if not name or not phone:
            st.error("Name and Phone are required!")
        else:
            try:
                dob = datetime(birth_year, birth_month, birth_day)
                photo_path = ""
                if photo:
                    photo_path = os.path.join(PHOTO_DIR, photo.name)
                    with open(photo_path, "wb") as f:
                        f.write(photo.getbuffer())
                
                members = load_members()
                new_member = {
                    "id": datetime.now().timestamp(),
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "address": address.strip(),
                    "birthday": dob.strftime("%d-%m-%Y"),
                    "photo": photo_path,
                    "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                members.append(new_member)
                save_members(members)
                st.success(f"✅ {name} added successfully!")
                st.rerun()
            except ValueError:
                st.error("Invalid date! (e.g., February doesn't have 31 days)")

st.markdown("---")

# ================== MANAGE MEMBERS (List & Delete) ==================
st.subheader("👥 Manage Members")
members = load_members()
members = sorted(members, key=lambda x: x["name"].lower())

search = st.text_input("🔍 Search member to delete")
filtered = [m for m in members if not search or search.lower() in m["name"].lower()]

if not filtered:
    st.info("No members found.")
else:
    for m in filtered:
        cols = st.columns([1, 4, 1])
        with cols[0]:
            if m["photo"] and os.path.exists(m["photo"]):
                st.image(m["photo"], width=80)
            else:
                st.markdown("📷<br>No Photo", unsafe_allow_html=True)
        with cols[1]:
            st.write(f"**{m['name']}**")
            st.caption(f"📞 {m['phone']} | 🎂 {m['birthday']}")
        with cols[2]:
            if st.button("🗑️ Delete", key=f"del_{m['id']}"):
                members = [x for x in members if x["id"] != m["id"]]
                if m["photo"] and os.path.exists(m["photo"]):
                    os.remove(m["photo"])
                save_members(members)
                st.warning(f"{m['name']} deleted.")
                st.rerun

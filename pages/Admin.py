import streamlit as st
import json
import os
from datetime import datetime

# ================== CONFIG - SAME AS MAIN APP ==================
PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"
ADMIN_PASSWORD = "sunriseadmin"  # CHANGE THIS TO A STRONG PASSWORD!
MEMBERS_FILE = "data/parish_members.json"
PHOTO_DIR = "photos"
LOGO_DIR = "uploads/logo"

os.makedirs("data", exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(LOGO_DIR, exist_ok=True)

def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_members(members):
    with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(members, f, indent=4, ensure_ascii=False)

# ================== LOGIN ==================
st.set_page_config(page_title="Admin • " + PARISH_NAME, page_icon="🔐")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("# 🔐 Admin Login")
    st.markdown("### Enter password to manage members")
    password = st.text_input("Password", type="password")
    if st.button("Login", use_container_width=True):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Welcome Admin 🌅")
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ================== ADMIN DASHBOARD ==================
st.markdown(f"# {PARISH_NAME}")
st.markdown("### Admin Dashboard ✨")

members = load_members()
st.markdown(f"**Total Members:** {len(members)}")

# ================== ADD NEW MEMBER ==================
st.subheader("➕ Add New Member")

current_year = datetime.now().year
years = list(range(1950, current_year + 2))[::-1]

with st.form("add_member"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *")
        phone = st.text_input("Phone Number *")
        email = st.text_input("Email (optional)")
    with col2:
        address = st.text_input("Address (optional)")
        birth_year = st.selectbox("Birth Year *", years)
        birth_month = st.selectbox("Birth Month *", range(1,13))
        birth_day = st.selectbox("Birth Day *", range(1,32))

    photo = st.file_uploader("Upload Photo (optional)", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Add Member")

    if submitted:
        if not name or not phone:
            st.error("Name and Phone are required!")
        else:
            try:
                dob = datetime(birth_year, birth_month, birth_day)
                birthday = dob.strftime("%d-%m-%Y")
                photo_path = ""
                if photo:
                    photo_path = os.path.join(PHOTO_DIR, photo.name)
                    with open(photo_path, "wb") as f:
                        f.write(photo.getbuffer())

                new_member = {
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "address": address.strip(),
                    "birthday": birthday,
                    "photo": photo_path,
                    "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                members.append(new_member)
                save_members(members)
                st.success(f"✅ {name} added successfully!")
                st.rerun()
            except ValueError:
                st.error("Invalid date (e.g. Feb 30 doesn't exist)")

# ================== EDIT OR DELETE MEMBER ==================
st.subheader("✏️ Edit or Delete Member")

search = st.text_input("🔍 Search member by name or phone")
found_members = [m for m in members if search.lower() in m["name"].lower() or search in m["phone"]]

if search and found_members:
    selected = st.selectbox(
        "Select member to edit/delete",
        found_members,
        format_func=lambda m: f"{m['name']} ({m['phone']})"
    )

    if selected:
        with st.form("edit_member"):
            col1, col2 = st.columns(2)
            with col1:
                edit_name = st.text_input("Full Name *", value=selected["name"])
                edit_phone = st.text_input("Phone Number *", value=selected["phone"])
                edit_email = st.text_input("Email", value=selected.get("email", ""))
            with col2:
                edit_address = st.text_input("Address", value=selected.get("address", ""))
                # Birthday kept as is (or you can add dropdowns if needed)

            new_photo = st.file_uploader("Update Photo (optional)", type=["png", "jpg", "jpeg"])
            save_btn = st.form_submit_button("Save Changes")

            if save_btn:
                if not edit_name or not edit_phone:
                    st.error("Name and Phone required")
                else:
                    # Update the member in list
                    selected["name"] = edit_name.strip()
                    selected["phone"] = edit_phone.strip()
                    selected["email"] = edit_email.strip()
                    selected["address"] = edit_address.strip()

                    if new_photo:
                        new_path = os.path.join(PHOTO_DIR, new_photo.name)
                        with open(new_path, "wb") as f:
                            f.write(new_photo.getbuffer())
                        selected["photo"] = new_path

                    save_members(members)
                    st.success("Member updated successfully!")
                    st.rerun()

        if st.button("🗑️ Delete This Member", type="primary"):
            if st.button("Confirm Delete - No Undo!", type="secondary"):
                members.remove(selected)
                if selected.get("photo") and os.path.exists(selected["photo"]):
                    os.remove(selected["photo"])
                save_members(members)
                st.success("Member deleted")
                st.rerun()

# ================== LOGOUT ==================
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()

import streamlit as st
import json
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
import urllib.parse

# ================== CONFIG ==================
PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"
ADMIN_PASSWORD = "sunriseadmin"
MEMBERS_FILE = "data/parish_members.json"
PHOTO_DIR = "photos"

EMAIL_ADDRESS = "yourchurch@gmail.com"       # CHANGE
EMAIL_PASSWORD = "APP_PASSWORD"              # CHANGE

os.makedirs("data", exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)

# ================== HELPERS ==================
def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_members(members):
    with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(members, f, indent=4, ensure_ascii=False)

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def whatsapp_link(phone, message):
    phone = phone.replace("+", "").replace(" ", "")
    msg = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={msg}"

# ================== LOGIN ==================
st.set_page_config(page_title="Admin • " + PARISH_NAME, page_icon="🔐")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("# 🔐 Admin Login")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ================== DASHBOARD ==================
st.markdown(f"# {PARISH_NAME} - Admin Panel")
members = load_members()
st.markdown(f"**Total Members:** {len(members)}")
st.divider()

# ================== ADD MEMBER ==================
st.subheader("➕ Add New Member")

current_year = datetime.now().year
years = list(range(1950, current_year + 2))[::-1]

with st.form("add_member"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *")
        phone = st.text_input("Phone Number *")
        email = st.text_input("Email")
    with col2:
        address = st.text_input("Address")
        birth_year = st.selectbox("Birth Year *", years)
        birth_month = st.selectbox("Birth Month *", range(1, 13))
        birth_day = st.selectbox("Birth Day *", range(1, 32))

    photo = st.file_uploader("Photo", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Add Member")

    if submitted:
        if not name or not phone:
            st.error("Name and Phone are required")
        else:
            try:
                dob = datetime(birth_year, birth_month, birth_day)
                photo_path = ""

                if photo:
                    photo_path = os.path.join(PHOTO_DIR, photo.name)
                    with open(photo_path, "wb") as f:
                        f.write(photo.getbuffer())

                members.append({
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "address": address.strip(),
                    "birthday": dob.strftime("%d-%m-%Y"),
                    "photo": photo_path,
                    "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

                save_members(members)
                st.success("Member added successfully")
                st.rerun()
            except ValueError:
                st.error("Invalid date")

st.divider()

# ================== EDIT / DELETE ==================
st.subheader("✏️ Edit or Delete Member")

search = st.text_input("🔍 Search (min 2 characters)")

found = []
if len(search) >= 2:
    found = [
        (i, m) for i, m in enumerate(members)
        if search.lower() in m["name"].lower() or search in m["phone"]
    ]

if found:
    selected = st.selectbox(
        "Select Member",
        found,
        format_func=lambda x: f"{x[1]['name']} - {x[1]['phone']}"
    )

    if st.button("Load Member"):
        st.session_state.edit_index = selected[0]
        st.rerun()

if "edit_index" in st.session_state:
    m = members[st.session_state.edit_index]

    with st.form("edit_form"):
        col1, col2 = st.columns(2)
        with col1:
            edit_name = st.text_input("Name", m["name"])
            edit_phone = st.text_input("Phone", m["phone"])
            edit_email = st.text_input("Email", m.get("email", ""))
        with col2:
            edit_address = st.text_input("Address", m.get("address", ""))

        new_photo = st.file_uploader("Update Photo", type=["png", "jpg", "jpeg"])
        save_edit = st.form_submit_button("Save Changes")

        if save_edit:
            m["name"] = edit_name.strip()
            m["phone"] = edit_phone.strip()
            m["email"] = edit_email.strip()
            m["address"] = edit_address.strip()

            if new_photo:
                path = os.path.join(PHOTO_DIR, new_photo.name)
                with open(path, "wb") as f:
                    f.write(new_photo.getbuffer())
                m["photo"] = path

            save_members(members)
            del st.session_state.edit_index
            st.success("Member updated")
            st.rerun()

    if st.button("🗑️ Delete Member"):
        members.pop(st.session_state.edit_index)
        save_members(members)
        del st.session_state.edit_index
        st.success("Member deleted")
        st.rerun()

st.divider()

# ================== MESSAGE CENTER ==================
st.header("📣 Message Center")

tab1, tab2 = st.tabs(["📧 Email", "📲 WhatsApp"])

with tab1:
    subject = st.text_input("Email Subject")
    email_msg = st.text_area("Email Message")

    if st.button("Send Email"):
        sent = 0
        for m in members:
            if m.get("email"):
                send_email(m["email"], subject, email_msg)
                sent += 1
        st.success(f"Email sent to {sent} members")

with tab2:
    wa_msg = st.text_area("WhatsApp Message")

    if st.button("Send WhatsApp"):
        for m in members:
            if m.get("phone"):
                link = whatsapp_link(m["phone"], wa_msg)
                st.markdown(f"[Send to {m['name']}]({link})", unsafe_allow_html=True)

st.divider()

# ================== LIST MEMBERS ==================
st.subheader("All Members")
for m in members:
    st.write(f"{m['name']} | {m['phone']} | {m['birthday']}")

# ================== LOGOUT ==================
if st.sidebar.button("🚪 Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()

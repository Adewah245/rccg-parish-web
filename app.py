import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ================== CONFIG ==================
PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"
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

members = load_members()

# ================== UPCOMING BIRTHDAYS ==================
today = datetime.today()
upcoming = []
for m in members:
    try:
        bday = datetime.strptime(m["birthday"], "%d-%m-%Y")
        bday_this_year = bday.replace(year=today.year)
        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)
        days_ahead = (bday_this_year - today).days
        if 0 <= days_ahead <= 30:
            upcoming.append((days_ahead, bday_this_year.strftime("%d %B"), m))
    except:
        pass
upcoming.sort()

# ================== STYLE ==================
st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="centered")

st.markdown("""
<style>
    .big-title { font-size: 3rem; text-align: center; color: #c0392b; font-weight: bold; }
    .christmas-message { font-size: 1.4rem; text-align: center; font-style: italic; color: #27ae60; background: #f0fff0; padding: 1.5rem; border-radius: 15px; margin: 2rem 0; border: 2px solid #27ae60; }
</style>
""", unsafe_allow_html=True)

# Header
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.image(os.path.join(LOGO_DIR, logo_files[0]), width=180)

st.markdown(f"<h1 class='big-title'>⛪ {PARISH_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;'>👥 Total Members: {len(members)}</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='christmas-message'>
📢 Christmas brings about a bounty of joy and the message of hope, love, and salvation through our Lord Jesus Christ.<br>
May this holy season fill your hearts with peace, your homes with warmth, and your lives with His everlasting light! ✝️🎄
</div>
""", unsafe_allow_html=True)

# ================== UPCOMING BIRTHDAYS ==================
if upcoming:
    st.markdown("### 🎉 Upcoming Birthdays (Next 30 Days)")
    for days, date_str, m in upcoming:
        with st.container(border=True):
            st.markdown(f"**{m['name'].title()}** — {date_str} ({days} day{'s' if days != 1 else ''} away) 🎂")
            phone = m['phone'].strip()
            if phone.startswith('0'):
                phone = '234' + phone[1:]
            elif not phone.startswith('234'):
                phone = '234' + phone
            whatsapp_url = f"https://wa.me/{phone}?text=Happy%20Birthday%20{m['name'].title()}!%20God%20bless%20you%20-%20Sunrise%20Parish%20🌅"
            st.markdown(f"[📱 Send Birthday Wish on WhatsApp]({whatsapp_url})")
            if m.get("email"):
                email_url = f"mailto:{m['email']}?subject=Happy%20Birthday&body=Dear%20{m['name'].title()},%20Happy%20Birthday!"
                st.markdown(f"[📧 Send via Email]({email_url})")

# ================== MESSAGE DISTRIBUTION ==================
st.markdown("### 📩 Message Distribution — Send to All Members")

tab_whatsapp, tab_email = st.tabs(["📱 WhatsApp", "📧 Emails"])

with tab_whatsapp:
    whatsapp_members = [m for m in members if m['phone'].strip()]
    if whatsapp_members:
        st.write(f"**{len(whatsapp_members)} members with WhatsApp:**")
        numbers = []
        for m in sorted(whatsapp_members, key=lambda x: x['name'].lower()):
            phone = m['phone'].strip()
            if phone.startswith('0'):
                phone = '234' + phone[1:]
            elif not phone.startswith('234'):
                phone = '234' + phone
            numbers.append(phone)
            st.write(f"• {m['name'].title()} — `{phone}`")
        st.code(",".join(numbers))
        st.caption("Copy and paste into WhatsApp broadcast")
    else:
        st.info("No phone numbers yet.")

with tab_email:
    email_members = [m for m in members if m.get('email', '').strip()]
    if email_members:
        st.write(f"**{len(email_members)} members with email:**")
        emails = [m['email'].strip() for m in sorted(email_members, key=lambda x: x['name'].lower())]
        for m in sorted(email_members, key=lambda x: x['name'].lower()):
            st.write(f"• {m['name'].title()} — `{m['email']}`")
        st.code("; ".join(emails))
        st.caption("Copy and paste into BCC")
    else:
        st.info("No emails yet.")

# ================== MEMBERS DIRECTORY ==================
st.markdown("## 👥 Members Directory")

search_term = st.text_input("🔍 Search by name or phone", placeholder="Type at least 3 characters...").strip().lower()

if len(search_term) >= 3:
    filtered_members = [m for m in members if search_term in m["name"].lower() or search_term in m["phone"]]
else:
    filtered_members = members

if not filtered_members:
    st.info("No members found." if len(search_term) >= 3 else "All members shown below.")
else:
    for member in filtered_members:
        with st.expander(f"👤 {member['name'].title()}  |  📞 {member['phone']}  |  🎂 {member['birthday']}"):
            cols = st.columns([1, 3])
            with cols[0]:
                photo_path = member.get("photo", "")
                if photo_path and os.path.exists(photo_path):
                    st.image(photo_path, use_column_width=True, caption=member['name'].title())
                else:
                    st.markdown("<div style='height:350px;background:#ecf0f1;border-radius:15px;display:flex;align-items:center;justify-content:center;'><p style='color:#95a5a6;font-size:1.6rem;'>📷 No Photo Yet</p></div>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"**Full Name:** {member['name'].title()}")
                st.markdown(f"**Phone:** {member['phone']}")
                if member.get("email"):
                    st.markdown(f"**Email:** {member['email']}")
                if member.get("address"):
                    st.markdown(f"**Address:** {member['address']}")
                st.markdown(f"**Member Since:** {member.get('joined', 'N/A')}")

                phone = member['phone'].strip()
                if phone.startswith('0'):
                    phone = '234' + phone[1:]
                elif not phone.startswith('234'):
                    phone = '234' + phone
                whatsapp_url = f"https://wa.me/{phone}?text=Hello%20{member['name'].title()}!%20God%20bless%20you%20-%20Sunrise%20Parish%20🌅"
                st.markdown(f"[📱 Send Message on WhatsApp]({whatsapp_url})")
                if member.get("email"):
                    email_url = f"mailto:{member['email']}?subject=Hello%20from%20Sunrise%20Parish"
                    st.markdown(f"[📧 Send Email]({email_url})")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7f8c8d;'>Built with ❤️ for RCCG Benue 2 Sunrise Parish 🌅</p>", unsafe_allow_html=True)

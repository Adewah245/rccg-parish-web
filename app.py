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

# ================== PAGE SETUP & STYLE ==================
st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="centered")

st.markdown("""
<style>
    .big-title { font-size: 3rem; text-align: center; color: #c0392b; font-weight: bold; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.6rem; text-align: center; color: #8e44ad; margin-bottom: 2rem; }
    .christmas-message { 
        font-size: 1.4rem; text-align: center; font-style: italic; color: #27ae60; 
        background: #f0fff0; padding: 1.5rem; border-radius: 15px; margin: 2rem 0; 
        border: 2px solid #27ae60; 
    }
</style>
""", unsafe_allow_html=True)

# Header
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.image(os.path.join(LOGO_DIR, logo_files[0]), width=180)

st.markdown(f"<h1 class='big-title'>⛪ {PARISH_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>👥 Total Members: {len(members)}</p>", unsafe_allow_html=True)

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
            whatsapp_url = f"https://wa.me/{phone}?text=Happy%20Birthday%20{m['name'].title()}!%20May%20God%20bless%20you%20abundantly%20-%20Sunrise%20Parish%20🌅"
            st.markdown(f"[📱 Send Birthday Wish on WhatsApp]({whatsapp_url})")
            if m.get("email"):
                email_url = f"mailto:{m['email']}?subject=Happy%20Birthday!&body=Dear%20{m['name'].title()},%20Happy%20Birthday!%20God%20bless%20you..."
                st.markdown(f"[📧 Send via Email]({email_url})")

# ================== MESSAGE DISTRIBUTION WITH NUMBERED LISTING ==================
st.markdown("### 📩 Message Distribution — Send to All Members")

tab_whatsapp, tab_email = st.tabs(["📱 WhatsApp Numbers", "📧 Emails"])

with tab_whatsapp:
    whatsapp_members = [m for m in members if m['phone'].strip()]
    if whatsapp_members:
        st.write(f"**{len(whatsapp_members)} members with phone numbers:**")
        numbers = []
        for i, m in enumerate(sorted(whatsapp_members, key=lambda x: x['name'].lower()), 1):
            phone = m['phone'].strip()
            if phone.startswith('0'):
                phone = '234' + phone[1:]
            elif not phone.startswith('234'):
                phone = '234' + phone
            numbers.append(phone)
            st.write(f"**{i}.** {m['name'].title()} — `{phone}`")
        
        all_numbers = ",".join(numbers)
        st.code(all_numbers, language=None)
        st.caption("Copy the numbers above → paste into WhatsApp to create broadcast list")
        
        broadcast_msg = "Hello beloved Sunrise Parish family!%0A%0AHere is

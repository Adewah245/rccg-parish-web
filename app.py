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
st.markdown(f"<p class

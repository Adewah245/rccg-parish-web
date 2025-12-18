import streamlit as st
import json
import os

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

# ================== PAGE SETUP ==================
st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="centered")

st.markdown(f"""
<style>
    .big-title {{ font-size: 2.8rem; text-align: center; color: #e67e22; margin-bottom: 0; }}
    .message {{ font-size: 1.3rem; text-align: center; font-style: italic; color: #27ae60; margin: 2rem 0; }}
</style>
""", unsafe_allow_html=True)

# Header
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.image(os.path.join(LOGO_DIR, logo_files[0]), width=200)

st.markdown(f"<h1 class='big-title'>⛪ {PARISH_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center; margin-bottom: 2rem;'>👥 Total Members: {len(members)}</h2>", unsafe_allow_html=True)

st.markdown("<p class='message'>📢 Christmas brings about a bounty of joy and the message of hope, love, and salvation through our Lord Jesus Christ. May this season fill your hearts with peace! ✝️🎄</p>", unsafe_allow_html=True)

# ================== MEMBERS DIRECTORY - CLICK TO OPEN DETAILS ==================
st.markdown("## 👥 Members Directory")

search = st.text_input("🔍 Search by name or phone", placeholder="Type to search...").strip().lower()

filtered_members = [
    m for m in members
    if not search or search in m["name"].lower() or search in m["phone"]
]

if not filtered_members:
    st.info("No members found matching your search." if search else "No members registered yet.")
else:
    for member in filtered_members:
        with st.expander(f"👤 {member['name'].title()}  |  📞 {member['phone']}  |  🎂 {member['birthday']}"):
            cols = st.columns([1, 2])
            with cols[0]:
                photo_path = member.get("photo", "")
                if photo_path and os.path.exists(photo_path):
                    st.image(photo_path, use_column_width=True, caption=member['name'].title())
                else:
                    st.markdown(
                        """
                        <div style="height:300px; background:#f8f9fa; border-radius:10px; 
                                    display:flex; align-items:center; justify-content:center;">
                            <p style="color:#adb5bd; font-size:1.5rem; margin:0;">📷 No Photo Yet</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            with cols[1]:
                st.markdown(f"**Name:** {member['name'].title()}")
                st.markdown(f"**Phone:** {member['phone']}")
                if member.get("email"):
                    st.markdown(f"**Email:** {member['email']}")
                if member.get("address"):
                    st.markdown(f"**Address:** {member['address']}")
                st.markdown(f"**Joined:** {member.get('joined', 'N/A')}")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Built with ❤️ for RCCG Benue 2 Sunrise Parish • Young & Adults Zone 🌅</p>", unsafe_allow_html=True)

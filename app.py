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

# ================== PAGE SETUP & BEAUTIFUL STYLE ==================
st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="centered")

st.markdown("""
<style>
    .big-title { 
        font-size: 3rem; 
        text-align: center; 
        color: #c0392b; 
        font-weight: bold; 
        margin-bottom: 0.5rem; 
    }
    .subtitle { 
        font-size: 1.6rem; 
        text-align: center; 
        color: #8e44ad; 
        margin-bottom: 2rem; 
    }
    .christmas-message { 
        font-size: 1.4rem; 
        text-align: center; 
        font-style: italic; 
        color: #27ae60; 
        background: #f0fff0; 
        padding: 1.5rem; 
        border-radius: 15px; 
        margin: 2rem 0; 
        border: 2px solid #27ae60; 
    }
    .expander-header {
        font-size: 1.3rem !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.image(os.path.join(LOGO_DIR, logo_files[0]), width=180, use_column_width=False)

st.markdown(f"<h1 class='big-title'>⛪ {PARISH_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>👥 Total Members: {len(members)}</p>", unsafe_allow_html=True)

st.markdown("""
<div class='christmas-message'>
📢 Christmas brings about a bounty of joy and the message of hope, love, and salvation through our Lord Jesus Christ.<br>
May this holy season fill your hearts with peace, your homes with warmth, and your lives with His everlasting light! ✝️🎄
</div>
""", unsafe_allow_html=True)

# ================== MEMBERS DIRECTORY ==================
st.markdown("## 👥 Members Directory")

search_term = st.text_input(
    "🔍 Search by name or phone",
    placeholder="Type at least 3 characters to search...",
    help="Search works on name or phone number (minimum 3 characters)"
).strip().lower()

# Filter only if 3+ characters typed
if len(search_term) >= 3:
    filtered_members = [
        m for m in members
        if search_term in m["name"].lower() or search_term in m["phone"]
    ]
else:
    filtered_members = members

if not filtered_members:
    st.info("No members found matching your search." if len(search_term) >= 3 else "Begin typing to search members.")
else:
    for member in filtered_members:
        with st.expander(f"👤 {member['name'].title()}  |  📞 {member['phone']}  |  🎂 {member['birthday']}", expanded=False):
            cols = st.columns([1, 3])
            with cols[0]:
                photo_path = member.get("photo", "")
                if photo_path and os.path.exists(photo_path):
                    st.image(photo_path, use_column_width=True, caption=member['name'].title())
                else:
                    st.markdown(
                        """
                        <div style="height:350px; background:#ecf0f1; border-radius:15px; 
                                    display:flex; align-items:center; justify-content:center; margin:10px 0;">
                            <p style="color:#95a5a6; font-size:1.6rem; margin:0;">📷 No Photo Yet</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            with cols[1]:
                st.markdown(f"**Full Name:** {member['name'].title()}")
                st.markdown(f"**Phone:** {member['phone']}")
                if member.get("email"):
                    st.markdown(f"**Email:** {member['email']}")
                if member.get("address"):
                    st.markdown(f"**Address:** {member['address']}")
                st.markdown(f"**Birthday:** {member['birthday']}")
                st.markdown(f"**Member Since:** {member.get('joined', 'N/A')}")

# Footer
st.markdown("<hr style='margin-top: 4rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#7f8c8d; font-size:1.1rem;'>"
            "Built with ❤️ and prayer for RCCG Benue 2 Sunrise Parish • Young & Adults Zone 🌅<br>"
            "May the Lord continue to bless and increase this family in Jesus' name. Amen.</p>", 
            unsafe_allow_html=True)

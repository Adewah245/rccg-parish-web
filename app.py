import streamlit as st
import json
import os

PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"
MEMBERS_FILE = "parish_members.json"
PHOTO_DIR = "photos"
LOGO_DIR = "uploads/logo"  # Optional logo folder

os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(LOGO_DIR, exist_ok=True)

def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

members = load_members()

st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="centered")

st.markdown("""
<style>
    .big-title { font-size: 2.8rem; text-align: center; color: #e67e22; }
    .message { font-size: 1.3rem; text-align: center; font-style: italic; color: #27ae60; margin: 2rem 0; }
    .card { padding: 1.5rem; border-radius: 15px; background: white; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Header
logo_files = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
if logo_files:
    st.image(os.path.join(LOGO_DIR, logo_files[0]), width=200)

st.markdown(f"<h1 class='big-title'>⛪ {PARISH_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;'>👥 Total Members: {len(members)}</h2>", unsafe_allow_html=True)

st.markdown("<p class='message'>📢 Christmas brings about a bounty of joy and the message of hope, love, and salvation through our Lord Jesus Christ. May this season fill your hearts with peace! ✝️🎄</p>", unsafe_allow_html=True)

# Members Directory
st.markdown("## 👥 Members Directory")
search = st.text_input("🔍 Search by name or phone").strip().lower()

filtered = [m for m in members if not search or search in m["name"].lower() or search in m["phone"]]

for m in filtered:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cols = st.columns([1, 3])
    with cols[0]:
        photo = m.get("photo", "")
        if photo and os.path.exists(photo):
            with st.expander("📷 View Full Photo"):
                st.image(photo, use_column_width=True, caption=m["name"])
            st.image(photo, width=150)
        else:
            st.markdown("<div style='text-align:center;padding:50px;background:#f0f0f0;border-radius:10px;'>📷 No Photo</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"### {m['name']}")
        st.write(f"📞 **Phone:** {m['phone']}")
        if m.get("email"): st.write(f"📧 **Email:** {m.get('email')}")
        if m.get("address"): st.write(f"🏠 **Address:** {m.get('address')}")
        st.write(f"🎂 **Birthday:** {m['birthday']}")
        st.write(f"📅 **Joined:** {m.get('joined', 'N/A')}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr><p style='text-align:center;'>Built with ❤️ for RCCG Sunrise Parish 🌅</p>", unsafe_allow_html=True)

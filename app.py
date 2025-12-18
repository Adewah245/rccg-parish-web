import streamlit as st
import json
import os

# ================== CONFIG ==================
PARISH_NAME = "RCCG BENUE 2 SUNRISE PARISH YOUNG & ADULTS ZONE"

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

members = load_members()
total_members = len(members)

# ================== PAGE CONFIG ==================
st.set_page_config(page_title=PARISH_NAME, page_icon="🌅", layout="centered")

# ================== STYLE ==================
st.markdown("""
<style>
    .big-title { font-size: 3rem; text-align: center; color: #d35400; }
    .subtitle { font-size: 1.5rem; text-align: center; color: #8e44ad; }
    .message { font-size: 1.2rem; text-align: center; font-style: italic; color: #27ae60; margin: 2rem 0; }
    .card { padding: 1.5rem; border-radius: 15px; background: white; box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin: 1.5rem 0; }
    .photo-expander { text-align: center; }
</style>
""", unsafe_allow_html=True)

# ================== HEADER WITH VISUALS ==================
st.markdown("<h1 class='big-title'>⛪ RCCG BENUE 2 SUNRISE PARISH</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Young & Adults Zone</p>", unsafe_allow_html=True)<grok:render card_id="7b412e,051027,2a8e85" card_type="image_card_group" type="render_card"></grok:render>

st.markdown(f"<h2 style='text-align:center;'>👥 Total Members: {total_members}</h2>", unsafe_allow_html=True)

st.markdown("<p class='message'>📢 Christmas brings about a bounty of joy and the message of hope, love, and salvation through our Lord Jesus Christ. May this season fill your hearts with peace! ✝️🎄</p>", unsafe_allow_html=True)<grok:render card_id="ffd4cd,2b2363" card_type="image_card_group" type="render_card"></grok:render>

# ================== MEMBERS DIRECTORY ==================
st.markdown("## 👥 Members Directory")

search = st.text_input("🔍 Search by name or phone", placeholder="Start typing...").strip().lower()

filtered = [m for m in members if not search or search in m["name"].lower() or search in m["phone"]]

if not filtered:
    st.info("No members found." if search else "No members yet — add some via Admin!")
else:
    for m in filtered:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cols = st.columns([1, 3])
        with cols[0]:
            if m["photo"] and os.path.exists(m["photo"]):
                with st.expander("📷 View Full Photo", expanded=False):
                    st.image(m["photo"], use_column_width=True, caption=m["name"])
                st.image(m["photo"], width=150)
            else:
                st.markdown("<div style='text-align:center;padding:60px;background:#ecf0f1;border-radius:12px;'>📷 No Photo</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"### {m['name']}")
            st.write(f"📞 **Phone:** {m['phone']}")
            if m.get("email"): st.write(f"📧 **Email:** {m['email']}")
            if m.get("address"): st.write(f"🏠 **Address:** {m['address']}")
            st.write(f"🎂 **Birthday:** {m['birthday']}")
            st.write(f"📅 **Joined:** {m.get('joined', 'N/A')}")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr><p style='text-align:center;color:#7f8c8d;'>Built with ❤️ for RCCG Sunrise Parish 🌅</p>", unsafe_allow_html=True)

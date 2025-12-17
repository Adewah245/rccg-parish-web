import streamlit as st
import json
import requests
from datetime import datetime

# Page config with custom styling
st.set_page_config(
    page_title="RCCG Sunrise Parish",
    layout="wide",
    page_icon="⛪",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Custom header styling */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Body text */
    p, div, span, label {
        font-family: 'Lato', sans-serif !important;
    }
    
    /* Cards for content */
    .content-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 2rem 0;
        animation: fadeInDown 1s ease-out;
    }
    
    /* Church name styling */
    .church-name {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        margin: 1rem 0;
        animation: fadeIn 1.5s ease-out;
    }
    
    .zone-name {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        letter-spacing: 3px;
        animation: fadeIn 2s ease-out;
    }
    
    /* Member cards */
    .member-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .member-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    /* Stats box */
    .stats-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .stats-number {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Message box */
    .message-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: slideInUp 1s ease-out;
    }
    
    /* Search box */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        padding: 1rem 1.5rem !important;
        border: 2px solid #667eea !important;
        font-size: 1.1rem !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white !important;
        color: #333 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: 2px solid #667eea !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        margin: 0.5rem 0 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f8f9ff !important;
        transform: translateX(5px);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stExpander"] {
        background: white;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from { 
            opacity: 0;
            transform: translateY(-30px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Decorative elements */
    .decoration {
        position: fixed;
        pointer-events: none;
        opacity: 0.1;
    }
</style>
""", unsafe_allow_html=True)

# Load data from GitHub
data_url = "https://raw.githubusercontent.com/Adewah245/rccg-parish-data/main/data.json"
photos_base_url = "https://raw.githubusercontent.com/Adewah245/rccg-parish-data/main/photos/"
logo_url = "https://raw.githubusercontent.com/Adewah245/rccg-parish-data/main/logo.png"

try:
    data = requests.get(data_url).json()
    members_list = data.get("members", [])
    messages = data.get("messages", [])
    last_update = data.get("last_update", "Unknown")
except:
    st.error("Unable to load data. Please contact the administrator.")
    st.stop()

# Convert list to dictionary
members = {}
for member in members_list:
    name = member.get("name", "Unknown")
    members[name] = member

# Header with logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(logo_url, width=200)
    except:
        st.markdown("⛪", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Church name
st.markdown("""
<div style="text-align: center;">
    <h1 class="church-name">🏢 RCCG BENUE 2 SUNRISE PARISH</h1>
    <p class="zone-name">YOUNG & ADULTS ZONE</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Latest Message in beautiful box
if messages:
    latest = messages[-1]
    st.markdown(f"""
    <div class="message-box">
        <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">📢 LATEST ANNOUNCEMENT</h3>
        <p style="font-size: 1.3rem; margin: 1rem 0; font-weight: 400;">{latest['text']}</p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin: 0;">📅 {latest['date']}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="message-box">
        <h3 style="margin: 0;">📢 ANNOUNCEMENT</h3>
        <p style="margin: 1rem 0;">No announcements yet. Stay tuned!</p>
    </div>
    """, unsafe_allow_html=True)

# Stats in cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stats-box">
        <p class="stats-number">{len(members)}</p>
        <p class="stats-label">Total Members</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-box" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <p class="stats-number">{len(messages)}</p>
        <p class="stats-label">Messages</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stats-box" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
        <p class="stats-number">⛪</p>
        <p class="stats-label">Growing Together</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Search section
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 🔍 Search Members")
search = st.text_input("", placeholder="Search by name or phone number...", label_visibility="collapsed")

filtered = members
if search:
    search_lower = search.lower()
    filtered = {}
    for name, info in members.items():
        name_match = search_lower in name.lower()
        phone_match = search_lower in info.get("phone", "").lower()
        if name_match or phone_match:
            filtered[name] = info

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Members list
if not filtered:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.warning("No members found matching your search.")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="content-card">', unsafe_allow_html=True)
    st.markdown(f"### 📋 Members Directory ({len(filtered)} members)")
    
    # Sort alphabetically
    sorted_members = sorted(filtered.items(), key=lambda x: x[0].lower())
    
    for i, (name, info) in enumerate(sorted_members, 1):
        with st.expander(f"{i}. {name.title()} • {info.get('phone', 'N/A')}"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Display photo
                photo = info.get('photo', '')
                if photo and photo not in ["Photo copy failed", ""]:
                    photo_url = photos_base_url + photo
                    try:
                        st.image(photo_url, width=150)
                    except:
                        st.markdown("👤<br><small>No photo</small>", unsafe_allow_html=True)
                else:
                    st.markdown("👤<br><small>No photo</small>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**📱 Phone:** {info.get('phone', 'N/A')}")
                st.markdown(f"**📍 Address:** {info.get('address', 'N/A')}")
                if info.get('email'):
                    st.markdown(f"**📧 Email:** {info.get('email')}")
                if info.get('birthday'):
                    st.markdown(f"**🎂 Birthday:** {info.get('birthday')}")
                st.markdown(f"<small>✅ Joined: {info.get('joined', 'Unknown')}</small>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: white; opacity: 0.8;">
    <p>Last updated: {last_update}</p>
    <p>✝️ Managed by Youth President | God bless you!</p>
</div>
""", unsafe_allow_html=True)

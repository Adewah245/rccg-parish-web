import streamlit as st
import json
import requests
from datetime import datetime
import base64

st.set_page_config(
    page_title="Admin Panel - RCCG Parish",
    layout="wide",
    page_icon="🔐"
)

# Custom CSS matching main app
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: white !important;
    }

    .admin-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .photo-preview {
        border: 3px solid #667eea;
        border-radius: 15px;
        padding: 10px;
        background: white;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================
GITHUB_REPO = "Adewah245/rccg-parish-data"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
DATA_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/data.json"
PHOTOS_PATH = "photos/"

# ==================== HELPER FUNCTIONS ====================

def get_file_from_github(path):
    """Get file content from GitHub"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        return base64.b64decode(content['content']).decode('utf-8'), content['sha']
    return None, None

def save_to_github(path, content, message, sha=None):
    """Save file to GitHub"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "message": message,
        "content": base64.b64encode(content.encode() if isinstance(content, str) else content).decode()
    }

    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    return response.status_code in [200, 201]

def upload_photo_to_github(photo_bytes, filename):
    """Upload photo to GitHub"""
    path = f"{PHOTOS_PATH}{filename}"
    
    # Check if photo already exists and get its SHA
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    existing = requests.get(url, headers=headers)
    existing_sha = existing.json().get('sha') if existing.status_code == 200 else None
    
    return save_to_github(path, photo_bytes, f"Upload photo: {filename}", existing_sha)

def load_data():
    """Load data from GitHub"""
    content, sha = get_file_from_github("data.json")
    if content:
        return json.loads(content), sha
    return {"members": [], "messages": [], "last_update": ""}, None

def save_data(data, sha):
    """Save data to GitHub"""
    data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = json.dumps(data, indent=4)
    return save_to_github("data.json", content, "Update data", sha)

# ==================== AUTHENTICATION ====================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="admin-card" style="max-width: 500px; margin: 5rem auto;">', unsafe_allow_html=True)
    st.title("🔐 Admin Login")
    st.markdown("### RCCG Sunrise Parish - Admin Panel")

    password = st.text_input("Enter Admin Password", type="password")

    if st.button("🔓 Login", use_container_width=True):
        if password == st.secrets.get("ADMIN_PASSWORD", "rccg2024"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid password!")

    st.info("💡 Default password: rccg2024")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== MAIN ADMIN PANEL ====================

st.title("🏢 RCCG Parish Admin Panel")
st.caption("Manage members, photos, and announcements")

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("---")

# Check GitHub token
if not GITHUB_TOKEN:
    st.error("⚠️ GitHub token not configured!")
    st.info("""
    **Setup Instructions:**
    1. Go to: https://github.com/settings/tokens
    2. Generate new token with 'repo' permission
    3. Add to Streamlit secrets: `GITHUB_TOKEN = "your_token"`
    """)
    st.stop()

# Load data
try:
    data, sha = load_data()
    members_list = data.get("members", [])
    messages = data.get("messages", [])
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ==================== TABS ====================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "➕ Add Member", 
    "✏️ Edit Member", 
    "📋 View Members", 
    "🎂 Birthdays", 
    "📢 Announcements", 
    "⚙️ Settings"
])

# ==================== TAB 1: ADD MEMBER ====================
with tab1:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.header("➕ Add New Member")

    with st.form("add_member_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *", placeholder="e.g., John Doe")
            phone = st.text_input("Phone Number *", placeholder="e.g., 09012345678")
            email = st.text_input("Email", placeholder="e.g., john@example.com")

        with col2:
            address = st.text_input("Address *", placeholder="e.g., 123 Main Street")
            birthday = st.text_input("Birthday", placeholder="DD-MM-YYYY (e.g., 15-05-1990)")
            photo = st.file_uploader("📸 Upload Photo", type=['jpg', 'jpeg', 'png', 'gif'])

        # Photo preview
        if photo:
            st.markdown("**Photo Preview:**")
            st.image(photo, width=200, caption="Preview")

        submitted = st.form_submit_button("➕ Add Member", use_container_width=True)

        if submitted:
            if not name or not phone or not address:
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                photo_filename = ""
                if photo:
                    safe_name = name.lower().replace(" ", "_")
                    ext = photo.name.split(".")[-1]
                    photo_filename = f"{safe_name}_{phone}.{ext}"

                    with st.spinner("Uploading photo..."):
                        if upload_photo_to_github(photo.read(), photo_filename):
                            st.success(f"✅ Photo uploaded: {photo_filename}")
                        else:
                            st.error("❌ Photo upload failed")
                            photo_filename = "Photo upload failed"

                new_member = {
                    "name": name.lower(),
                    "phone": phone,
                    "address": address,
                    "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

                if email:
                    new_member["email"] = email
                if birthday:
                    new_member["birthday"] = birthday
                if photo_filename:
                    new_member["photo"] = photo_filename

                members_list.append(new_member)
                data["members"] = members_list

                with st.spinner("Saving..."):
                    if save_data(data, sha):
                        st.success(f"✅ Member '{name}' added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to save")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: EDIT MEMBER (NEW!) ====================
with tab2:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.header("✏️ Edit Member Information & Photo")
    
    if not members_list:
        st.info("No members to edit. Add members first!")
    else:
        # Select member to edit
        member_names = [f"{m.get('name', 'Unknown').title()} - {m.get('phone', 'N/A')}" for m in members_list]
        selected_name = st.selectbox("Select Member to Edit", member_names)
        
        if selected_name:
            # Find the selected member
            selected_idx = member_names.index(selected_name)
            member = members_list[selected_idx]
            
            st.markdown("---")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Current Photo")
                if member.get('photo') and member['photo'] != "Photo upload failed":
                    photo_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{PHOTOS_PATH}{member['photo']}"
                    try:
                        st.image(photo_url, width=200)
                    except:
                        st.write("📷 Photo unavailable")
                else:
                    st.write("👤 No photo")
                
                st.markdown("---")
                
                # Upload new photo
                st.subheader("📸 Change Photo")
                new_photo = st.file_uploader("Upload New Photo", type=['jpg', 'jpeg', 'png', 'gif'], key="edit_photo")
                
                if new_photo:
                    st.image(new_photo, width=200, caption="New Photo Preview")
                    
                    if st.button("⬆️ Upload New Photo", use_container_width=True):
                        safe_name = member.get('name', 'unknown').lower().replace(" ", "_")
                        ext = new_photo.name.split(".")[-1]
                        photo_filename = f"{safe_name}_{member.get('phone', '')}.{ext}"
                        
                        with st.spinner("Uploading photo..."):
                            if upload_photo_to_github(new_photo.read(), photo_filename):
                                member['photo'] = photo_filename
                                data["members"] = members_list
                                if save_data(data, sha):
                                    st.success("✅ Photo updated successfully!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save")
                            else:
                                st.error("❌ Photo upload failed")
            
            with col2:
                st.subheader("Edit Information")
                
                with st.form("edit_member_form"):
                    new_name = st.text_input("Full Name *", value=member.get('name', ''))
                    new_phone = st.text_input("Phone Number *", value=member.get('phone', ''))
                    new_email = st.text_input("Email", value=member.get('email', ''))
                    new_address = st.text_input("Address *", value=member.get('address', ''))
                    new_birthday = st.text_input("Birthday", value=member.get('birthday', ''), placeholder="DD-MM-YYYY")
                    
                    save_changes = st.form_submit_button("💾 Save Changes", use_container_width=True)
                    
                    if save_changes:
                        if not new_name or not new_phone or not new_address:
                            st.error("❌ Please fill in all required fields")
                        else:
                            member['name'] = new_name.lower()
                            member['phone'] = new_phone
                            member['address'] = new_address
                            
                            if new_email:
                                member['email'] = new_email
                            if new_birthday:
                                member['birthday'] = new_birthday
                            
                            data["members"] = members_list
                            
                            with st.spinner("Saving..."):
                                if save_data(data, sha):
                                    st.success("✅ Member information updated!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 3: VIEW MEMBERS ====================
with tab3:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.header("📋 Members Directory")
    st.info(f"Total Members: {len(members_list)}")

    search = st.text_input("🔍 Search", placeholder="Search by name or phone")

    filtered = members_list
    if search:
        search_lower = search.lower()
        filtered = [m for m in members_list if
                   search_lower in m.get("name", "").lower() or
                   search_lower in m.get("phone", "")]

    sorted_members = sorted(filtered, key=lambda x: x.get("name", "").lower())

    st.markdown(f"**Showing {len(sorted_members)} member(s)**")

    for idx, member in enumerate(sorted_members):
        with st.expander(f"👤 {member.get('name', 'Unknown').title()} - {member.get('phone', 'N/A')}"):
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                if member.get('photo') and member['photo'] != "Photo upload failed":
                    photo_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{PHOTOS_PATH}{member['photo']}"
                    try:
                        st.image(photo_url, width=150)
                    except:
                        st.write("📷 Photo unavailable")
                else:
                    st.write("👤 No photo")

            with col2:
                st.write(f"**📱 Phone:** {member.get('phone', 'N/A')}")
                st.write(f"**📍 Address:** {member.get('address', 'N/A')}")
                st.write(f"**📧 Email:** {member.get('email', 'N/A')}")
                st.write(f"**🎂 Birthday:** {member.get('birthday', 'N/A')}")
                st.caption(f"✅ Joined: {member.get('joined', 'Unknown')}")

            with col3:
                if st.button(f"🗑️ Delete", key=f"del_{idx}"):
                    if st.session_state.get(f"confirm_del_{idx}"):
                        members_list.remove(member)
                        data["members"] = members_list
                        if save_data(data, sha):
                            st.success("✅ Deleted")
                            st.rerun()
                    else:
                        st.session_state[f"confirm_del_{idx}"] = True
                        st.warning("Click again to confirm")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 4: BIRTHDAYS ====================
with tab4:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.header("🎂 Upcoming Birthdays (Next 30 Days)")

    today = datetime.now()
    upcoming = []

    for m in members_list:
        birthday = m.get("birthday", "")
        if not birthday:
            continue
        try:
            bday = datetime.strptime(birthday, "%d-%m-%Y")
            this_year = bday.replace(year=today.year)
            if this_year < today:
                this_year = this_year.replace(year=today.year + 1)
            days = (this_year - today).days
            if 0 <= days <= 30:
                upcoming.append((days, m.get("name", "Unknown"), this_year.strftime("%d %B"), m.get("phone", "")))
        except:
            continue

    if not upcoming:
        st.info("🎂 No birthdays in the next 30 days")
    else:
        upcoming.sort()
        for days, name, date, phone in upcoming:
            if days == 0:
                st.success(f"🎉 **{name.title()}** - TODAY! ({phone})")
            elif days == 1:
                st.warning(f"🎂 **{name.title()}** - {date} (Tomorrow!) ({phone})")
            else:
                st.info(f"🎂 **{name.title()}** - {date} ({days} days) ({phone})")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 5: ANNOUNCEMENTS ====================
with tab5:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.header("📢 Parish Announcements")

    if messages:
        st.subheader("Current Messages")
        for idx, msg in enumerate(reversed(messages)):
            with st.expander(f"📅 {msg['date']}"):
                st.write(msg['text'])
                if st.button("🗑️ Delete", key=f"msg_{idx}"):
                    messages.remove(msg)
                    data["messages"] = messages
                    if save_data(data, sha):
                        st.success("✅ Deleted")
                        st.rerun()

    st.markdown("---")
    st.subheader("📝 Post New Announcement")

    with st.form("announcement_form"):
        message_text = st.text_area("Message", placeholder="Enter announcement...", height=150)
        submit_msg = st.form_submit_button("📢 Post", use_container_width=True)

        if submit_msg and message_text:
            new_message = {
                "text": message_text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            messages.append(new_message)
            data["messages"] = messages

            if save_data(data, sha):
                st.success("✅ Posted!")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 6: SETTINGS ====================
with tab6:
    st.markdown('<div class="admin-card">', unsafe_allow_html=True)
    st.header("⚙️ Settings")

    # Logo Upload
    st.subheader("🎨 Church Logo")

    col1, col2 = st.columns([1, 2])

    with col1:
        logo_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/logo.png"
        try:
            st.image(logo_url, width=200)
        except:
            st.info("No logo yet")

    with col2:
        logo_file = st.file_uploader("Upload Logo", type=['png', 'jpg', 'jpeg'], key="logo")

        if logo_file:
            st.image(logo_file, width=200, caption="Preview")

            if st.button("⬆️ Upload Logo"):
                with st.spinner("Uploading..."):
                    ext = logo_file.name.split(".")[-1]
                    logo_filename = f"logo.{ext}"

                    # Check if exists
                    logo_url_api = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{logo_filename}"
                    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                    existing = requests.get(logo_url_api, headers=headers)
                    existing_sha = existing.json().get('sha') if existing.status_code == 200 else None

                    logo_bytes = logo_file.read()
                    if save_to_github(logo_filename, logo_bytes, "Update logo", existing_sha):
                        st.success("✅ Logo uploaded!")
                        st.balloons()
                    else:
                        st.error("❌ Failed")

    st.markdown("---")

    # Stats
    st.subheader("📊 Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Members", len(members_list))
    with col2:
        st.metric("Announcements", len(messages))
    with col3:
        st.metric("Last Updated", data.get("last_update", "Unknown"))

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p style="text-align: center; color: white;">✝️ God bless your ministry!</p>', unsafe_allow_html=True)

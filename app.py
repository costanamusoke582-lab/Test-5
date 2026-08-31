import streamlit as st
from supabase import create_client, Client

# --- PAGE SETUP ---
st.set_page_config(page_title="Course Platform", layout="wide")

# --- DATABASE CONNECTION ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase: Client = init_connection()
except Exception:
    st.warning("Database not connected yet. Please configure your secrets.toml file.")

# --- AUTHENTICATION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    # In a production app, this connects to Supabase Auth. 
    # For now, it's a simple gateway to block unauthenticated users.
    if st.session_state.email and st.session_state.password:
        st.session_state.authenticated = True

if not st.session_state.authenticated:
    st.title("Student Login")
    st.text_input("Email", key="email")
    st.text_input("Password", type="password", key="password")
    st.button("Log In", on_click=login)
    st.stop() # Stops the rest of the app from loading until logged in

# --- MAIN DASHBOARD ---
st.title("📚 Student Resource Portal")
st.write("Welcome! Use the sidebar to browse courses or search for specific topics below.")

# --- SEARCH BAR ---
search_query = st.text_input("🔍 Search for a course or lesson title...")
if search_query:
    st.subheader(f"Search Results for: {search_query}")
    # Example Supabase query:
    # response = supabase.table("lessons").select("*").ilike("lesson_title", f"%{search_query}%").execute()
    st.info("The database will return matching YouTube links and Drive PDFs here.")

st.divider()

# --- COURSE BROWSE TREE (SIDEBAR) ---
st.sidebar.header("Browse Curriculum")

# 1. Select Program
program = st.sidebar.selectbox(
    "Select Program",
    ["KIU/Health Sciences/BMS", "Nursing", "Pharmacy"]
)

# 2. Select Year & Semester
year_sem = st.sidebar.selectbox(
    "Select Semester",
    ["Year 2 / Semester 1", "Year 3 / Semester 1", "Year 3 / Semester 2"]
)

# 3. Select Course (Populated based on the above choices)
course = st.sidebar.selectbox(
    "Select Course",
    ["Pathophysiology", "Pharmacology", "Histopathology", "Physiology"]
)

# --- DISPLAYING RESOURCES ---
st.subheader(f"Current Course: {course}")

# Mocking the data layout for visual understanding
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎥 Video Lectures")
    # In reality, this data is pulled from the 'resources' table where link_kind = 'youtube'
    st.button("Play: Epilepsy 2")
    st.button("Play: Meningitis")
    st.button("Play: Vasoactive Peptides")

with col2:
    st.markdown("### 📝 Notes & Questions")
    # Pulled from 'resources' where link_kind = 'drive_Notes' or 'drive_questions'
    st.button("Open: Pathophysiology Drive Folder")
    st.button("Download: Practice Questions")

# Logout button
st.sidebar.divider()
if st.sidebar.button("Log Out"):
    st.session_state.authenticated = False
    st.rerun()

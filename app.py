import streamlit as st
import json
import pandas as pd
import io
from streamlit_option_menu import option_menu
import re

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.email = ""

# Load the career roadmap data
with open("roadmap_data.json", "r", encoding="utf-8") as file:
    roadmap_data = json.load(file)

# Extract the available careers from the JSON file
available_careers = list(roadmap_data.keys())

# Set page configuration
st.set_page_config(
    page_title="YuvaPath - Career Guidance",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for vibrant light-themed UI
st.markdown(
    """
    <style>
    /* Main app background with pastel gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e9fd 50%, #d9e4ff 100%);
        color: #2c3e50;
        font-family: 'Inter', 'Arial', sans-serif;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: #ffffff;
        border-right: 2px solid #ff6b6b;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    .css-1d391kg .stSelectbox, .css-1d391kg .stTextInput {
        background: #f9f9f9;
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 10px;
    }
    .css-1d391kg .stSelectbox label, .css-1d391kg .stTextInput label {
        color: #ff6b6b;
        font-weight: 600;
        font-size: 1.1em;
    }

    /* Title and header styling */
    h1 {
        color: #ff6b6b;
        font-size: 2.8em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    h3 {
        color: #e84393;
        font-size: 1.6em;
        font-weight: 600;
    }

    /* Card styling for phases */
    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #dfe6e9;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-3px);
    }

    /* Resource link styling */
    .resource-link {
        color: #ff6b6b;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    .resource-link:hover {
        color: #e84393;
        text-decoration: underline;
    }

    /* Selectbox and text input styling */
    .stSelectbox, .stTextInput {
        background: #f9f9f9;
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        padding: 10px;
    }
    .stSelectbox label, .stTextInput label {
        color: #ff6b6b;
        font-weight: 600;
    }

    /* Success message styling */
    .stSuccess {
        background: #e6fffa;
        border-left: 5px solid #2ed573;
        border-radius: 10px;
        padding: 15px;
        color: #2c3e50;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #636e72;
        font-size: 0.95em;
        margin-top: 30px;
        padding: 20px;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }

    /* Divider styling */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #ff6b6b, transparent);
        margin: 25px 0;
    }

    /* Vibrant text for emphasis */
    .vibrant-text {
        color: #ff6b6b;
        font-weight: 600;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Sign-in functionality with email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def authenticate(email, password):
    # Allow any valid email with non-empty password for demo purposes
    # In production, integrate with a secure backend authentication system
    return is_valid_email(email) and len(password) >= 6

# Sidebar with navigation menu
with st.sidebar:
    st.markdown("<h3 style='color: #ff6b6b;'>🚀 App Settings</h3>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Sign In", "Settings"],
        icons=["lock", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"background-color": "#ffffff", "border": "2px solid #ff6b6b", "border-radius": "10px"},
            "nav-link": {"color": "#2c3e50", "--hover-color": "#ff6b6b"},
            "nav-link-selected": {"background-color": "#ff6b6b", "color": "#ffffff"},
        }
    )

    if selected == "Sign In":
        if not st.session_state.authenticated:
            st.markdown("<h3 class='vibrant-text'>🔒 Sign In</h3>", unsafe_allow_html=True)
            email = st.text_input("Email", key="email_input")
            password = st.text_input("Password", type="password", key="password_input")
            if st.button("Sign In"):
                if authenticate(email, password):
                    st.session_state.authenticated = True
                    st.session_state.email = email
                    st.success(f"Welcome, {email}! You are now signed in.")
                else:
                    st.error("Invalid email or password (password must be at least 6 characters).")
        else:
            st.markdown(f"<p class='vibrant-text'>Welcome, {st.session_state.email}!</p>", unsafe_allow_html=True)
            if st.button("Sign Out"):
                st.session_state.authenticated = False
                st.session_state.email = ""
                st.success("You have signed out.")
    
    if selected == "Settings":
        language = st.selectbox("Choose Language:", ["English", "Hindi", "Tamil", "Telugu"], key="language")

# App title and subtitle
st.markdown(
    """
    <h1>🚀 YuvaPath - Career Guidance</h1>
    <p style='text-align: center; color: #636e72; font-size: 1.2em;'>
        Discover your career path with vibrant resources & personalized roadmaps.
    </p>
    """,
    unsafe_allow_html=True
)

# Career selection (only shown if authenticated)
if st.session_state.authenticated:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='vibrant-text'>🌟 Select Your Career Path</h3>", unsafe_allow_html=True)
    career_choice = st.selectbox("Select Career:", available_careers, key="career")
    st.markdown("</div>", unsafe_allow_html=True)

    # Display selected career details
    if career_choice:
        career_data = roadmap_data[career_choice]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3 class='vibrant-text'>📌 {career_data['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>💰 Expected Salary:</strong> {career_data['salary']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>⏳ Learning Duration:</strong> {career_data['duration']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3 class='vibrant-text'>📚 Career Roadmap:</h3>", unsafe_allow_html=True)

        for phase, resources in career_data["phases"].items():
            st.markdown(f"<div class='card'><h3 class='vibrant-text'>🔹 {phase}</h3>", unsafe_allow_html=True)
            for resource in resources:
                st.markdown(
                    f"- <a href='{resource['link']}' class='resource-link' target='_blank'>{resource['name']}</a> ({resource['platform']})",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        # Project Ideas Section
        if "project_ideas" in career_data:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h3 class='vibrant-text'>🚀 Project Ideas:</h3>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            for project in career_data["project_ideas"]:
                st.markdown(
                    f"- **{project['title']}**: {project['description']} "
                    f"(*Difficulty: {project['difficulty']}*)",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        # Download Roadmap as Markdown
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3 class='vibrant-text'>📥 Download Your Roadmap</h3>", unsafe_allow_html=True)
        roadmap_content = f"# {career_data['title']} Roadmap\n\n"
        roadmap_content += f"**Expected Salary:** {career_data['salary']}\n\n"
        roadmap_content += f"**Learning Duration:** {career_data['duration']}\n\n"
        roadmap_content += "## Roadmap Phases\n"
        for phase, resources in career_data["phases"].items():
            roadmap_content += f"### {phase}\n"
            for resource in resources:
                roadmap_content += f"- [{resource['name']}]({resource['link']}) ({resource['platform']})\n"
        if "project_ideas" in career_data:
            roadmap_content += "\n## Project Ideas\n"
            for project in career_data["project_ideas"]:
                roadmap_content += f"- **{project['title']}**: {project['description']} (*Difficulty: {project['difficulty']}*)\n"
        roadmap_content += "\n*Generated by YuvaPath - Career Guidance*"
        
        buffer = io.StringIO()
        buffer.write(roadmap_content)
        st.download_button(
            label="Download Roadmap",
            data=buffer.getvalue(),
            file_name=f"{career_choice}_roadmap.md",
            mime="text/markdown"
        )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.success("✅ Chart your course through each phase to reach your career goal!")
else:
    st.warning("Please sign in to access your career path!")

# Footer
st.markdown(
    "<div class='footer'>🚀 <em>YuvaPath is your career guide — Explore, Learn, and Thrive!</em></div>",
    unsafe_allow_html=True
)

import streamlit as st
import json

# Load the career roadmap data
with open("roadmap_data.json", "r", encoding="utf-8") as file:
    roadmap_data = json.load(file)

# Extract the available careers from the JSON file
available_careers = list(roadmap_data.keys())

# Set page configuration
st.set_page_config(
    page_title="YuvaPath - Cosmic Career Guidance",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for galaxy-themed UI
st.markdown(
    """
    <style>
    /* Main app background with galaxy effect */
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #2c3e50 100%);
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
        background-size: cover;
        color: #e0e1dd;
        font-family: 'Orbitron', 'Arial', sans-serif;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(10, 27, 42, 0.9);
        border-right: 2px solid #00d4ff;
        padding: 20px;
        backdrop-filter: blur(5px);
    }
    .css-1d391kg .stSelectbox {
        background: rgba(52, 73, 94, 0.8);
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 8px;
    }
    .css-1d391kg .stSelectbox label {
        color: #00d4ff;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
    }

    /* Title and header styling */
    h1 {
        color: #00d4ff;
        font-size: 2.8em;
        font-weight: 700;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.7);
        margin-bottom: 10px;
    }
    h3 {
        color: #778beb;
        font-size: 1.6em;
        font-weight: 600;
        text-shadow: 0 0 5px rgba(119, 139, 235, 0.5);
    }

    /* Card styling for phases */
    .card {
        background: rgba(27, 39, 59, 0.85);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 212, 255, 0.2);
        border: 1px solid #415a77;
    }

    /* Resource link styling */
    .resource-link {
        color: #54a0ff;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    .resource-link:hover {
        color: #00d4ff;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.7);
    }

    /* Selectbox styling */
    .stSelectbox {
        background: rgba(52, 73, 94, 0.8);
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 8px;
    }
    .stSelectbox label {
        color: #00d4ff;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
    }

    /* Success message styling */
    .stSuccess {
        background: rgba(46, 204, 113, 0.2);
        border-left: 5px solid #2ecc71;
        border-radius: 10px;
        padding: 20px;
        color: #e0e1dd;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.3);
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #a4b0be;
        font-size: 0.95em;
        margin-top: 40px;
        padding: 25px;
        background: rgba(10, 27, 42, 0.9);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }

    /* Divider styling */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(to right, transparent, #00d4ff, transparent);
        margin: 30px 0;
    }

    /* Glowing text for emphasis */
    .glow-text {
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.7);
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Sidebar with language selection
with st.sidebar:
    st.markdown("<h3 style='color: #00d4ff;'>🌌 Cosmic Settings</h3>", unsafe_allow_html=True)
    language = st.selectbox("Choose Language:", ["English", "Hindi", "Tamil", "Telugu"], key="language")

# App title and subtitle
st.markdown(
    """
    <h1>🌌 YuvaPath - Cosmic Career Guidance</h1>
    <p style='text-align: center; color: #a4b0be; font-size: 1.2em;'>
        Navigate your career path through the stars with free resources & personalized roadmaps.
    </p>
    """,
    unsafe_allow_html=True
)

# Career selection
st.markdown("<div class='card'>", unsafe_allow_html=True)
career_choice = st.selectbox("💫 Select Your Career Constellation:", available_careers, key="career")
st.markdown("</div>", unsafe_allow_html=True)

# Display selected career details
if career_choice:
    career_data = roadmap_data[career_choice]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3 class='glow-text'>📌 {career_data['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>💰 Expected Salary:</strong> {career_data['salary']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>⏳ Learning Duration:</strong> {career_data['duration']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 class='glow-text'>📚 Cosmic Career Roadmap:</h3>", unsafe_allow_html=True)

    for phase, resources in career_data["phases"].items():
        st.markdown(f"<div class='card'><h3 class='glow-text'>🔹 {phase}</h3>", unsafe_allow_html=True)
        for resource in resources:
            st.markdown(
                f"- <a href='{resource['link']}' class='resource-link' target='_blank'>{resource['name']}</a> ({resource['platform']})",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("✅ Chart your course through each phase to reach your stellar career goal!")

# Footer
st.markdown(
    "<div class='footer'>💡 <em>YuvaPath is your cosmic mentor — Explore, Learn, and Conquer the Stars!</em></div>",
    unsafe_allow_html=True
)

import streamlit as st
import json

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

# Custom CSS for UI beautification
st.markdown(
    """
    <style>
    /* Main app background and text */
    .stApp {
        background-color: #f5f7fa;
        color: #2c3e50;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2c3e50;
        color: #ffffff;
        padding: 20px;
    }
    .css-1d391kg .stSelectbox {
        background-color: #34495e;
        border-radius: 8px;
        padding: 5px;
    }
    .css-1d391kg .stSelectbox label {
        color: #ffffff;
        font-weight: bold;
    }

    /* Title and header styling */
    h1 {
        color: #2c3e50;
        font-size: 2.5em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    h3 {
        color: #34495e;
        font-size: 1.5em;
        font-weight: 600;
    }

    /* Card styling for phases */
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
    }

    /* Resource link styling */
    .resource-link {
        color: #3498db;
        text-decoration: none;
        font-weight: 500;
    }
    .resource-link:hover {
        color: #2980b9;
        text-decoration: underline;
    }

    /* Selectbox styling */
    .stSelectbox {
        background-color: #ffffff;
        border: 2px solid #3498db;
        border-radius: 8px;
        padding: 5px;
    }
    .stSelectbox label {
        color: #2c3e50;
        font-weight: bold;
    }

    /* Success message styling */
    .stSuccess {
        background-color: #e8f4f8;
        border-left: 5px solid #2ecc71;
        border-radius: 8px;
        padding: 15px;
        color: #2c3e50;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9em;
        margin-top: 30px;
        padding: 20px;
        background-color: #ecf0f1;
        border-radius: 8px;
    }

    /* Divider styling */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #3498db, transparent);
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with language selection
with st.sidebar:
    st.markdown("<h3 style='color: #ffffff;'>🌐 Settings</h3>", unsafe_allow_html=True)
    language = st.selectbox("Choose Language:", ["English", "Hindi", "Tamil", "Telugu"], key="language")

# App title and subtitle
st.markdown(
    """
    <h1>🎯 YuvaPath - AI Career Guidance</h1>
    <p style='text-align: center; color: #7f8c8d; font-size: 1.1em;'>
        Helping youth find the right career path with free resources & personalized roadmaps.
    </p>
    """,
    unsafe_allow_html=True
)

# Career selection
st.markdown("<div class='card'>", unsafe_allow_html=True)
career_choice = st.selectbox("💼 Select Your Career Interest:", available_careers, key="career")
st.markdown("</div>", unsafe_allow_html=True)

# Display selected career details
if career_choice:
    career_data = roadmap_data[career_choice]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>📌 {career_data['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>💰 Expected Salary:</strong> {career_data['salary']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>⏳ Learning Duration:</strong> {career_data['duration']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>📚 Career Roadmap:</h3>", unsafe_allow_html=True)

    for phase, resources in career_data["phases"].items():
        st.markdown(f"<div class='card'><h3>🔹 {phase}</h3>", unsafe_allow_html=True)
        for resource in resources:
            st.markdown(
                f"- <a href='{resource['link']}' class='resource-link' target='_blank'>{resource['name']}</a> ({resource['platform']})",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("✅ Follow each phase step-by-step to reach your career goal!")

# Footer
st.markdown(
    "<div class='footer'>💡 <em>YuvaPath is your personal mentor — Learn, Grow, and Succeed!</em></div>",
    unsafe_allow_html=True
)

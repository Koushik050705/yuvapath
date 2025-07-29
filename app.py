import streamlit as st
import json
import pandas as pd
import plotly.express as px
from io import StringIO
import os

# Load the career roadmap data
with open("roadmap_data.json", "r", encoding="utf-8") as file:
    roadmap_data = json.load(file)

# Extract the available careers from the JSON file
available_careers = list(roadmap_data.keys())

# Mock user database (JSON file for persistent storage)
USER_DB = "user_data.json"
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

def load_user_data():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=4)

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "progress" not in st.session_state:
    st.session_state.progress = {career: {phase: [False] * len(resources) for phase, resources in roadmap_data[career]["phases"].items()} for career in available_careers}
if "ratings" not in st.session_state:
    st.session_state.ratings = {career: {phase: [0] * len(resources) for phase, resources in roadmap_data[career]["phases"].items()} for career in available_careers}
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

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
    .stApp {
        background: %s;
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
        background-size: cover;
        color: %s;
        font-family: 'Orbitron', 'Arial', sans-serif;
        transition: all 0.3s ease;
    }
    .css-1d391kg {
        background: %s;
        border-right: 2px solid #00d4ff;
        padding: 20px;
        backdrop-filter: blur(5px);
    }
    .css-1d391kg .stSelectbox, .css-1d391kg .stTextInput {
        background: %s;
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 8px;
    }
    .css-1d391kg .stSelectbox label, .css-1d391kg .stTextInput label {
        color: #00d4ff;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
    }
    h1 {
        color: #00d4ff;
        font-size: 2.8em;
        font-weight: 700;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.7);
        margin-bottom: 10px;
    }
    h3 {
        color: %s;
        font-size: 1.6em;
        font-weight: 600;
        text-shadow: 0 0 5px rgba(119, 139, 235, 0.5);
    }
    .card {
        background: %s;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 212, 255, 0.2);
        border: 1px solid #415a77;
    }
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
    .stSelectbox, .stTextInput {
        background: %s;
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 8px;
    }
    .stSelectbox label, .stTextInput label {
        color: #00d4ff;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
    }
    .stSuccess {
        background: rgba(46, 204, 113, 0.2);
        border-left: 5px solid #2ecc71;
        border-radius: 10px;
        padding: 20px;
        color: %s;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.3);
    }
    .footer {
        text-align: center;
        color: %s;
        font-size: 0.95em;
        margin-top: 40px;
        padding: 25px;
        background: %s;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(to right, transparent, #00d4ff, transparent);
        margin: 30px 0;
    }
    .glow-text {
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.7);
    }
    .progress-bar {
        background: %s;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        background: #00d4ff;
        height: 100%;
        transition: width 0.5s ease;
    }
    @media (max-width: 768px) {
        h1 {
            font-size: 2em;
        }
        .card {
            padding: 15px;
            margin: 10px 0;
        }
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """ % (
        "linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #2c3e50 100%)" if st.session_state.theme == "dark" else "#e6f0fa",
        "#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50",
        "rgba(10, 27, 42, 0.9)" if st.session_state.theme == "dark" else "rgba(52, 73, 94, 0.9)",
        "rgba(52, 73, 94, 0.8)" if st.session_state.theme == "dark" else "rgba(200, 214, 229, 0.8)",
        "#778beb" if st.session_state.theme == "dark" else "#2c3e50",
        "rgba(27, 39, 59, 0.85)" if st.session_state.theme == "dark" else "#ffffff",
        "rgba(52, 73, 94, 0.8)" if st.session_state.theme == "dark" else "rgba(200, 214, 229, 0.8)",
        "#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50",
        "#a4b0be" if st.session_state.theme == "dark" else "#7f8c8d",
        "rgba(10, 27, 42, 0.9)" if st.session_state.theme == "dark" else "rgba(236, 240, 241, 0.9)",
        "rgba(52, 73, 94, 0.8)" if st.session_state.theme == "dark" else "rgba(200, 214, 229, 0.8)"
    ),
    unsafe_allow_html=True
)

# Sidebar with user authentication, settings, and features
with st.sidebar:
    st.markdown("<h3 style='color: #00d4ff;'>🌌 Cosmic Hub</h3>", unsafe_allow_html=True)
    
    # User authentication
    if not st.session_state.user:
        st.markdown("<h4 style='color: #00d4ff;'>Login</h4>", unsafe_allow_html=True)
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")
        if st.button("Login"):
            user_data = load_user_data()
            if username in user_data and user_data[username]["password"] == password:
                st.session_state.user = username
                st.session_state.progress = user_data[username].get("progress", st.session_state.progress)
                st.session_state.ratings = user_data[username].get("ratings", st.session_state.ratings)
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials. Register below.")
        st.markdown("<h4 style='color: #00d4ff;'>Register</h4>", unsafe_allow_html=True)
        new_username = st.text_input("New Username", key="new_username")
        new_password = st.text_input("New Password", type="password", key="new_password")
        if st.button("Register"):
            user_data = load_user_data()
            if new_username in user_data:
                st.error("Username already exists.")
            else:
                user_data[new_username] = {"password": new_password, "progress": st.session_state.progress, "ratings": st.session_state.ratings}
                save_user_data(user_data)
                st.success("Registered successfully! Please login.")
    else:
        st.markdown(f"<p style='color: #00d4ff;'>Welcome, {st.session_state.user}!</p>", unsafe_allow_html=True)
        if st.button("Logout"):
            user_data = load_user_data()
            user_data[st.session_state.user] = {"password": user_data[st.session_state.user]["password"], "progress": st.session_state.progress, "ratings": st.session_state.ratings}
            save_user_data(user_data)
            st.session_state.user = None
            st.success("Logged out successfully!")

    # Language and theme settings
    language = st.selectbox("Choose Language:", ["English", "Hindi", "Tamil", "Telugu"], key="language")
    theme = st.selectbox("Theme:", ["Dark (Galaxy)", "Light"], key="theme")
    st.session_state.theme = "dark" if theme == "Dark (Galaxy)" else "light"
    
    # Search resources
    st.markdown("<h4 style='color: #00d4ff;'>🔍 Search Resources</h4>", unsafe_allow_html=True)
    search_query = st.text_input("Search by name or platform:", key="search")
    
    # Feedback form
    st.markdown("<h4 style='color: #00d4ff;'>📝 Feedback</h4>", unsafe_allow_html=True)
    feedback = st.text_area("Share your suggestions:", key="feedback")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter feedback before submitting.")
    
    # Email subscription
    st.markdown("<h4 style='color: #00d4ff;'>📧 Subscribe to Updates</h4>", unsafe_allow_html=True)
    email = st.text_input("Enter your email:", key="email")
    if st.button("Subscribe"):
        if email:
            st.success("Subscribed successfully! You'll receive cosmic career tips!")
        else:
            st.warning("Please enter a valid email.")

# App title and subtitle
st.markdown(
    """
    <h1>🌌 YuvaPath - Cosmic Career Guidance</h1>
    <p style='text-align: center; color: %s; font-size: 1.2em;'>
        Navigate your career path through the stars with free resources & personalized roadmaps.
    </p>
    """ % ("#a4b0be" if st.session_state.theme == "dark" else "#7f8c8d"),
    unsafe_allow_html=True
)

# Career quiz
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3 class='glow-text'>🚀 Career Quiz</h3>", unsafe_allow_html=True)
with st.form("quiz_form"):
    st.markdown("<p>Answer these questions to find your ideal career path:</p>", unsafe_allow_html=True)
    tech_interest = st.slider("How interested are you in technology? (1=Low, 5=High)", 1, 5, 3, key="tech_interest")
    business_interest = st.slider("How interested are you in business/management? (1=Low, 5=High)", 1, 5, 3, key="business_interest")
    science_interest = st.slider("How interested are you in science/research? (1=Low, 5=High)", 1, 5, 3, key="science_interest")
    submitted = st.form_submit_button("Get Recommendation")
    if submitted:
        scores = {"ai": tech_interest, "web development": tech_interest, "data science": tech_interest + science_interest,
                  "cybersecurity": tech_interest, "cloud computing": tech_interest, "bcom": business_interest,
                  "law": business_interest, "bsc": science_interest, "mba": business_interest}
        recommended_career = max(scores, key=scores.get)
        st.markdown(f"<p class='glow-text'>Recommended Career: <strong>{roadmap_data[recommended_career]['title']}</strong></p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Career comparison chart using Plotly
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3 class='glow-text'>📊 Career Salary Comparison</h3>", unsafe_allow_html=True)
salary_data = {
    career: [int(s.replace("₹", "").split("–")[0]), int(s.replace("₹", "").split("–")[1].replace(" LPA", ""))]
    for career, data in roadmap_data.items()
}
df = pd.DataFrame({
    "Career": [roadmap_data[career]["title"] for career in available_careers],
    "Min Salary (LPA)": [salary_data[career][0] for career in available_careers],
    "Max Salary (LPA)": [salary_data[career][1] for career in available_careers]
})
fig = px.bar(
    df,
    x="Career",
    y=["Min Salary (LPA)", "Max Salary (LPA)"],
    barmode="group",
    title="Career Salary Comparison",
    labels={"value": "Salary (LPA)", "variable": "Salary Type"},
    color_discrete_map={"Min Salary (LPA)": "#00d4ff", "Max Salary (LPA)": "#778beb"}
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50",
    title_font_color="#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50",
    xaxis_title_font_color="#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50",
    yaxis_title_font_color="#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50",
    legend_font_color="#e0e1dd" if st.session_state.theme == "dark" else "#2c3e50"
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

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
    
    # Download roadmap button
    roadmap_text = f"# {career_data['title']}\n\n**Salary:** {career_data['salary']}\n**Duration:** {career_data['duration']}\n\n## Roadmap\n"
    for phase, resources in career_data["phases"].items():
        roadmap_text += f"\n### {phase}\n"
        for resource in resources:
            roadmap_text += f"- [{resource['name']}]({resource['link']}) ({resource['platform']})\n"
    roadmap_buffer = StringIO(roadmap_text)
    st.download_button(
        label="📥 Download Roadmap",
        data=roadmap_buffer.getvalue(),
        file_name=f"{career_choice}_roadmap.md",
        mime="text/markdown"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 class='glow-text'>📚 Cosmic Career Roadmap:</h3>", unsafe_allow_html=True)

    # Filter resources based on search query
    filtered_phases = career_data["phases"]
    if search_query:
        filtered_phases = {}
        for phase, resources in career_data["phases"].items():
            filtered_resources = [
                res for res in resources
                if search_query.lower() in res["name"].lower() or search_query.lower() in res["platform"].lower()
            ]
            if filtered_resources:
                filtered_phases[phase] = filtered_resources

    for phase, resources in filtered_phases.items():
        st.markdown(f"<div class='card'><h3 class='glow-text'>🔹 {phase}</h3>", unsafe_allow_html=True)
        completed = sum(st.session_state.progress[career_choice][phase])
        total = len(resources)
        progress_percent = (completed / total * 100) if total > 0 else 0
        st.markdown(f"<p><strong>Progress:</strong> {completed}/{total} ({progress_percent:.1f}%)</p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='progress-bar'><div class='progress-fill' style='width: {progress_percent}%'></div></div>",
            unsafe_allow_html=True
        )
        for i, resource in enumerate(resources):
            st.markdown(
                f"- <a href='{resource['link']}' class='resource-link' target='_blank'>{resource['name']}</a> ({resource['platform']})",
                unsafe_allow_html=True
            )
            completed = st.checkbox("Completed", key=f"{career_choice}_{phase}_{i}", value=st.session_state.progress[career_choice][phase][i])
            st.session_state.progress[career_choice][phase][i] = completed
            rating = st.slider("Rate this resource:", 0, 5, st.session_state.ratings[career_choice][phase][i], key=f"rating_{career_choice}_{phase}_{i}")
            st.session_state.ratings[career_choice][phase][i] = rating
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("✅ Chart your course through each phase to reach your stellar career goal!")

# Footer
st.markdown(
    "<div class='footer'>💡 <em>YuvaPath is your cosmic mentor — Explore, Learn, and Conquer the Stars!</em></div>",
    unsafe_allow_html=True
)

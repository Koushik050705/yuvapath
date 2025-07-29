import streamlit as st
import json

# Load the career roadmap data
with open("roadmap_data.json", "r", encoding="utf-8") as file:
    roadmap_data = json.load(file)

# Extract the available careers from the JSON file
available_careers = list(roadmap_data.keys())

# Page config
st.set_page_config(page_title="YuvaPath - Career Guidance", layout="wide")

# App title
st.title("🎯 YuvaPath - AI Career Guidance")
st.write("Helping youth find the right career path with free resources & personalized roadmaps.")

# Language selection
language = st.selectbox("🌐 Choose Language:", ["English", "Hindi", "Tamil", "Telugu"])

# User selects career from dropdown
career_choice = st.selectbox("💼 Select Your Career Interest:", available_careers)

# Display selected career details
if career_choice:
    career_data = roadmap_data[career_choice]

    st.subheader(f"📌 {career_data['title']}")
    st.markdown(f"💰 **Expected Salary:** {career_data['salary']}")
    st.markdown(f"⏳ **Learning Duration:** {career_data['duration']}")

    st.markdown("---")
    st.subheader("📚 Career Roadmap:")

    for phase, resources in career_data["phases"].items():
        st.markdown(f"### 🔹 {phase}")
        for resource in resources:
            st.markdown(f"- [{resource['name']}]({resource['link']}) ({resource['platform']})")
        st.markdown("")

    st.markdown("---")
    st.success("✅ Follow each phase step-by-step to reach your career goal!")

# Footer
st.markdown("---")
st.markdown("💡 *YuvaPath is your personal mentor — Learn, Grow, and Succeed!*")

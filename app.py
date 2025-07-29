import streamlit as st
import json
import os

# ----------------- Load Roadmap Data -----------------
@st.cache_data
def load_roadmap():
    with open("roadmap_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

roadmap_data = load_roadmap()

# ----------------- Session State -----------------
if "language" not in st.session_state:
    st.session_state.language = "English"
if "career_interest" not in st.session_state:
    st.session_state.career_interest = ""
if "progress" not in st.session_state:
    st.session_state.progress = {}

# ----------------- App Title -----------------
st.set_page_config(page_title="YuvaPath", page_icon="🎯", layout="wide")
st.title("🎯 YuvaPath - Career Guidance for Every Youth in India")

# ----------------- Onboarding -----------------
st.subheader("🌐 Select Your Language")
st.session_state.language = st.selectbox("Choose language", ["English", "Hindi", "Tamil", "Telugu"])

st.subheader("📚 Education & Career Interest")
education = st.selectbox("Education Level", ["High School", "Undergraduate", "Graduate", "Other"])
st.session_state.career_interest = st.text_input("Your Career Interest (e.g., AI, Law, Medicine)")

if st.button("Generate My Roadmap"):
    if st.session_state.career_interest.lower() in roadmap_data:
        st.success(f"Roadmap for {st.session_state.career_interest} generated!")
    else:
        st.warning("We don't have a roadmap for that career yet.")

# ----------------- Roadmap Display -----------------
career = st.session_state.career_interest.lower()
if career in roadmap_data:
    info = roadmap_data[career]
    st.header(f"📌 {info['title']}")
    st.info(f"💰 Salary Range: {info['salary']} | ⏳ Duration: {info['duration']}")

    for phase, courses in info["phases"].items():
        with st.expander(phase):
            for course in courses:
                done = st.checkbox(course["name"], key=f"{phase}_{course['name']}")
                if st.session_state.progress.get(course["name"]) != done:
                    st.session_state.progress[course["name"]] = done
                st.markdown(f"[📌 Open Course]({course['link']})")

    # Progress bar
    completed = sum(st.session_state.progress.values())
    total = len(st.session_state.progress)
    if total > 0:
        st.progress(completed / total)

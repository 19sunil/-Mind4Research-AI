# app.py
# Streamlit UI for Mind4Research AI
# Run: streamlit run app.py

import streamlit as st
from pipeline import run_research_pipeline
from datetime import datetime
import time
import base64
from pathlib import Path

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Mind4Research AI",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
if "processing" not in st.session_state:
    st.session_state.processing = False

# ----------------------------
# Function: Play MP3 from assets
# ----------------------------
def autoplay_audio(file_path: str):
    path = Path(file_path)

    if path.exists():
        audio_bytes = path.read_bytes()
        b64 = base64.b64encode(audio_bytes).decode()

        md = f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: 600;
    background: linear-gradient(90deg,#4A90E2,#6EC6FF);
    color: white;
    border: none;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #4A90E2;
}

.sub-text {
    font-size: 18px;
    color: #9aa0a6;
}

.agent-box {
    padding:15px;
    border-radius:15px;
    background:#111827;
    border:1px solid #1f2937;
    margin-bottom:10px;
}

.footer {
    text-align:center;
    color:gray;
    font-size:14px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown(
    '<div class="big-title">🧠 Mind4Research AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-text">Multi-Agent Research Automation System</div>',
    unsafe_allow_html=True
)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("⚙ Settings")
    show_raw = st.checkbox("Show raw search results", value=True)
    st.info("River sound plays during processing")

# ----------------------------
# Input
# ----------------------------
topic = st.text_input(
    "🔍 Enter Research Topic",
    placeholder="Example: Future of AI in Healthcare"
)

generate = st.button("🚀 Generate Research Report", use_container_width=True)

# ----------------------------
# Run Pipeline
# ----------------------------
if generate:

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    try:
        st.session_state.processing = True

        # PLAY SOUND
        autoplay_audio("assets/River_Forest.mp3")

        st.markdown("### 🌊 Live Agent Activity")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div class="agent-box">🧠 Planner Agent<br>Breaking tasks...</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="agent-box">🔎 Search Agent<br>Collecting sources...</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                '<div class="agent-box">📊 Analyst Agent<br>Finding insights...</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="agent-box">✍ Writer Agent<br>Preparing report...</div>',
                unsafe_allow_html=True
            )

        with st.spinner("Running Multi-Agent Research Pipeline..."):
            result = run_research_pipeline(topic)
            time.sleep(1)

        st.session_state.processing = False

        st.success("✅ Research Completed Successfully!")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Final Report",
            "🧠 Critic Feedback",
            "🌐 Search Results",
            "📚 Scraped Content"
        ])

        with tab1:
            st.write(result["report"])

        with tab2:
            st.write(result["feedback"])

        with tab3:
            if show_raw:
                st.code(result["search_results"])

        with tab4:
            st.write(result["scraped_context"])

    except Exception as e:
        st.session_state.processing = False
        st.error(str(e))

# ----------------------------
# Footer
# ----------------------------
st.markdown(
    f'<div class="footer">Mind4Research AI © {datetime.now().year}</div>',
    unsafe_allow_html=True
)
from dotenv import load_dotenv

load_dotenv()
from frontend.ai_renderer import show_ai_renderer
from frontend.sketch_studio import show_sketch_studio
import streamlit as st
from pathlib import Path

from frontend.dashboard import show_dashboard

# Application configuration
st.set_page_config(
    page_title="GardenForge AI | Landscape Design",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path(__file__).parent / "frontend" / "styles.css"

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Sidebar branding
with st.sidebar:

    st.markdown(
        '<div class="brand">🌿 GardenForge</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-caption">AI LANDSCAPE STUDIO</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    pages = [
        "Dashboard",
        "Sketch Studio",
        "AI Renderer",
        "Gallery"
    ]

    selected = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed"
    )

    st.session_state.page = selected

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-label">ACCOUNT</div>',
        unsafe_allow_html=True
    )

    st.markdown("🌱 Landscape Designer")
    st.caption("Personal Workspace")

    st.markdown("---")
    st.caption("GardenForge AI v1.0")

# Main page routing
if st.session_state.page == "Dashboard":
    show_dashboard()

elif st.session_state.page == "Sketch Studio":
    show_sketch_studio()

elif st.session_state.page == "AI Renderer":
    show_ai_renderer()

elif st.session_state.page == "Gallery":
    st.title("Design Gallery")
    st.info("Your generated landscape gallery will be developed next.")

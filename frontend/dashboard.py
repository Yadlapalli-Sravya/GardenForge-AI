
import streamlit as st


def show_dashboard():

    st.markdown("""
        <div class="main-title">Welcome to GardenForge AI 🌿</div>
        <div class="subtitle">
            Transform your imagination into extraordinary landscapes.
            Design smarter. Visualize better.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero">
            <h2>Design your dream landscape.</h2>
            <p>
                Turn your hand-drawn garden sketches into
                photorealistic landscape concepts with AI.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Statistics
    st.markdown('<div class="section-title">Your Workspace</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Projects", "12", "+2 this month")

    with col2:
        st.metric("AI Designs", "28", "+8 this month")

    with col3:
        st.metric("Saved Concepts", "16", "+4 this month")

    with col4:
        st.metric("Design Styles", "6", "Available styles")

    st.markdown("---")

    # Quick actions
    st.markdown('<div class="section-title">Quick Actions</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### ✏️ Sketch Studio")
        st.write("Upload your garden sketch and prepare it for AI rendering.")
        if st.button("Open Sketch Studio", use_container_width=True):
            st.session_state.page = "Sketch Studio"
            st.rerun()

    with c2:
        st.markdown("### 🎨 Design Gallery")
        st.write("Explore your landscape design collection.")
        if st.button("Explore Gallery", use_container_width=True):
            st.session_state.page = "Gallery"
            st.rerun()

    with c3:
        st.markdown("### ✨ AI Renderer")
        st.write("Create photorealistic landscape concepts.")
        if st.button("Explore AI Renderer", use_container_width=True):
            st.session_state.page = "AI Renderer"
            st.rerun()

    st.markdown("---")

    # Recent projects
    st.markdown('<div class="section-title">Recent Projects</div>',
                unsafe_allow_html=True)

    projects = [
        ("🌳", "Modern Zen Garden", "Modern Minimalist", "Completed"),
        ("🌺", "Tropical Paradise", "Tropical Landscape", "In Progress"),
        ("🏡", "Residential Garden", "Contemporary", "Completed"),
    ]

    cols = st.columns(3)

    for col, project in zip(cols, projects):
        with col:
            st.markdown(f"""
                <div class="project-card">
                    <div style="font-size:32px">{project[0]}</div>
                    <h4>{project[1]}</h4>
                    <p>{project[2]}</p>
                    <p><b>{project[3]}</b></p>
                </div>
            """, unsafe_allow_html=True)

    st.caption(
        "GardenForge AI · Intelligent Landscape Design Platform"
    )


import os
import tempfile
import streamlit as st

from io import BytesIO
from PIL import Image
from gradio_client import Client, handle_file

from ai_engine.prompt_builder import build_prompt
from ai_engine.gemini_service import analyze_landscape_sketch


def show_ai_renderer():

    st.markdown("""
        <div class="main-title">🌿 GardenForge AI</div>
        <div class="subtitle">
            Transform your pencil sketches into customized
            photorealistic landscape concepts.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Kaggle Gradio connection
    api_url = st.text_input(
        "Kaggle GPU API URL",
        value=os.getenv("GARDENFORGE_API_URL", ""),
        placeholder="Paste your https://....gradio.live address",
        key="gardenforge_api_url"
    )

    st.markdown("### 1. Upload Your Original Garden Sketch")

    uploaded = st.file_uploader(
        "Choose a pencil sketch or garden drawing",
        type=["png", "jpg", "jpeg"],
        key="direct_garden_sketch"
    )

    sketch = None

    if uploaded is not None:
        sketch = Image.open(
            BytesIO(uploaded.getvalue())
        ).convert("RGB")

        # A new upload means a new generation
        upload_id = uploaded.name + str(uploaded.size)

        if st.session_state.get("renderer_upload_id") != upload_id:
            st.session_state.renderer_upload_id = upload_id
            st.session_state.gemini_analysis = None
            st.session_state.generated_image = None
            st.session_state.renderer_prompt = None

    else:
        sketch = st.session_state.get("original_sketch")

        if sketch is None:
            sketch = st.session_state.get("processed_sketch")

    if sketch is None:
        st.info("Upload a garden sketch to begin.")
        return

    st.image(
        sketch,
        caption="Original Garden Sketch",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### 2. Customize Your Garden")

    style = st.selectbox(
        "Choose Landscape Style",
        [
            "Modern Minimalist",
            "Tropical Paradise",
            "Japanese Zen",
            "Mediterranean",
            "Luxury Contemporary",
            "Natural Cottage"
        ],
        key="renderer_style"
    )

    custom_prompt = st.text_area(
        "Describe the changes you want",
        placeholder=(
            "Example: Add a swimming pool, tropical plants, "
            "colorful flowers, outdoor seating and warm lighting."
        ),
        height=120,
        key="renderer_custom_prompt"
    )

    guidance = st.slider(
        "Prompt Guidance",
        min_value=5.0,
        max_value=12.0,
        value=7.5,
        step=0.5,
        key="renderer_guidance"
    )

    st.markdown("---")
    st.markdown("### 3. Gemini Sketch Analysis")

    if st.button(
        "🔍 Analyze Sketch with Gemini",
        use_container_width=True
    ):
        try:
            with st.spinner("Gemini is analyzing your garden..."):
                analysis = analyze_landscape_sketch(sketch)
                st.session_state.gemini_analysis = analysis

            st.success("Sketch analysis completed!")

        except Exception as error:
            st.error(f"Gemini analysis failed: {error}")

    analysis = st.session_state.get("gemini_analysis")

    if analysis:
        with st.expander("View Gemini Analysis"):
            st.write(analysis)

    st.markdown("---")
    st.markdown("### 4. Generate Your HD Landscape")

    if st.button(
        "✨ Generate GardenForge Landscape",
        type="primary",
        use_container_width=True
    ):

        if not api_url.strip():
            st.error("Paste your active Kaggle Gradio API URL first.")

        else:
            try:
                with st.spinner("Preparing your garden design..."):

                    if not analysis:
                        analysis = analyze_landscape_sketch(sketch)
                        st.session_state.gemini_analysis = analysis

                    prompt = build_prompt(
                        analysis,
                        style,
                        custom_prompt
                    )

                    st.session_state.renderer_prompt = prompt

                with tempfile.NamedTemporaryFile(
                    suffix=".png",
                    delete=False
                ) as temp_file:

                    sketch.save(temp_file, format="PNG")
                    sketch_path = temp_file.name

                try:
                    with st.spinner(
                        "Kaggle T4 GPU is generating your landscape..."
                    ):

                        client = Client(api_url.strip())

                        result = client.predict(
                            handle_file(sketch_path),
                            prompt,
                            style,
                            guidance,
                            api_name="/generate_garden"
                        )

                finally:
                    if os.path.exists(sketch_path):
                        os.remove(sketch_path)

                if isinstance(result, (tuple, list)):
                    result = result[0]

                if isinstance(result, dict):
                    result = (
                        result.get("path")
                        or result.get("name")
                        or result.get("url")
                    )

                if isinstance(result, Image.Image):
                    generated = result.convert("RGB")
                else:
                    generated = Image.open(result).convert("RGB")

                st.session_state.generated_image = generated
                st.session_state.generated_prompt = prompt
                st.session_state.generated_style = style

                st.success("Your GardenForge landscape is ready!")

            except Exception as error:
                st.error(f"Landscape generation failed: {error}")

    # 5. Display result
    generated = st.session_state.get("generated_image")

    if generated is not None:

        st.markdown("---")
        st.markdown("## 🌿 Before & After Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Original Sketch")
            st.image(sketch, use_container_width=True)

        with col2:
            st.markdown("### AI-Generated Design")
            st.image(generated, use_container_width=True)

        st.markdown("### Download Your Landscape")

        buffer = BytesIO()
        generated.save(buffer, format="PNG")

        st.download_button(
            "⬇️ Download HD Landscape",
            data=buffer.getvalue(),
            file_name="GardenForge_HD_Landscape.png",
            mime="image/png",
            use_container_width=True
        )

        st.success(
            f"Export resolution: {generated.width} × {generated.height}"
        )

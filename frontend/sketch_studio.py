
import hashlib
from io import BytesIO

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from ai_engine.gemini_service import analyze_landscape_sketch
from ai_engine.prompt_builder import build_prompt


# ==========================================================
# 1. SESSION STATE INITIALIZATION
# ==========================================================

def initialize_session_state():

    defaults = {
        "processed_sketch": None,
        "original_sketch": None,
        "sketch_filename": None,
        "sketch_hash": None,
        "gemini_analysis": None,
        "generated_prompt": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# 2. SKETCH PROCESSING FUNCTION
# ==========================================================

def process_sketch(image, method, threshold1=50, threshold2=150):

    image_array = np.array(image.convert("RGB"))

    image_cv = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2BGR
    )

    if method == "Grayscale":

        processed = cv2.cvtColor(
            image_cv,
            cv2.COLOR_BGR2GRAY
        )

        return Image.fromarray(processed)

    elif method == "Edge Detection":

        gray = cv2.cvtColor(
            image_cv,
            cv2.COLOR_BGR2GRAY
        )

        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        edges = cv2.Canny(
            blurred,
            threshold1,
            threshold2
        )

        return Image.fromarray(edges)

    elif method == "Pencil Sketch":

        gray = cv2.cvtColor(
            image_cv,
            cv2.COLOR_BGR2GRAY
        )

        inverted = 255 - gray

        blurred = cv2.GaussianBlur(
            inverted,
            (21, 21),
            0
        )

        inverted_blur = 255 - blurred

        sketch = cv2.divide(
            gray,
            inverted_blur,
            scale=256
        )

        return Image.fromarray(sketch)

    return image


# ==========================================================
# 3. MAIN SKETCH STUDIO
# ==========================================================

def show_sketch_studio():

    initialize_session_state()

    st.markdown("""
        <div class="main-title">Sketch Studio ✏️</div>

        <div class="subtitle">
            Upload, inspect and prepare your landscape sketches
            for AI-powered transformation.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ------------------------------------------------------
    # 01. UPLOAD SKETCH
    # ------------------------------------------------------

    st.markdown(
        '<div class="section-title">01 · Upload Your Sketch</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a landscape or garden sketch",
        type=["png", "jpg", "jpeg"],
        help="Upload a clear hand-drawn landscape design."
    )

    if uploaded_file is None:

        st.info(
            "Please upload a landscape sketch to begin."
        )

        st.markdown("""
            **Supported formats:** PNG, JPG, JPEG

            **Recommended:** Clear sketches with visible
            garden boundaries, pathways, plants and structures.
        """)

        return

    # ------------------------------------------------------
    # 02. LOAD IMAGE
    # ------------------------------------------------------

    try:

        image_bytes = uploaded_file.getvalue()

        original_image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

    except Exception:

        st.error(
            "Unable to read this image. Please upload another file."
        )

        return

    # Detect a new uploaded image and reset previous results

    current_hash = hashlib.sha256(
        image_bytes
    ).hexdigest()

    if current_hash != st.session_state.sketch_hash:

        st.session_state.sketch_hash = current_hash

        st.session_state.original_sketch = original_image

        st.session_state.processed_sketch = None

        st.session_state.sketch_filename = uploaded_file.name

        st.session_state.gemini_analysis = None

        st.session_state.generated_prompt = None

    width, height = original_image.size

    file_size = len(image_bytes)

    st.success(
        "Your sketch has been uploaded successfully!"
    )

    # ------------------------------------------------------
    # 03. IMAGE INFORMATION
    # ------------------------------------------------------

    st.markdown(
        '<div class="section-title">02 · Image Information</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Width", f"{width} px")

    c2.metric("Height", f"{height} px")

    c3.metric(
        "File Size",
        f"{file_size / 1024:.1f} KB"
    )

    st.markdown("---")

    # ------------------------------------------------------
    # 04. ORIGINAL IMAGE
    # ------------------------------------------------------

    st.markdown(
        '<div class="section-title">03 · Original Sketch</div>',
        unsafe_allow_html=True
    )

    st.image(
        original_image,
        caption="Uploaded landscape sketch",
        use_container_width=True
    )

    st.markdown("---")

    # ------------------------------------------------------
    # 05. SKETCH PROCESSING
    # ------------------------------------------------------

    st.markdown(
        '<div class="section-title">04 · Sketch Processing</div>',
        unsafe_allow_html=True
    )

    method = st.selectbox(
        "Select processing technique",
        [
            "Grayscale",
            "Edge Detection",
            "Pencil Sketch"
        ],
        key="processing_method"
    )

    threshold1 = 50
    threshold2 = 150

    if method == "Edge Detection":

        threshold1 = st.slider(
            "Lower Edge Threshold",
            0,
            255,
            50
        )

        threshold2 = st.slider(
            "Upper Edge Threshold",
            0,
            255,
            150
        )

        if threshold1 >= threshold2:

            st.warning(
                "The upper threshold should be greater "
                "than the lower threshold."
            )

    if st.button(
        "Process Sketch",
        type="primary",
        use_container_width=True
    ):

        if method == "Edge Detection" and threshold1 >= threshold2:

            st.error(
                "Please adjust the edge thresholds."
            )

        else:

            try:

                with st.spinner(
                    "Processing your landscape sketch..."
                ):

                    processed_image = process_sketch(
                        original_image,
                        method,
                        threshold1,
                        threshold2
                    )

                    st.session_state.processed_sketch = processed_image

                    st.session_state.original_sketch = original_image

                    st.session_state.gemini_analysis = None

                    st.session_state.generated_prompt = None

                st.success(
                    "Sketch processing completed!"
                )

            except Exception as error:

                st.error(
                    f"Sketch processing failed: {error}"
                )

    # ------------------------------------------------------
    # 06. DISPLAY PROCESSED SKETCH
    # ------------------------------------------------------

    processed = st.session_state.processed_sketch

    if processed is None:
        return

    st.markdown("---")

    st.markdown(
        '<div class="section-title">05 · Processed Sketch</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            original_image,
            caption="Original Sketch",
            use_container_width=True
        )

    with col2:

        st.image(
            processed,
            caption="Processed Sketch",
            use_container_width=True
        )

    # Download processed sketch

    buffer = BytesIO()

    processed.save(
        buffer,
        format="PNG"
    )

    st.download_button(
        label="Download Processed Sketch",
        data=buffer.getvalue(),
        file_name="gardenforge_processed.png",
        mime="image/png",
        use_container_width=True
    )

    # ------------------------------------------------------
    # 07. GEMINI AI LANDSCAPE ANALYSIS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### ✨ AI Landscape Analysis"
    )

    st.write(
        "Let Gemini examine your uploaded garden design "
        "and suggest professional landscape improvements."
    )

    if st.button(
        "Analyze My Garden Sketch with Gemini",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Gemini is analyzing your landscape..."
            ):

                analysis = analyze_landscape_sketch(
                    original_image
                )

                st.session_state.gemini_analysis = analysis

                st.session_state.generated_prompt = None

            st.success(
                "Landscape analysis completed!"
            )

        except Exception as error:

            st.error(
                f"Landscape analysis failed: {error}"
            )

    # Display Gemini report

    analysis = st.session_state.get(
        "gemini_analysis"
    )

    if analysis:

        st.markdown("---")

        st.markdown(
            "### 📋 Your AI Landscape Report"
        )

        st.markdown(analysis)

        # --------------------------------------------------
        # 08. SMART LANDSCAPE PROMPT GENERATOR
        # --------------------------------------------------

        st.markdown("---")

        st.markdown(
            "### 🎨 Smart Landscape Prompt Generator"
        )

        st.write(
            "Customize your garden design and generate "
            "a professional AI image-generation prompt."
        )

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
            key="landscape_style"
        )

        custom_prompt = st.text_area(
            "Additional Design Instructions",
            placeholder=(
                "Example: Add warm garden lighting, "
                "a small pond and flowering plants..."
            ),
            key="custom_design_prompt"
        )

        # Generate prompt

        if st.button(
            "✨ Generate Landscape Prompt",
            type="primary",
            use_container_width=True
        ):

            try:

                final_prompt = build_prompt(
                    analysis,
                    style,
                    custom_prompt
                )

                st.session_state.generated_prompt = final_prompt

                st.success(
                    "Landscape prompt generated successfully!"
                )

            except Exception as error:

                st.error(
                    f"Prompt generation failed: {error}"
                )

        # --------------------------------------------------
        # 09. DISPLAY AND DOWNLOAD GENERATED PROMPT
        # --------------------------------------------------

        generated_prompt = st.session_state.get(
            "generated_prompt"
        )

        if generated_prompt:

            st.markdown("---")

            st.markdown(
                "### 🌟 Your Generated Landscape Prompt"
            )

            st.text_area(
                "AI Landscape Prompt",
                value=generated_prompt,
                height=300,
                key="generated_prompt_display"
            )

            st.download_button(
                label="📥 Download Landscape Prompt",
                data=generated_prompt,
                file_name="gardenforge_prompt.txt",
                mime="text/plain",
                use_container_width=True
            )

    else:

        st.info(
            "First analyze your garden sketch with Gemini. "
            "Your Smart Landscape Prompt Generator will "
            "appear after the analysis is complete."
        )

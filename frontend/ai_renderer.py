
import base64
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, ImageOps


MODEL_ID = "@cf/black-forest-labs/flux-2-klein-9b"

STYLES = {
    "Modern Minimalist": "modern minimalist garden, geometric planting beds, clean stone paving, elegant architectural landscaping",
    "Tropical Paradise": "lush tropical garden, palms, exotic foliage, vibrant flowering plants, natural stone",
    "Japanese Zen": "peaceful Japanese garden, koi pond, Japanese maple, bamboo, stone lanterns and stepping stones",
    "Mediterranean": "Mediterranean garden, olive trees, lavender, terracotta, warm natural stone",
    "Luxury Contemporary": "luxury contemporary landscape, premium outdoor furniture, elegant lighting, sophisticated planting",
    "Natural Cottage": "English cottage garden, colorful flowers, curved paths, layered shrubs and natural planting"
}


def generate_cloudflare_image(sketch, prompt, style):

    account_id = st.secrets.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = st.secrets.get("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        raise ValueError("Cloudflare credentials are missing from Streamlit Secrets.")

    endpoint = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/{MODEL_ID}"
    )

    # Prepare reference image.
    # Cloudflare requires reference images smaller than 512 x 512.
    sketch = ImageOps.exif_transpose(sketch).convert("RGB")
    sketch.thumbnail((511, 511), Image.Resampling.LANCZOS)

    image_buffer = BytesIO()
    sketch.save(image_buffer, format="PNG")
    image_bytes = image_buffer.getvalue()

    full_prompt = f"""
    Transform the supplied garden pencil sketch into a premium,
    photorealistic landscape architecture visualization.

    SELECTED STYLE:
    {STYLES[style]}

    USER REQUIREMENTS:
    {prompt if prompt.strip() else "Create a beautiful, professionally landscaped garden."}

    REFERENCE IMAGE INSTRUCTIONS:
    Use the uploaded sketch as the primary visual reference.
    Preserve its garden boundaries, overall composition,
    pathways, pond positions, bridges, seating areas,
    buildings and visible structures.

    Do not invent a completely different garden.
    Do not remove major structures from the reference.
    Add realistic materials, detailed healthy vegetation,
    natural water, realistic grass and professional lighting.

    VISUAL QUALITY:
    High-end architectural landscape photography,
    natural daylight, realistic shadows, balanced colors,
    detailed textures and professional visualization.
    """

    data = {
        "prompt": full_prompt,
        "width": "1024",
        "height": "1024",
        "guidance": "4"
    }

    files = {
        "input_image_0": (
            "garden_sketch.png",
            image_bytes,
            "image/png"
        )
    }

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.post(
        endpoint,
        headers=headers,
        data=data,
        files=files,
        timeout=300
    )

    if response.status_code != 200:
        try:
            detail = response.json()
        except Exception:
            detail = response.text[:1000]

        raise RuntimeError(
            f"Cloudflare API error ({response.status_code}): {detail}"
        )

    result = response.json()

    if not result.get("success", True):
        raise RuntimeError(str(result.get("errors", result)))

    image_data = result.get("result", {}).get("image")

    if not image_data:
        raise RuntimeError(
            f"No generated image returned. Response: {result}"
        )

    generated_bytes = base64.b64decode(image_data)
    generated_image = Image.open(
        BytesIO(generated_bytes)
    ).convert("RGB")

    return generated_image


def show_ai_renderer():

    st.markdown(
        """
        <div class="main-title">GardenForge AI 🌿</div>
        <div class="subtitle">
        Transform pencil sketches into customized,
        photorealistic landscape designs.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 1. Upload Your Garden Sketch")

    uploaded_file = st.file_uploader(
        "Upload a pencil sketch or garden drawing",
        type=["png", "jpg", "jpeg"],
        key="cloudflare_garden_upload"
    )

    if uploaded_file is None:
        st.info("Upload a garden sketch to begin.")
        return

    sketch = Image.open(uploaded_file).convert("RGB")

    st.image(
        sketch,
        caption="Your original garden sketch",
        use_container_width=True
    )

    st.markdown("### 2. Customize Your Garden")

    style = st.selectbox(
        "Choose Landscape Style",
        list(STYLES.keys()),
        key="cloudflare_garden_style"
    )

    custom_prompt = st.text_area(
        "Describe your dream garden",
        placeholder=(
            "Example: Add a swimming pool, colorful flowers, "
            "wooden seating, tropical plants and warm lighting."
        ),
        height=120,
        key="cloudflare_garden_prompt"
    )

    st.markdown("### 3. Generate Your HD Landscape")

    st.caption(
        "Powered by Cloudflare Workers AI and FLUX.2 Klein 9B."
    )

    if st.button(
        "✨ Generate 1024 × 1024 Landscape",
        type="primary",
        use_container_width=True
    ):

        try:
            with st.spinner(
                "GardenForge AI is transforming your sketch..."
            ):
                generated = generate_cloudflare_image(
                    sketch,
                    custom_prompt,
                    style
                )

            st.session_state["generated_image"] = generated
            st.session_state["garden_original"] = sketch

            st.success("Your landscape design is ready!")

        except Exception as error:
            st.error(f"Generation failed: {error}")

    generated = st.session_state.get("generated_image")

    if generated is not None:

        st.divider()
        st.markdown("## 4. Your GardenForge Design")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Original Sketch**")
            original = st.session_state.get(
                "garden_original", sketch
            )
            st.image(original, use_container_width=True)

        with col2:
            st.markdown("**AI-Generated Landscape**")
            st.image(generated, use_container_width=True)

        st.success(
            f"Output resolution: {generated.width} × {generated.height}"
        )

        buffer = BytesIO()
        generated.save(buffer, format="PNG")

        st.download_button(
            "⬇️ Download HD Garden Design",
            data=buffer.getvalue(),
            file_name="GardenForge_HD_1024.png",
            mime="image/png",
            use_container_width=True
        )

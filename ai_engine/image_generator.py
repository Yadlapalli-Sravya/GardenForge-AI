
import replicate
from io import BytesIO
from PIL import Image

from ai_engine.model_loader import get_replicate_client


MODEL_VERSION = (
    "435061a1b5a4c1e26740464bf786efdfa9cb3a3ac488595a2de23e143fdb0117"
)


def generate_landscape(
    sketch,
    prompt,
    image_resolution="512",
    ddim_steps=20,
    scale=9
):

    client = get_replicate_client()

    image_buffer = BytesIO()

    sketch.convert("RGB").save(
        image_buffer,
        format="PNG"
    )

    image_buffer.seek(0)

    image_buffer.name = "garden_sketch.png"

    try:
        output = client.run(
            f"jagilley/controlnet-scribble:{MODEL_VERSION}",
            input={
                "image": image_buffer,
                "prompt": prompt,
                "image_resolution": str(image_resolution),
                "ddim_steps": int(ddim_steps),
                "scale": float(scale),
                "num_samples": "1",
                "eta": 0,
                "a_prompt": (
                    "best quality, extremely detailed, "
                    "photorealistic landscape architecture"
                ),
                "n_prompt": (
                    "low quality, blurry, distorted geometry, "
                    "poor composition, unrealistic vegetation"
                )
            }
        )

        if not output:
            raise RuntimeError("No image was returned.")

        result = output[0]

        if hasattr(result, "read"):
            image_bytes = result.read()

        else:
            import requests

            response = requests.get(
                str(result),
                timeout=120
            )
            response.raise_for_status()
            image_bytes = response.content

        return Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

    except Exception as error:
        raise RuntimeError(
            f"Landscape generation failed: {error}"
        ) from error


import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"


def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key is missing!")

    return genai.Client(api_key=api_key)


def analyze_landscape_sketch(image):

    client = get_gemini_client()

    prompt = """
    You are GardenForge AI, a professional landscape architect.

    Analyze the uploaded garden sketch carefully.

    Provide the following sections:

    1. Overall Garden Layout
    2. Visible Trees and Plants
    3. Pathways and Walking Areas
    4. Water Features
    5. Seating and Outdoor Structures
    6. Recommended Landscape Style
    7. Design Improvement Suggestions

    Finally, provide a detailed image-generation prompt.

    IMPORTANT:
    - Preserve the original sketch layout.
    - Describe only features visible in the image.
    - Clearly distinguish observations from suggestions.
    - Use professional landscape architecture terminology.
    """

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image]
            )

            if not response.text:
                raise RuntimeError("Empty Gemini response.")

            return response.text

        except Exception as error:

            message = str(error)

            temporary = (
                "503" in message
                or "UNAVAILABLE" in message
                or "429" in message
            )

            if temporary and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            raise RuntimeError(
                f"Gemini analysis failed: {message}"
            ) from error

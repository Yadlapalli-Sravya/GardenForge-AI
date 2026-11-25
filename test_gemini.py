
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"

print("\n--- TEXT TEST ---")

try:
    response = client.models.generate_content(
        model=MODEL,
        contents="Introduce GardenForge AI in one sentence."
    )
    print("TEXT SUCCESS!")
    print(response.text)

except Exception as e:
    print("TEXT FAILED:", str(e)[:400])


print("\n--- IMAGE TEST ---")

try:
    image = Image.new("RGB", (512, 512), "white")

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            "Describe this image in one sentence.",
            image
        ]
    )

    print("IMAGE SUCCESS!")
    print(response.text)

except Exception as e:
    print("IMAGE FAILED:", str(e)[:400])

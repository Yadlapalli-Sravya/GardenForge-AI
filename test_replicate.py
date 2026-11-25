
import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("REPLICATE_API_TOKEN")

if not token:
    print("ERROR: Replicate API token not found.")
else:
    try:
        response = requests.get(
            "https://api.replicate.com/v1/account",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=20
        )

        if response.status_code == 200:
            account = response.json()

            print("SUCCESS! Replicate API connected.")
            print("Account:", account.get("username"))
            print("API Status: Authenticated")

        elif response.status_code == 401:
            print("ERROR: Invalid or expired API token.")

        else:
            print("API Error:", response.status_code)
            print(response.text[:500])

    except requests.RequestException as error:
        print("Connection error:", error)


import os
import replicate


MODEL_NAME = "jagilley/controlnet-scribble"


def get_replicate_client():

    token = os.getenv("REPLICATE_API_TOKEN")

    if not token:
        raise ValueError(
            "Replicate API token is missing. "
            "Check your .env file."
        )

    return replicate.Client(api_token=token)


def check_model_configuration():

    try:
        get_replicate_client()
        return True, "AI model configuration is ready."

    except Exception as error:
        return False, str(error)

import os

class LargeLanguageModel:
    def __init__(self):
        pass

    def get_key(self):
        """Retrieve Hugging Face API key from environment variables."""
        __api_key = os.getenv("HUGGINGFACE_API_KEY", "default_huggingface_key")
        return __api_key

    def get_gpt_key(self):
        """Retrieve GPT API key from environment variables."""
        __api_key = os.getenv("GPT_API_KEY", "default_gpt_key")
        return __api_key

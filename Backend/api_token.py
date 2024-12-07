import os

class LargeLanguageModel():
    def __init__(self):
        pass
    
    def get_Key(self):
        # Fetch the Hugging Face API key from environment variables
        hf_api_key = os.getenv('HF_API_KEY')
        return hf_api_key
    
    def get_gpt_key(self):
        # Fetch the OpenAI GPT API key from environment variables
        gpt_api_key = os.getenv('GPT_API_KEY')
        return gpt_api_key

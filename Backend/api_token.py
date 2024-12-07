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


# class LargeLanguageModel():
#     def __init__(self):
#         pass
    
#     def get_Key(self):
#         __api_key = "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"
#         return __api_key
    
#     def get_gpt_key(self):
#         __api_key = "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"
#         return __api_key

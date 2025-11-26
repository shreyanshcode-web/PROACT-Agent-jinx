import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

# Configure the API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")

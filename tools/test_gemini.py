import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
model = genai.GenerativeModel(model_name)

# Test a simple prompt
try:
    print(f"Sending test request to Gemini (Model: {model_name})...")
    response = model.generate_content("Hello, Gemini! Can you tell me a short joke?")
    print("\nResponse from Gemini:")
    print(response.text)
    print("\n[SUCCESS] Gemini integration is working correctly.")
except Exception as e:
    print(f"\n[ERROR] Error calling Gemini API: {e}")
    print("\nTroubleshooting steps:")
    print("1. Verify your GEMINI_API_KEY in the .env file")
    print("2. Make sure you have an active internet connection")
    print("3. Check if the Google Generative AI service is available in your region")
    exit(1)

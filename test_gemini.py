import os
import google.generativeai as genai

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Test a simple prompt
try:
    print("Sending test request to Gemini...")
    response = model.generate_content("Hello, Gemini! Can you tell me a short joke?")
    print("\nResponse from Gemini:")
    print(response.text)
    print("\n✅ Success! Gemini integration is working correctly.")
except Exception as e:
    print(f"\n❌ Error calling Gemini API: {e}")
    print("\nTroubleshooting steps:")
    print("1. Verify your GEMINI_API_KEY in the .env file")
    print("2. Make sure you have an active internet connection")
    print("3. Check if the Google Generative AI service is available in your region")

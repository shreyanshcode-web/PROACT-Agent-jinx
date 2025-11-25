#!/usr/bin/env python
"""Direct test of Gemini API without Jinx complexity"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_direct_gemini():
    """Test Gemini API directly"""
    print("Testing Gemini API directly...")
    
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Create model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Test prompts
        prompts = [
            "Write a simple Python function to add two numbers",
            "Create a hello world program in Python",
            "Explain what an AI agent is in one sentence"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n--- Test {i} ---")
            print(f"Prompt: {prompt}")
            print("Response: ", end="")
            
            response = model.generate_content(prompt)
            print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("DIRECT GEMINI API TEST")
    print("="*50)
    
    success = test_direct_gemini()
    
    if success:
        print("\n✅ Gemini API is working correctly!")
        print("\nThe issue is with Jinx's complex module structure.")
        print("Let me create a working agent for you...")
    else:
        print("\n❌ Gemini API test failed.")
    
    print("="*50)

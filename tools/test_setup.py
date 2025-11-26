#!/usr/bin/env python
"""Test script to verify the setup"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_env_vars():
    """Test if environment variables are loaded correctly"""
    print("Testing environment variables...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    provider = os.getenv("JINX_LLM_PROVIDER")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return False
    if provider != "gemini":
        print("❌ JINX_LLM_PROVIDER not set to gemini")
        return False
    
    print("✅ Environment variables loaded correctly")
    return True

def test_gemini_import():
    """Test if google-generativeai can be imported"""
    print("\nTesting Gemini import...")
    try:
        import google.generativeai as genai
        print("✅ google-generativeai imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import google-generativeai: {e}")
        return False

def test_gemini_connection():
    """Test if Gemini API can be connected"""
    print("\nTesting Gemini API connection...")
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Test with a simple model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Send a test request
        response = model.generate_content("Hello! Just testing the connection. Reply with 'Connection successful!'")
        
        if response.text:
            print("✅ Gemini API connection successful!")
            print(f"Response: {response.text[:100]}...")
            return True
        else:
            print("❌ No response from Gemini API")
            return False
            
    except Exception as e:
        print(f"❌ Failed to connect to Gemini API: {e}")
        return False

def test_jinx_imports():
    """Test if Jinx modules can be imported"""
    print("\nTesting Jinx imports...")
    try:
        from jinx.orchestrator import main
        print("✅ Jinx orchestrator imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Jinx orchestrator: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("JINX AGENT SETUP TEST")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_env_vars()
    all_passed &= test_gemini_import()
    all_passed &= test_gemini_connection()
    all_passed &= test_jinx_imports()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ALL TESTS PASSED - Ready to run Jinx!")
        print("\nTo start the agent, run:")
        print("  .venv\\Scripts\\python.exe jinx.py")
    else:
        print("❌ Some tests failed - Please check the errors above")
    print("=" * 50)

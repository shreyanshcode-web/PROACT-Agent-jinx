#!/usr/bin/env python
"""Test if Jinx can now start without OpenAI errors"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_jinx_imports():
    """Test if Jinx modules can be imported without errors"""
    print("Testing Jinx imports...")
    
    try:
        # Test importing the orchestrator
        from jinx.orchestrator import main
        print("✅ Successfully imported jinx.orchestrator")
        
        # Test importing OpenAI service
        from jinx.openai_service import spark_openai
        print("✅ Successfully imported jinx.openai_service")
        
        # Test importing net client
        from jinx.net import get_openai_client
        print("✅ Successfully imported jinx.net")
        
        # Test getting OpenAI client
        client = get_openai_client()
        print("✅ Successfully got OpenAI client (dummy or real)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment():
    """Test environment variables"""
    print("\nTesting environment variables...")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    provider = os.getenv("JINX_LLM_PROVIDER")
    
    print(f"GEMINI_API_KEY: {'Set' if gemini_key else 'Not set'}")
    print(f"OPENAI_API_KEY: {'Set' if openai_key else 'Not set'}")
    print(f"JINX_LLM_PROVIDER: {provider}")
    
    return True

if __name__ == "__main__":
    print("="*50)
    print("JINX FIX TEST")
    print("="*50)
    
    test_environment()
    success = test_jinx_imports()
    
    print("\n" + "="*50)
    if success:
        print("✅ Jinx should now work without OpenAI errors!")
        print("\nTo run Jinx:")
        print("  python jinx.py")
    else:
        print("❌ Still have issues - check the errors above")
    print("="*50)

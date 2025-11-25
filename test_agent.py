#!/usr/bin/env python
"""Simple test to verify the agent can process a command"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

async def test_agent():
    """Test the agent with a simple command"""
    print("Testing Jinx Agent...")
    
    # Import the conversation service
    from jinx.micro.llm import spark_llm
    
    # Test a simple prompt
    try:
        print("\nSending test prompt to Gemini...")
        response, tag = await spark_llm("Hello! Can you write a simple Python function that adds two numbers?")
        
        print("\n" + "="*50)
        print("AGENT RESPONSE:")
        print("="*50)
        print(response)
        print("="*50)
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("JINX AGENT FUNCTIONALITY TEST")
    print("="*50)
    
    success = asyncio.run(test_agent())
    
    if success:
        print("\n✅ Agent is working! The LLM integration is successful.")
        print("\nTo use the full agent with interactive mode, run:")
        print("  .venv\\Scripts\\python.exe jinx.py")
    else:
        print("\n❌ Agent test failed. Check the error above.")
    
    print("="*50)

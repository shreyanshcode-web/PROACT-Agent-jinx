#!/usr/bin/env python
"""Run Jinx with Gemini API"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Verify Gemini API key is set
if not os.getenv("GEMINI_API_KEY"):
    print("=" * 60)
    print("ERROR: GEMINI_API_KEY not found in environment!")
    print("=" * 60)
    print("\nPlease add your Gemini API key to the .env file:")
    print("GEMINI_API_KEY=your_api_key_here")
    print("\nGet your API key from: https://makersuite.google.com/app/apikey")
    print("=" * 60)
    sys.exit(1)

print("Starting Jinx with Gemini API...")
print("=" * 50)

# Now import and run Jinx
try:
    from jinx.orchestrator import main as jinx_main
    
    # Run the main function
    jinx_main()
    
except KeyboardInterrupt:
    print("\n\nJinx stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

print("Step 1: Importing jinx.micro.llm.gemini_service...")
try:
    import jinx.micro.llm.gemini_service
    print("✅ Success")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print("Step 2: Importing jinx.openai_service...")
try:
    import jinx.openai_service
    print("✅ Success")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print("Step 3: Importing jinx.orchestrator...")
try:
    import jinx.orchestrator
    print("✅ Success")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print("Step 4: Importing jinx.micro.conversation.orchestrator...")
try:
    import jinx.micro.conversation.orchestrator
    print("✅ Success")
except ImportError as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print("\n🎉 All critical imports verified successfully! No circular dependencies found.")

"""
Quick verification script to check if main modules import correctly after migration.
"""

import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def test_import(module_name):
    """Test if a module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {module_name}")
        return True
    except Exception as e:
        print(f"❌ {module_name}: {str(e)}")
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("PROACT-Agent-jinx - Import Verification")
    print("=" * 60)
    print()
    
    modules_to_test = [
        "jinx.settings",
        "jinx.log_paths",
        "jinx.gemini_service",
        "jinx.logger.llm_requests",
        "jinx.rag_service",
        "jinx.orchestrator",
        "jinx.net.client",
        "jinx.micro.llm",
    ]
    
    results = []
    for module in modules_to_test:
        results.append(test_import(module))
    
    print()
    print("=" * 60)
    success_count = sum(results)
    total_count = len(results)
    print(f"Results: {success_count}/{total_count} modules imported successfully")
    
    if success_count == total_count:
        print("✅ All core modules are working!")
    else:
        print("⚠️  Some modules have import errors - check above for details")
    print("=" * 60)
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())

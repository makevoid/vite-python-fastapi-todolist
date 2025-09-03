#!/usr/bin/env python3
"""
Unified test runner that executes both backend unit tests and E2E tests
Each test suite runs in isolation with separate databases and ports
"""
import subprocess
import sys
import os
import tempfile
from pathlib import Path

def run_command(cmd, cwd=None, description=""):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"🏃 Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"Working directory: {cwd or os.getcwd()}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=False,  # Show output in real-time
            text=True
        )
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Main test runner"""
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    e2e_dir = project_root / "e2e"
    
    print("🧪 Todo List App - Comprehensive Test Suite")
    print("="*60)
    print("This will run all tests in isolated environments:")
    print("• Backend unit tests (in-memory database)")
    print("• E2E tests (separate test database + ports 8001/5174)")
    print("="*60)
    
    results = []
    
    # 1. Backend Unit Tests
    print("\n📋 Phase 1: Backend Unit Tests")
    print("Uses in-memory SQLite database for complete isolation")
    
    backend_success = run_command(
        ["python3", "-m", "pytest", "test_api.py", "-v", "--tb=short"],
        cwd=backend_dir,
        description="Backend Unit Tests"
    )
    results.append(("Backend Unit Tests", backend_success))
    
    # 2. E2E Tests (with auto-spawned services)
    print("\n🌐 Phase 2: End-to-End Tests")
    print("Spawns isolated test services on ports 8001 (backend) and 5174 (frontend)")
    print("Uses separate test database in temp directory")
    
    e2e_success = run_command(
        ["python3", "-m", "pytest", "test_todo_e2e.py::TestTodoAppE2E::test_app_title", 
         "test_todo_e2e.py::TestTodoAppE2E::test_create_todo",
         "test_todo_e2e.py::TestTodoAppE2E::test_toggle_todo_completion",
         "test_todo_e2e.py::TestTodoAppE2E::test_delete_todo",
         "test_todo_e2e.py::TestTodoAppE2E::test_complex_workflow",
         "-v", "--tb=short"],
        cwd=e2e_dir,
        description="End-to-End Tests (Core Workflows)"
    )
    results.append(("End-to-End Tests", e2e_success))
    
    # Results Summary
    print("\n" + "="*60)
    print("🎯 TEST RESULTS SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<25} {status}")
        if not success:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! The application is ready for production.")
        return 0
    else:
        print("💥 SOME TESTS FAILED! Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
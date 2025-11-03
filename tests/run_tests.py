#!/usr/bin/env python3
"""
Test runner for markdown-headings package
"""

import sys
import subprocess
from pathlib import Path


def run_tests():
    """Run all tests in the tests directory."""
    test_dir = Path(__file__).parent
    
    # Find all test files
    test_files = list(test_dir.glob("test_*.py"))
    
    if not test_files:
        print("No test files found!")
        return 1
    
    print(f"Running {len(test_files)} test files...")
    print("=" * 50)
    
    failed_tests = []
    
    for test_file in test_files:
        print(f"Running {test_file.name}...")
        try:
            result = subprocess.run([
                sys.executable, str(test_file)
            ], capture_output=True, text=True, cwd=test_dir.parent)
            
            if result.returncode == 0:
                print(f"✓ {test_file.name} passed")
                if result.stdout:
                    print("  Output:")
                    for line in result.stdout.strip().split('\n'):
                        print(f"    {line}")
            else:
                print(f"✗ {test_file.name} failed")
                failed_tests.append(test_file.name)
                if result.stderr:
                    print("  Error:")
                    for line in result.stderr.strip().split('\n'):
                        print(f"    {line}")
                if result.stdout:
                    print("  Output:")
                    for line in result.stdout.strip().split('\n'):
                        print(f"    {line}")
        
        except Exception as e:
            print(f"✗ {test_file.name} failed with exception: {e}")
            failed_tests.append(test_file.name)
        
        print("-" * 30)
    
    # Summary
    print(f"\nTest Summary:")
    print(f"Total tests: {len(test_files)}")
    print(f"Passed: {len(test_files) - len(failed_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print(f"Failed tests: {', '.join(failed_tests)}")
        return 1
    else:
        print("All tests passed! ✓")
        return 0


if __name__ == "__main__":
    exit(run_tests())
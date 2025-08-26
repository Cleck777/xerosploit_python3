#!/usr/bin/env python3
"""
Test script to verify Xerosploit installation and basic functionality
"""

import sys
import os
import subprocess
from pathlib import Path

def test_imports():
    """Test if required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tabulate
        print("✓ tabulate imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import tabulate: {e}")
        return False
    
    try:
        import terminaltables
        print("✓ terminaltables imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import terminaltables: {e}")
        return False
    
    try:
        import banner
        print("✓ banner module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import banner: {e}")
        return False
    
    return True

def test_system_dependencies():
    """Test if system dependencies are available"""
    print("\nTesting system dependencies...")
    
    dependencies = {
        'nmap': 'Network mapping tool',
        'hping3': 'Network packet crafting tool',
        'gem': 'Ruby package manager'
    }
    
    all_good = True
    for cmd, desc in dependencies.items():
        try:
            result = subprocess.run(['which', cmd], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {cmd} found: {result.stdout.strip()}")
            else:
                print(f"✗ {cmd} not found ({desc})")
                all_good = False
        except Exception as e:
            print(f"✗ Error checking {cmd}: {e}")
            all_good = False
    
    return all_good

def test_bettercap():
    """Test if bettercap gem is installed"""
    print("\nTesting bettercap gem...")
    
    try:
        result = subprocess.run(['gem', 'list', 'bettercap'], capture_output=True, text=True)
        if 'bettercap' in result.stdout:
            print("✓ bettercap gem is installed")
            return True
        else:
            print("✗ bettercap gem not found")
            return False
    except Exception as e:
        print(f"✗ Error checking bettercap: {e}")
        return False

def test_banner():
    """Test banner functionality"""
    print("\nTesting banner functionality...")
    
    try:
        import banner
        header = banner.xe_header()
        if header and len(header) > 0:
            print("✓ Banner generation works")
            return True
        else:
            print("✗ Banner generation failed")
            return False
    except Exception as e:
        print(f"✗ Error testing banner: {e}")
        return False

def main():
    """Run all tests"""
    print("Xerosploit Installation Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_system_dependencies,
        test_bettercap,
        test_banner
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'=' * 40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Xerosploit should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

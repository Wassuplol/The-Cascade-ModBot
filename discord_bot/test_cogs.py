#!/usr/bin/env python3
"""
Simple test script to verify all cogs can be imported without errors
"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cog_imports():
    """Test that all cogs can be imported without errors"""
    print("Testing cog imports...")
    
    cogs_to_test = [
        "cogs.economy",
        "cogs.moderation", 
        "cogs.fun",
        "cogs.utility",
        "cogs.music"
    ]
    
    for cog_path in cogs_to_test:
        try:
            module = __import__(cog_path, fromlist=[''])
            print(f"✓ Successfully imported {cog_path}")
        except ImportError as e:
            print(f"✗ Failed to import {cog_path}: {e}")
            return False
        except Exception as e:
            print(f"✗ Error importing {cog_path}: {e}")
            return False
    
    print("\nAll cogs imported successfully!")
    return True

if __name__ == "__main__":
    success = test_cog_imports()
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
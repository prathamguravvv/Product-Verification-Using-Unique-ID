"""
Simple Run Script
Run this file to test the framework quickly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import ImageIdentityFramework


def main():
    print("="*60)
    print("Image Identity Framework - Quick Test")
    print("="*60)
    
    # Initialize
    framework = ImageIdentityFramework()
    print("\n✓ Framework initialized\n")
    
    # Generate image
    print("Generating identifiable image...")
    image, pattern_id, hash_value = framework.generate_identifiable_image("test_image.png")
    
    print(f"✓ Image generated!")
    print(f"  Pattern ID: {pattern_id}")
    print(f"  Hash: {hash_value[:32]}...")
    print(f"  Saved: test_image.png\n")
    
    # Verify image
    print("Verifying image...")
    result = framework.verify_image("test_image.png")
    
    print(f"✓ Verification complete!")
    print(f"  Extracted ID: {result['pattern_id']}")
    print(f"  Valid: {result['is_valid']}")
    print(f"  Tampered: {result['tampered']}\n")
    
    # Check match
    if result['pattern_id'] == pattern_id:
        print("✓ SUCCESS: Pattern ID matches!")
    else:
        print("✗ ERROR: Pattern ID mismatch!")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

"""
Generate Sample Images
Creates multiple sample images to showcase pattern variety
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import ImageIdentityFramework


def main():
    print("="*60)
    print("Generating Sample Images with Random Patterns")
    print("="*60)
    
    # Initialize
    framework = ImageIdentityFramework()
    
    # Create output directory
    output_dir = Path("sample_images")
    output_dir.mkdir(exist_ok=True)
    
    # Generate 10 sample images
    num_samples = 10
    print(f"\nGenerating {num_samples} unique images...\n")
    
    for i in range(num_samples):
        filename = output_dir / f"sample_{i+1:02d}.png"
        image, pattern_id, hash_value = framework.generate_identifiable_image(str(filename))
        
        print(f"✓ {filename.name}")
        print(f"  Pattern ID: {pattern_id}")
        print(f"  Hash: {hash_value[:32]}...")
        
        # Verify immediately
        result = framework.verify_image(str(filename))
        if result['is_valid'] and result['pattern_id'] == pattern_id:
            print(f"  Verified: ✓\n")
        else:
            print(f"  Verified: ✗ ERROR\n")
    
    print("="*60)
    print(f"Generated {num_samples} images in: {output_dir.absolute()}")
    print("\nPattern Types Include:")
    print("  • Vertical gradients")
    print("  • Horizontal gradients")
    print("  • Diagonal gradients")
    print("  • Radial gradients")
    print("  • Checkerboard patterns")
    print("  • Wave patterns")
    print("\nShapes Include:")
    print("  • Circles")
    print("  • Rectangles")
    print("  • Triangles")
    print("  • Diamonds")
    print("  • Pentagons")
    print("  • Stars")
    print("  • Random lines")
    print("="*60)


if __name__ == "__main__":
    main()

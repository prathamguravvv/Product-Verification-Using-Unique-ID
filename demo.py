"""
Demo Script - Complete Working Example
Demonstrates the full Image Identity Framework
"""

from src.main import ImageIdentityFramework
from pathlib import Path
import sys


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def main():
    """Run complete demo."""
    
    print_header("Image Identity Framework - Demo")
    print("Database-free image identification system")
    print("Developers: Sohan, Pratham, Vighnesh, Ronit\n")
    
    # Initialize framework
    print("Initializing framework...")
    framework = ImageIdentityFramework()
    print("✓ Framework initialized successfully!\n")
    
    # Create output directory
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    
    # Demo 1: Generate single image
    print_header("Demo 1: Generate Identifiable Image")
    
    image_path = output_dir / "demo_image_1.png"
    print(f"Generating image: {image_path}")
    
    image, pattern_id, image_hash = framework.generate_identifiable_image(str(image_path))
    
    print(f"✓ Image generated successfully!")
    print(f"  Pattern ID: {pattern_id}")
    print(f"  Hash: {image_hash[:32]}...")
    print(f"  Size: {image.size}")
    print(f"  Saved to: {image_path}")
    
    # Demo 2: Verify the image
    print_header("Demo 2: Verify Image Identity")
    
    print(f"Verifying image: {image_path}")
    result = framework.verify_image(str(image_path))
    
    print(f"✓ Verification complete!")
    print(f"  Extracted Pattern ID: {result['pattern_id']}")
    print(f"  Valid: {result['is_valid']}")
    print(f"  Tampered: {result['tampered']}")
    print(f"  Verification Token: {result['verification_token']}")
    
    # Demo 3: Test extraction accuracy
    print_header("Demo 3: Test Extraction Accuracy")
    
    if result['pattern_id'] == pattern_id:
        print("✓ SUCCESS: Extracted pattern ID matches original!")
        print(f"  Original:  {pattern_id}")
        print(f"  Extracted: {result['pattern_id']}")
    else:
        print("✗ ERROR: Pattern ID mismatch!")
        print(f"  Original:  {pattern_id}")
        print(f"  Extracted: {result['pattern_id']}")
    
    # Demo 4: Batch generation
    print_header("Demo 4: Batch Generation")
    
    batch_dir = output_dir / "batch"
    print(f"Generating 3 images in: {batch_dir}")
    
    batch_results = framework.batch_generate(3, str(batch_dir))
    
    print(f"✓ Generated {len(batch_results)} images:")
    for item in batch_results:
        print(f"  {item['index']}. {Path(item['path']).name}")
        print(f"     Pattern ID: {item['pattern_id']}")
    
    # Demo 5: Verify batch images
    print_header("Demo 5: Verify Batch Images")
    
    for item in batch_results:
        result = framework.verify_image(item['path'])
        status = "✓" if result['is_valid'] and not result['tampered'] else "✗"
        print(f"{status} {Path(item['path']).name}: Valid={result['is_valid']}, Tampered={result['tampered']}")
    
    # Summary
    print_header("Demo Complete!")
    print("All operations completed successfully!")
    print(f"\nGenerated files are in: {output_dir.absolute()}")
    print("\nKey Features Demonstrated:")
    print("  ✓ Pattern ID generation")
    print("  ✓ Unique image generation")
    print("  ✓ Steganographic embedding")
    print("  ✓ Identity extraction")
    print("  ✓ Cryptographic verification")
    print("  ✓ Batch processing")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

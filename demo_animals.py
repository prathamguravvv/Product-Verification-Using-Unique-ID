"""
Animal Image Demo
Generate unique animal-themed identifiable images
"""

from src.main import ImageIdentityFramework
from pathlib import Path


def main():
    print("="*70)
    print("  🐾 Animal Image Identity Framework Demo 🐾")
    print("="*70)
    print("\nGenerating unique animal-themed images with embedded identities...\n")
    
    # Initialize with animal style
    framework = ImageIdentityFramework(image_style="animal")
    
    # Create output directory
    output_dir = Path("animal_output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate multiple animal images
    num_images = 5
    print(f"Generating {num_images} unique animal images...\n")
    
    results = []
    for i in range(num_images):
        image_path = output_dir / f"animal_{i+1}.png"
        
        # Generate image
        image, pattern_id, hash_value = framework.generate_identifiable_image(str(image_path))
        
        print(f"✓ Animal {i+1}:")
        print(f"  File: {image_path.name}")
        print(f"  Pattern ID: {pattern_id}")
        print(f"  Hash: {hash_value[:24]}...")
        print()
        
        results.append({
            'path': str(image_path),
            'pattern_id': pattern_id,
            'hash': hash_value
        })
    
    # Verify all images
    print("="*70)
    print("Verifying all generated images...\n")
    
    all_valid = True
    for i, item in enumerate(results, 1):
        result = framework.verify_image(item['path'])
        
        status = "✓" if result['is_valid'] and not result['tampered'] else "✗"
        print(f"{status} Animal {i}: ", end="")
        
        if result['pattern_id'] == item['pattern_id']:
            print(f"Valid ✓ (ID matches)")
        else:
            print(f"Error ✗ (ID mismatch)")
            all_valid = False
    
    # Summary
    print("\n" + "="*70)
    if all_valid:
        print("🎉 SUCCESS! All animal images generated and verified!")
    else:
        print("⚠️  Some images had verification issues")
    
    print(f"\n📁 Images saved in: {output_dir.absolute()}")
    print("\nEach image contains:")
    print("  • Unique animal-themed design")
    print("  • Embedded pattern identifier (invisible)")
    print("  • Cryptographic hash for verification")
    print("  • Tamper detection capability")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()

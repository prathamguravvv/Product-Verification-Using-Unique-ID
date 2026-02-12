"""
Demo Script for Sohan's Modules
Pattern Generator + Image Generator

This demonstrates the complete workflow of:
1. Generating unique pattern IDs
2. Creating visually distinct images
3. Preparing images for steganographic embedding
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.pattern_generator import PatternGenerator
from src.image_generator import ImageGenerator


def main():
    print("=" * 60)
    print("Database-Free Image Identity Framework")
    print("Demo: Pattern Generation & Image Generation")
    print("Developer: Sohan")
    print("=" * 60)
    print()
    
    # Initialize generators
    print("Initializing generators...")
    pattern_gen = PatternGenerator(prefix="DEMO")
    image_gen = ImageGenerator(image_size=(512, 512))
    print("✓ Generators initialized\n")
    
    # Generate single pattern and image
    print("--- Single Image Generation ---")
    pattern_id = pattern_gen.generate_pattern_id()
    print(f"Pattern ID: {pattern_id}")
    print(f"Valid: {pattern_gen.validate_pattern_id(pattern_id)}")
    print(f"Hash: {pattern_gen.get_hash_from_pattern(pattern_id)}")
    
    image = image_gen.generate_image(pattern_id)
    filename = f"output_{pattern_id}.png"
    image_gen.save_image(image, filename)
    print(f"✓ Image saved: {filename}\n")
    
    # Generate batch
    print("--- Batch Generation (5 images) ---")
    batch_ids = pattern_gen.generate_batch(5)
    
    # Create output directory
    os.makedirs("batch_output", exist_ok=True)
    
    for i, pid in enumerate(batch_ids, 1):
        print(f"{i}. Generating image for {pid}...")
        img = image_gen.generate_image(pid)
        filename = f"batch_output/image_{i}_{pid}.png"
        image_gen.save_image(img, filename)
    
    print("\n✓ Batch generation complete!")
    
    # Deterministic generation demo
    print("\n--- Deterministic Generation ---")
    seed = "my-custom-seed-123"
    det_id1 = pattern_gen.generate_deterministic_id(seed)
    det_id2 = pattern_gen.generate_deterministic_id(seed)
    
    print(f"Seed: {seed}")
    print(f"ID 1: {det_id1}")
    print(f"ID 2: {det_id2}")
    print(f"Hash Match: {det_id1.split('-')[1] == det_id2.split('-')[1]}")
    
    # Generate image from deterministic ID
    det_image = image_gen.generate_image(det_id1)
    det_filename = f"deterministic_{det_id1}.png"
    image_gen.save_image(det_image, det_filename)
    
    # Statistics
    print("\n" + "=" * 60)
    print("Generation Statistics")
    print("=" * 60)
    print(f"Total IDs generated: {len(pattern_gen.generated_ids)}")
    print(f"All IDs unique: {len(pattern_gen.generated_ids) == len(batch_ids) + 1}")
    print(f"Image size: {image.size}")
    print(f"Image mode: {image.mode}")
    
    print("\n✓ Demo completed successfully!")
    print("\nNext Steps:")
    print("- Images are ready for steganographic embedding (Pratham's module)")
    print("- Pattern IDs can be embedded into images")
    print("- Images can be verified using cryptographic hashing (Vighnesh's module)")


if __name__ == "__main__":
    main()

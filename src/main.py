"""
Main Pipeline Module
Developer: Ronit

Integrates all modules into a unified pipeline.
"""

from pathlib import Path
from .pattern_generator import PatternGenerator
from .image_generator import ImageGenerator
from .steganography import SteganographyEncoder
from .identity_extractor import IdentityExtractor
from .crypto_verifier import CryptoVerifier
from PIL import Image


class ImageIdentityFramework:
    """Main framework integrating all modules."""
    
    def __init__(self):
        """Initialize all components."""
        self.pattern_gen = PatternGenerator()
        self.image_gen = ImageGenerator()
        self.encoder = SteganographyEncoder()
        self.extractor = IdentityExtractor()
        self.verifier = CryptoVerifier()
        
    def generate_identifiable_image(self, save_path=None):
        """
        Complete pipeline: Generate image with embedded identity.
        
        Args:
            save_path: Optional path to save the image
            
        Returns:
            tuple: (image, pattern_id, hash)
        """
        # Step 1: Generate pattern ID
        pattern_id = self.pattern_gen.generate_pattern_id()
        
        # Step 2: Generate base image
        base_image = self.image_gen.generate_image(pattern_id)
        
        # Step 3: Embed identity
        identifiable_image = self.encoder.embed_identity(base_image, pattern_id)
        
        # Step 4: Calculate hash
        image_hash = self.verifier.calculate_image_hash(identifiable_image)
        
        # Step 5: Save if path provided
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            identifiable_image.save(save_path)
        
        return identifiable_image, pattern_id, image_hash
    
    def verify_image(self, image_path):
        """
        Complete pipeline: Verify image identity.
        
        Args:
            image_path: Path to image file
            
        Returns:
            dict: Verification results
        """
        # Step 1: Load image
        image = Image.open(image_path)
        
        # Step 2: Extract identity
        extracted_id = self.extractor.extract_identity(image)
        
        # Step 3: Verify authenticity
        verification_result = self.verifier.verify_identity(image, extracted_id)
        
        return verification_result
    
    def batch_generate(self, count, output_dir):
        """
        Generate multiple identifiable images.
        
        Args:
            count: Number of images to generate
            output_dir: Directory to save images
            
        Returns:
            list: List of generated image info
        """
        results = []
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i in range(count):
            save_path = output_path / f"image_{i+1:04d}.png"
            image, pattern_id, image_hash = self.generate_identifiable_image(str(save_path))
            
            results.append({
                'index': i + 1,
                'path': str(save_path),
                'pattern_id': pattern_id,
                'hash': image_hash
            })
        
        return results


if __name__ == "__main__":
    # Test the framework
    framework = ImageIdentityFramework()
    print("Image Identity Framework initialized")
    
    # Test generation
    print("\nGenerating test image...")
    image, pattern_id, hash_value = framework.generate_identifiable_image("test_output.png")
    print(f"Pattern ID: {pattern_id}")
    print(f"Hash: {hash_value}")
    
    # Test verification
    print("\nVerifying test image...")
    result = framework.verify_image("test_output.png")
    print(f"Verification result: {result}")

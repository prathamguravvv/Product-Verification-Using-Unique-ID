"""
Cryptographic Verifier Module
Developer: Vighnesh

Handles cryptographic verification and tamper detection.
"""

import hashlib
from datetime import datetime
from PIL import Image
import io


class CryptoVerifier:
    """Verifies identity authenticity and detects tampering."""
    
    def __init__(self, hash_algorithm="sha256"):
        """
        Initialize the crypto verifier.
        
        Args:
            hash_algorithm: Hash algorithm to use
        """
        self.hash_algorithm = hash_algorithm
        
    def verify_identity(self, image, extracted_id, original_hash=None):
        """
        Verify image identity and authenticity.
        
        Args:
            image: PIL Image object
            extracted_id: Extracted pattern identifier
            original_hash: Optional original hash for comparison
            
        Returns:
            dict: Verification results
        """
        # Calculate current image hash
        current_hash = self.calculate_image_hash(image)
        
        # Verify pattern ID format
        is_valid_format = self.validate_pattern_format(extracted_id)
        
        # Check for tampering if original hash provided
        tampered = False
        if original_hash:
            tampered = self.detect_tampering(image, original_hash)
        
        # Generate verification token
        token = self.generate_verification_token(extracted_id)
        
        return {
            'pattern_id': extracted_id,
            'is_valid': is_valid_format,
            'tampered': tampered,
            'current_hash': current_hash,
            'original_hash': original_hash,
            'verification_token': token,
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_image_hash(self, image):
        """
        Calculate cryptographic hash of image.
        
        Args:
            image: PIL Image object
            
        Returns:
            str: Hexadecimal hash string
        """
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        # Calculate hash
        if self.hash_algorithm == "sha256":
            hash_obj = hashlib.sha256(img_bytes)
        elif self.hash_algorithm == "md5":
            hash_obj = hashlib.md5(img_bytes)
        else:
            hash_obj = hashlib.sha256(img_bytes)
        
        return hash_obj.hexdigest()
    
    def detect_tampering(self, image, original_hash):
        """
        Detect if image has been tampered with.
        
        Args:
            image: PIL Image object
            original_hash: Original image hash
            
        Returns:
            bool: True if tampering detected
        """
        current_hash = self.calculate_image_hash(image)
        return not self.validate_hash_consistency(current_hash, original_hash)
    
    def generate_verification_token(self, pattern_id):
        """
        Generate verification token for pattern ID.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            str: Verification token
        """
        # Combine pattern_id with timestamp
        timestamp = datetime.now().isoformat()
        combined = f"{pattern_id}-{timestamp}"
        
        # Generate token hash
        token_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        return f"TOKEN-{token_hash[:16].upper()}"
    
    def validate_hash_consistency(self, hash1, hash2):
        """
        Validate consistency between two hashes.
        
        Args:
            hash1: First hash
            hash2: Second hash
            
        Returns:
            bool: True if hashes match
        """
        return hash1 == hash2
    
    def validate_pattern_format(self, pattern_id):
        """
        Validate pattern ID format.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            bool: True if valid format
        """
        if not pattern_id or not isinstance(pattern_id, str):
            return False
        
        # Check if starts with PATTERN-
        if not pattern_id.startswith("PATTERN-"):
            return False
        
        # Check length
        if len(pattern_id) < 10:
            return False
        
        return True


if __name__ == "__main__":
    # Test the crypto verifier
    verifier = CryptoVerifier()
    print("Crypto Verifier initialized")
    
    # Test with dummy image
    test_image = Image.new('RGB', (100, 100), color='red')
    hash_value = verifier.calculate_image_hash(test_image)
    print(f"Image hash: {hash_value}")

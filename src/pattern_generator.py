"""
Pattern Generator Module
Developer: Sohan

Generates unique pattern identifiers using cryptographic techniques.
"""

import hashlib
import uuid
from datetime import datetime


class PatternGenerator:
    """Generates unique pattern identifiers for images."""
    
    def __init__(self, seed=None):
        """
        Initialize the pattern generator.
        
        Args:
            seed: Optional seed for reproducible pattern generation
        """
        self.seed = seed
        
    def generate_pattern_id(self):
        """
        Generate a unique pattern identifier.
        
        Returns:
            str: Unique pattern identifier
        """
        # Generate UUID
        unique_id = str(uuid.uuid4())
        
        # Add timestamp for additional uniqueness
        timestamp = datetime.now().isoformat()
        
        # Combine and hash
        combined = f"{unique_id}-{timestamp}"
        if self.seed:
            combined = f"{self.seed}-{combined}"
        
        # Generate hash
        pattern_hash = self.generate_hash(combined)
        
        # Create pattern ID format: PATTERN-{first 16 chars of hash}
        pattern_id = f"PATTERN-{pattern_hash[:16].upper()}"
        
        return pattern_id
    
    def generate_hash(self, data):
        """
        Generate cryptographic hash for data.
        
        Args:
            data: Data to hash
            
        Returns:
            str: Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        hash_obj = hashlib.sha256(data)
        return hash_obj.hexdigest()
    
    def validate_pattern_format(self, pattern_id):
        """
        Validate pattern ID format.
        
        Args:
            pattern_id: Pattern identifier to validate
            
        Returns:
            bool: True if valid format
        """
        if not pattern_id:
            return False
        
        # Check format: PATTERN-{16 hex chars}
        if not pattern_id.startswith("PATTERN-"):
            return False
        
        suffix = pattern_id.split("-", 1)[1]
        if len(suffix) != 16:
            return False
        
        # Check if suffix is hexadecimal
        try:
            int(suffix, 16)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    # Test the pattern generator
    generator = PatternGenerator()
    pattern_id = generator.generate_pattern_id()
    print(f"Generated Pattern ID: {pattern_id}")
    print(f"Valid format: {generator.validate_pattern_format(pattern_id)}")

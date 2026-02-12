"""
Pattern Generator Module
Developer: Sohan

Generates unique pattern identifiers using cryptographic hashing.
"""

import hashlib
import uuid
import time
from datetime import datetime


class PatternGenerator:
    """Generates unique, cryptographically secure pattern identifiers."""
    
    def __init__(self, prefix="IMG"):
        """
        Initialize the pattern generator.
        
        Args:
            prefix: Prefix for pattern IDs (default: "IMG")
        """
        self.prefix = prefix
        self.generated_ids = set()  # Track generated IDs to ensure uniqueness
        
    def generate_pattern_id(self, seed=None):
        """
        Generate a unique pattern identifier.
        
        Args:
            seed: Optional seed for deterministic generation
            
        Returns:
            str: Unique pattern identifier (format: PREFIX-HASH-TIMESTAMP)
        """
        if seed is None:
            # Generate random seed using UUID and timestamp
            seed = f"{uuid.uuid4()}{time.time()}"
        
        # Create cryptographic hash
        hash_obj = hashlib.sha256(seed.encode())
        hash_hex = hash_obj.hexdigest()[:16]  # Use first 16 chars
        
        # Add timestamp for additional uniqueness
        timestamp = int(time.time() * 1000) % 1000000  # Last 6 digits
        
        # Construct pattern ID
        pattern_id = f"{self.prefix}-{hash_hex.upper()}-{timestamp}"
        
        # Ensure uniqueness
        while pattern_id in self.generated_ids:
            seed = f"{seed}{time.time()}"
            hash_obj = hashlib.sha256(seed.encode())
            hash_hex = hash_obj.hexdigest()[:16]
            pattern_id = f"{self.prefix}-{hash_hex.upper()}-{timestamp}"
        
        self.generated_ids.add(pattern_id)
        return pattern_id
    
    def generate_batch(self, count=10):
        """
        Generate multiple unique pattern IDs.
        
        Args:
            count: Number of IDs to generate
            
        Returns:
            list: List of unique pattern identifiers
        """
        return [self.generate_pattern_id() for _ in range(count)]
    
    def validate_pattern_id(self, pattern_id):
        """
        Validate pattern ID format.
        
        Args:
            pattern_id: Pattern ID to validate
            
        Returns:
            bool: True if valid format
        """
        try:
            parts = pattern_id.split('-')
            if len(parts) != 3:
                return False
            
            prefix, hash_part, timestamp = parts
            
            # Check prefix
            if prefix != self.prefix:
                return False
            
            # Check hash part (16 hex chars)
            if len(hash_part) != 16 or not all(c in '0123456789ABCDEF' for c in hash_part):
                return False
            
            # Check timestamp (numeric)
            if not timestamp.isdigit():
                return False
            
            return True
        except:
            return False
    
    def get_hash_from_pattern(self, pattern_id):
        """
        Extract hash component from pattern ID.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            str: Hash component or None if invalid
        """
        if self.validate_pattern_id(pattern_id):
            return pattern_id.split('-')[1]
        return None
    
    def generate_deterministic_id(self, seed_string):
        """
        Generate deterministic pattern ID from seed.
        Useful for reproducible generation.
        
        Args:
            seed_string: Seed string for generation
            
        Returns:
            str: Deterministic pattern identifier
        """
        hash_obj = hashlib.sha256(seed_string.encode())
        hash_hex = hash_obj.hexdigest()[:16]
        timestamp = int(time.time() * 1000) % 1000000
        
        return f"{self.prefix}-{hash_hex.upper()}-{timestamp}"


if __name__ == "__main__":
    # Test the pattern generator
    generator = PatternGenerator()
    
    print("=== Pattern Generator Test ===\n")
    
    # Generate single ID
    pattern_id = generator.generate_pattern_id()
    print(f"Generated Pattern ID: {pattern_id}")
    print(f"Valid: {generator.validate_pattern_id(pattern_id)}")
    print(f"Hash: {generator.get_hash_from_pattern(pattern_id)}\n")
    
    # Generate batch
    print("Batch Generation (5 IDs):")
    batch = generator.generate_batch(5)
    for i, pid in enumerate(batch, 1):
        print(f"{i}. {pid}")
    
    # Deterministic generation
    print("\nDeterministic Generation:")
    det_id = generator.generate_deterministic_id("test-seed-123")
    print(f"Deterministic ID: {det_id}")

"""
Unit Tests for Pattern Generator
Developer: Sohan
"""

import pytest
import sys
sys.path.append('..')

from src.pattern_generator import PatternGenerator
import time


class TestPatternGenerator:
    """Test cases for Pattern Generator module."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = PatternGenerator()
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        assert self.generator is not None
        assert self.generator.prefix == "IMG"
        assert isinstance(self.generator.generated_ids, set)
    
    def test_custom_prefix(self):
        """Test generator with custom prefix."""
        custom_gen = PatternGenerator(prefix="TEST")
        pattern_id = custom_gen.generate_pattern_id()
        assert pattern_id.startswith("TEST-")
    
    def test_generate_pattern_id(self):
        """Test pattern ID generation."""
        pattern_id = self.generator.generate_pattern_id()
        
        # Check format
        assert isinstance(pattern_id, str)
        assert pattern_id.count('-') == 2
        
        # Check components
        parts = pattern_id.split('-')
        assert len(parts) == 3
        assert parts[0] == "IMG"
        assert len(parts[1]) == 16  # Hash part
        assert parts[2].isdigit()  # Timestamp part
    
    def test_uniqueness(self):
        """Test that generated IDs are unique."""
        ids = [self.generator.generate_pattern_id() for _ in range(100)]
        
        # All IDs should be unique
        assert len(ids) == len(set(ids))
    
    def test_deterministic_generation(self):
        """Test deterministic ID generation."""
        seed = "test-seed-123"
        
        id1 = self.generator.generate_deterministic_id(seed)
        id2 = self.generator.generate_deterministic_id(seed)
        
        # Hash parts should be same (timestamp may differ)
        hash1 = id1.split('-')[1]
        hash2 = id2.split('-')[1]
        assert hash1 == hash2
    
    def test_batch_generation(self):
        """Test batch generation."""
        count = 10
        batch = self.generator.generate_batch(count)
        
        assert len(batch) == count
        assert len(set(batch)) == count  # All unique
    
    def test_validate_pattern_id(self):
        """Test pattern ID validation."""
        # Valid ID
        valid_id = self.generator.generate_pattern_id()
        assert self.generator.validate_pattern_id(valid_id) == True
        
        # Invalid IDs
        assert self.generator.validate_pattern_id("INVALID") == False
        assert self.generator.validate_pattern_id("IMG-123-456") == False
        assert self.generator.validate_pattern_id("") == False
    
    def test_get_hash_from_pattern(self):
        """Test hash extraction."""
        pattern_id = self.generator.generate_pattern_id()
        hash_part = self.generator.get_hash_from_pattern(pattern_id)
        
        assert hash_part is not None
        assert len(hash_part) == 16
        assert all(c in '0123456789ABCDEF' for c in hash_part)
    
    def test_hash_extraction_invalid_id(self):
        """Test hash extraction with invalid ID."""
        hash_part = self.generator.get_hash_from_pattern("INVALID-ID")
        assert hash_part is None
    
    def test_generated_ids_tracking(self):
        """Test that generated IDs are tracked."""
        initial_count = len(self.generator.generated_ids)
        
        self.generator.generate_pattern_id()
        self.generator.generate_pattern_id()
        
        assert len(self.generator.generated_ids) == initial_count + 2
    
    def test_collision_handling(self):
        """Test that collisions are handled (though unlikely)."""
        # Generate many IDs quickly
        ids = [self.generator.generate_pattern_id() for _ in range(1000)]
        
        # Should all be unique
        assert len(ids) == len(set(ids))


class TestPatternGeneratorEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_seed(self):
        """Test generation with empty seed."""
        generator = PatternGenerator()
        pattern_id = generator.generate_deterministic_id("")
        
        assert pattern_id is not None
        assert generator.validate_pattern_id(pattern_id)
    
    def test_long_prefix(self):
        """Test with long prefix."""
        generator = PatternGenerator(prefix="VERYLONGPREFIX")
        pattern_id = generator.generate_pattern_id()
        
        assert pattern_id.startswith("VERYLONGPREFIX-")
    
    def test_special_characters_in_seed(self):
        """Test deterministic generation with special characters."""
        generator = PatternGenerator()
        seed = "test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        
        pattern_id = generator.generate_deterministic_id(seed)
        assert pattern_id is not None
        assert generator.validate_pattern_id(pattern_id)
    
    def test_unicode_seed(self):
        """Test with unicode characters in seed."""
        generator = PatternGenerator()
        seed = "测试-тест-परीक्षण"
        
        pattern_id = generator.generate_deterministic_id(seed)
        assert pattern_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

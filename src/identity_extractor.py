"""
Identity Extractor Module
Developer: Pratham

Extracts embedded pattern identifiers from images.
"""

from PIL import Image
import numpy as np


class IdentityExtractor:
    """Extracts embedded identifiers from images."""
    
    def __init__(self, method="LSB"):
        """
        Initialize the identity extractor.
        
        Args:
            method: Extraction method (must match embedding method)
        """
        self.method = method
        
    def extract_identity(self, image):
        """
        Extract pattern identifier from image.
        
        Args:
            image: PIL Image object with embedded identity
            
        Returns:
            str: Extracted pattern identifier
        """
        # Convert image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # First extract the length (32 bits)
        length_binary = self.extract_lsb(img_array, 32)
        data_length = int(length_binary, 2)
        
        # Extract the actual data
        binary_data = self.extract_lsb(img_array, data_length, offset=32)
        
        # Convert binary to string
        extracted_data = self.binary_to_string(binary_data)
        
        return extracted_data
    
    def extract_lsb(self, image_array, data_length, offset=0):
        """
        Extract data using LSB method.
        
        Args:
            image_array: Numpy array of image
            data_length: Expected length of embedded data in bits
            offset: Bit offset to start extraction
            
        Returns:
            str: Binary string of extracted data
        """
        flat_array = image_array.flatten()
        
        binary_data = ''
        for i in range(offset, offset + data_length):
            # Extract LSB
            binary_data += str(flat_array[i] & 1)
        
        return binary_data
    
    def binary_to_string(self, binary_data):
        """
        Convert binary data to string.
        
        Args:
            binary_data: Binary string
            
        Returns:
            str: Decoded string
        """
        # Split into 8-bit chunks
        chars = []
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        
        return ''.join(chars)
    
    def validate_extracted_data(self, data):
        """
        Validate extracted data integrity.
        
        Args:
            data: Extracted data
            
        Returns:
            bool: True if data is valid
        """
        # Check if data is printable and not empty
        if not data:
            return False
        
        # Check if all characters are printable
        return all(c.isprintable() or c.isspace() for c in data)


if __name__ == "__main__":
    # Test the identity extractor
    extractor = IdentityExtractor()
    print("Identity Extractor initialized")

"""
Steganography Module
Developer: Pratham

Embeds pattern identifiers into images using steganographic techniques.
"""

from PIL import Image
import numpy as np


class SteganographyEncoder:
    """Embeds data into images while preserving visual quality."""
    
    def __init__(self, method="LSB"):
        """
        Initialize the steganography encoder.
        
        Args:
            method: Embedding method ("LSB", "DCT", "DWT")
        """
        self.method = method
        
    def embed_identity(self, image, pattern_id):
        """
        Embed pattern identifier into image.
        
        Args:
            image: PIL Image object
            pattern_id: Pattern identifier to embed
            
        Returns:
            PIL.Image: Image with embedded identity
        """
        # Convert image to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert pattern_id to binary
        binary_data = self.encode_to_binary(pattern_id)
        
        # Add length header (32 bits for data length)
        data_length = len(binary_data)
        length_binary = format(data_length, '032b')
        full_binary = length_binary + binary_data
        
        # Check capacity
        capacity = self.calculate_capacity(image)
        if len(full_binary) > capacity:
            raise ValueError(f"Data too large. Need {len(full_binary)} bits, have {capacity} bits")
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Embed using LSB
        embedded_array = self.embed_lsb(img_array, full_binary)
        
        # Convert back to PIL Image
        return Image.fromarray(embedded_array.astype('uint8'), 'RGB')
    
    def encode_to_binary(self, data):
        """
        Convert data to binary representation.
        
        Args:
            data: Data to encode
            
        Returns:
            str: Binary string
        """
        binary = ''.join(format(ord(char), '08b') for char in data)
        return binary
    
    def embed_lsb(self, image_array, binary_data):
        """
        Embed data using Least Significant Bit method.
        
        Args:
            image_array: Numpy array of image
            binary_data: Binary string to embed
            
        Returns:
            numpy.ndarray: Modified image array
        """
        flat_array = image_array.flatten()
        
        # Embed each bit
        for i, bit in enumerate(binary_data):
            # Modify LSB of pixel value
            flat_array[i] = (flat_array[i] & 0xFE) | int(bit)
        
        # Reshape back to original shape
        return flat_array.reshape(image_array.shape)
    
    def calculate_capacity(self, image):
        """
        Calculate embedding capacity of image.
        
        Args:
            image: PIL Image
            
        Returns:
            int: Maximum bits that can be embedded
        """
        width, height = image.size
        # RGB image has 3 channels, we can use 1 bit per channel
        return width * height * 3


if __name__ == "__main__":
    # Test the steganography encoder
    encoder = SteganographyEncoder()
    print("Steganography Encoder initialized")

"""
Image Generator Module
Developer: Sohan

Generates visually distinct images based on pattern identifiers.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import hashlib
import random


class ImageGenerator:
    """Generates unique, visually distinct images from pattern identifiers."""
    
    def __init__(self, image_size=(512, 512), mode='RGB'):
        """
        Initialize the image generator.
        
        Args:
            image_size: Tuple of (width, height) for generated images
            mode: Image mode ('RGB', 'RGBA', etc.)
        """
        self.image_size = image_size
        self.mode = mode
        
    def generate_image(self, pattern_id):
        """
        Generate a unique image based on pattern identifier.
        
        Args:
            pattern_id: Pattern identifier to base image on
            
        Returns:
            PIL.Image: Generated image
        """
        # Use pattern_id as seed for reproducible generation
        seed = self._pattern_to_seed(pattern_id)
        random.seed(seed)
        np.random.seed(seed % (2**32))
        
        # Generate image using geometric patterns
        image = self._generate_geometric_pattern(pattern_id)
        
        return image
    
    def _pattern_to_seed(self, pattern_id):
        """
        Convert pattern ID to numeric seed.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            int: Numeric seed
        """
        hash_obj = hashlib.md5(pattern_id.encode())
        return int(hash_obj.hexdigest(), 16) % (2**32)
    
    def _generate_geometric_pattern(self, pattern_id):
        """
        Generate image with geometric patterns.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            PIL.Image: Generated image
        """
        # Create base image
        image = Image.new(self.mode, self.image_size, color='white')
        draw = ImageDraw.Draw(image)
        
        # Extract hash for color generation
        hash_part = pattern_id.split('-')[1] if '-' in pattern_id else pattern_id
        
        # Generate background gradient
        self._draw_gradient_background(image, hash_part)
        
        # Generate geometric shapes
        num_shapes = random.randint(5, 15)
        for i in range(num_shapes):
            self._draw_random_shape(draw, hash_part, i)
        
        # Add pattern ID watermark (subtle)
        self._add_watermark(draw, pattern_id)
        
        return image
    
    def _draw_gradient_background(self, image, hash_part):
        """
        Draw gradient background based on hash.
        
        Args:
            image: PIL Image to draw on
            hash_part: Hash component of pattern ID
        """
        width, height = self.image_size
        pixels = image.load()
        
        # Generate colors from hash
        color1 = self._hash_to_color(hash_part[:6])
        color2 = self._hash_to_color(hash_part[6:12])
        
        # Create gradient
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
    
    def _draw_random_shape(self, draw, hash_part, index):
        """
        Draw random geometric shape.
        
        Args:
            draw: ImageDraw object
            hash_part: Hash component
            index: Shape index
        """
        width, height = self.image_size
        
        # Generate shape parameters from hash
        shape_seed = int(hash_part[index % len(hash_part)], 16)
        shape_type = shape_seed % 4  # 4 types of shapes
        
        # Random position and size
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(20, 100)
        
        # Random color from hash
        color_hash = hash_part[index % len(hash_part):(index + 6) % len(hash_part)]
        color = self._hash_to_color(color_hash.ljust(6, '0'))
        
        # Draw shape
        if shape_type == 0:  # Circle
            draw.ellipse([x, y, x + size, y + size], fill=color, outline=None)
        elif shape_type == 1:  # Rectangle
            draw.rectangle([x, y, x + size, y + size], fill=color, outline=None)
        elif shape_type == 2:  # Triangle
            points = [(x, y + size), (x + size//2, y), (x + size, y + size)]
            draw.polygon(points, fill=color, outline=None)
        else:  # Line
            draw.line([x, y, x + size, y + size], fill=color, width=3)
    
    def _hash_to_color(self, hash_str):
        """
        Convert hash string to RGB color.
        
        Args:
            hash_str: Hex hash string
            
        Returns:
            tuple: RGB color tuple
        """
        # Pad if necessary
        hash_str = hash_str.ljust(6, '0')[:6]
        
        try:
            r = int(hash_str[0:2], 16)
            g = int(hash_str[2:4], 16)
            b = int(hash_str[4:6], 16)
            return (r, g, b)
        except:
            return (128, 128, 128)  # Default gray
    
    def _add_watermark(self, draw, pattern_id):
        """
        Add subtle watermark with pattern ID.
        
        Args:
            draw: ImageDraw object
            pattern_id: Pattern identifier
        """
        # Add small text at bottom
        text = f"ID: {pattern_id}"
        position = (10, self.image_size[1] - 20)
        
        try:
            # Try to use default font
            draw.text(position, text, fill=(200, 200, 200, 128))
        except:
            # Fallback without font
            draw.text(position, text, fill=(200, 200, 200))
    
    def generate_noise_image(self, pattern_id):
        """
        Generate image using noise pattern (alternative method).
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            PIL.Image: Generated noise-based image
        """
        seed = self._pattern_to_seed(pattern_id)
        np.random.seed(seed % (2**32))
        
        # Generate random noise
        noise = np.random.randint(0, 256, (*self.image_size, 3), dtype=np.uint8)
        
        # Apply smoothing for better visual quality
        from scipy import ndimage
        noise = ndimage.gaussian_filter(noise, sigma=5)
        
        image = Image.fromarray(noise.astype('uint8'), self.mode)
        return image
    
    def save_image(self, image, filename):
        """
        Save generated image to file.
        
        Args:
            image: PIL Image
            filename: Output filename
        """
        image.save(filename)
        print(f"Image saved: {filename}")


if __name__ == "__main__":
    from pattern_generator import PatternGenerator
    
    print("=== Image Generator Test ===\n")
    
    # Initialize generators
    pattern_gen = PatternGenerator()
    image_gen = ImageGenerator()
    
    # Generate pattern ID
    pattern_id = pattern_gen.generate_pattern_id()
    print(f"Pattern ID: {pattern_id}")
    
    # Generate image
    print("Generating image...")
    image = image_gen.generate_image(pattern_id)
    
    # Save image
    output_file = f"test_image_{pattern_id.replace(':', '-')}.png"
    image_gen.save_image(image, output_file)
    
    print(f"\nImage size: {image.size}")
    print(f"Image mode: {image.mode}")
    print("\nTest completed successfully!")

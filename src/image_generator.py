"""
Image Generator Module
Developer: Sohan

Generates visually distinct images based on pattern identifiers.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import hashlib


class ImageGenerator:
    """Generates unique images based on pattern identifiers."""
    
    def __init__(self, width=512, height=512):
        """
        Initialize the image generator.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.width = width
        self.height = height
        
    def generate_image(self, pattern_id):
        """
        Generate a unique image based on pattern ID.
        
        Args:
            pattern_id: Unique pattern identifier
            
        Returns:
            PIL.Image: Generated image
        """
        # Create base pattern from pattern_id
        base_pattern = self.create_base_pattern(pattern_id)
        
        # Convert to PIL Image
        image = Image.fromarray(base_pattern.astype('uint8'), 'RGB')
        
        # Add visual elements for distinctiveness
        image = self.add_visual_elements(image, pattern_id)
        
        return image
    
    def create_base_pattern(self, pattern_id):
        """
        Create base visual pattern from pattern ID.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            numpy.ndarray: Base pattern array
        """
        # Use pattern_id as seed for random generation
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(seed)
        
        # Generate gradient background
        pattern = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create color scheme from pattern_id hash
        hash_bytes = hashlib.sha256(pattern_id.encode()).digest()
        color1 = [hash_bytes[0], hash_bytes[1], hash_bytes[2]]
        color2 = [hash_bytes[3], hash_bytes[4], hash_bytes[5]]
        
        # Create gradient
        for y in range(self.height):
            ratio = y / self.height
            for x in range(self.width):
                pattern[y, x] = [
                    int(color1[0] * (1 - ratio) + color2[0] * ratio),
                    int(color1[1] * (1 - ratio) + color2[1] * ratio),
                    int(color1[2] * (1 - ratio) + color2[2] * ratio)
                ]
        
        # Add noise for uniqueness
        noise = np.random.randint(-20, 20, (self.height, self.width, 3))
        pattern = np.clip(pattern + noise, 0, 255)
        
        return pattern
    
    def add_visual_elements(self, image, pattern_id):
        """
        Add visual elements for distinctiveness.
        
        Args:
            image: PIL Image
            pattern_id: Pattern identifier
            
        Returns:
            PIL.Image: Enhanced image
        """
        draw = ImageDraw.Draw(image)
        
        # Use pattern_id to determine circle positions
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(seed)
        
        # Draw random circles
        num_circles = 5 + (seed % 10)
        for _ in range(num_circles):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            radius = np.random.randint(20, 80)
            
            # Generate color from pattern_id
            color_seed = hashlib.sha256(f"{pattern_id}-{x}-{y}".encode()).digest()
            color = (color_seed[0], color_seed[1], color_seed[2], 128)
            
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=color, outline=None)
        
        return image
    
    def ensure_visual_distinctiveness(self, image):
        """
        Ensure generated image is visually distinct.
        
        Args:
            image: Generated image
            
        Returns:
            bool: True if image meets distinctiveness criteria
        """
        # Convert to numpy array
        img_array = np.array(image)
        
        # Check variance (distinct images should have good variance)
        variance = np.var(img_array)
        
        # Check if variance is above threshold
        return variance > 100


if __name__ == "__main__":
    # Test the image generator
    generator = ImageGenerator()
    print("Image Generator initialized")
    
    # Test generation
    test_pattern = "PATTERN-TEST12345678"
    image = generator.generate_image(test_pattern)
    print(f"Generated image size: {image.size}")
    print(f"Visually distinct: {generator.ensure_visual_distinctiveness(image)}")

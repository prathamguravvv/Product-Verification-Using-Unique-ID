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
        
        # Generate random background
        pattern = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create color scheme from pattern_id hash
        hash_bytes = hashlib.sha256(pattern_id.encode()).digest()
        color1 = [hash_bytes[0], hash_bytes[1], hash_bytes[2]]
        color2 = [hash_bytes[3], hash_bytes[4], hash_bytes[5]]
        color3 = [hash_bytes[6], hash_bytes[7], hash_bytes[8]]
        
        # Choose random pattern type based on seed
        pattern_type = seed % 6
        
        if pattern_type == 0:
            # Vertical gradient
            for y in range(self.height):
                ratio = y / self.height
                pattern[y, :] = [
                    int(color1[0] * (1 - ratio) + color2[0] * ratio),
                    int(color1[1] * (1 - ratio) + color2[1] * ratio),
                    int(color1[2] * (1 - ratio) + color2[2] * ratio)
                ]
        elif pattern_type == 1:
            # Horizontal gradient
            for x in range(self.width):
                ratio = x / self.width
                pattern[:, x] = [
                    int(color1[0] * (1 - ratio) + color2[0] * ratio),
                    int(color1[1] * (1 - ratio) + color2[1] * ratio),
                    int(color1[2] * (1 - ratio) + color2[2] * ratio)
                ]
        elif pattern_type == 2:
            # Diagonal gradient
            for y in range(self.height):
                for x in range(self.width):
                    ratio = (x + y) / (self.width + self.height)
                    pattern[y, x] = [
                        int(color1[0] * (1 - ratio) + color2[0] * ratio),
                        int(color1[1] * (1 - ratio) + color2[1] * ratio),
                        int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    ]
        elif pattern_type == 3:
            # Radial gradient
            center_x, center_y = self.width // 2, self.height // 2
            max_dist = np.sqrt(center_x**2 + center_y**2)
            for y in range(self.height):
                for x in range(self.width):
                    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(dist / max_dist, 1.0)
                    pattern[y, x] = [
                        int(color1[0] * (1 - ratio) + color2[0] * ratio),
                        int(color1[1] * (1 - ratio) + color2[1] * ratio),
                        int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    ]
        elif pattern_type == 4:
            # Checkerboard pattern
            block_size = 32 + (seed % 64)
            for y in range(self.height):
                for x in range(self.width):
                    if ((x // block_size) + (y // block_size)) % 2 == 0:
                        pattern[y, x] = color1
                    else:
                        pattern[y, x] = color2
        else:
            # Wave pattern
            frequency = 0.01 + (seed % 100) * 0.0001
            for y in range(self.height):
                for x in range(self.width):
                    wave = (np.sin(x * frequency) + np.sin(y * frequency)) / 2
                    ratio = (wave + 1) / 2
                    pattern[y, x] = [
                        int(color1[0] * (1 - ratio) + color2[0] * ratio),
                        int(color1[1] * (1 - ratio) + color2[1] * ratio),
                        int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    ]
        
        # Add noise for uniqueness
        noise = np.random.randint(-30, 30, (self.height, self.width, 3))
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
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # Use pattern_id to determine shape positions
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(seed)
        
        # Random number of shapes
        num_shapes = 3 + (seed % 8)
        
        for i in range(num_shapes):
            # Random position
            x = np.random.randint(50, self.width - 50)
            y = np.random.randint(50, self.height - 50)
            size = np.random.randint(30, 100)
            
            # Generate color from pattern_id
            color_seed = hashlib.sha256(f"{pattern_id}-{i}".encode()).digest()
            color = (color_seed[0], color_seed[1], color_seed[2], 150)
            
            # Choose random shape type
            shape_type = (seed + i) % 6
            
            if shape_type == 0:
                # Circle
                draw.ellipse([x-size, y-size, x+size, y+size], 
                           fill=color, outline=None)
            elif shape_type == 1:
                # Rectangle
                draw.rectangle([x-size, y-size, x+size, y+size],
                             fill=color, outline=None)
            elif shape_type == 2:
                # Triangle
                points = [
                    (x, y - size),
                    (x - size, y + size),
                    (x + size, y + size)
                ]
                draw.polygon(points, fill=color, outline=None)
            elif shape_type == 3:
                # Diamond
                points = [
                    (x, y - size),
                    (x + size, y),
                    (x, y + size),
                    (x - size, y)
                ]
                draw.polygon(points, fill=color, outline=None)
            elif shape_type == 4:
                # Pentagon
                angles = np.linspace(0, 2*np.pi, 6)
                points = [(x + size * np.cos(a), y + size * np.sin(a)) for a in angles]
                draw.polygon(points, fill=color, outline=None)
            else:
                # Star
                outer_radius = size
                inner_radius = size // 2
                points = []
                for j in range(10):
                    angle = j * np.pi / 5 - np.pi / 2
                    radius = outer_radius if j % 2 == 0 else inner_radius
                    points.append((
                        x + radius * np.cos(angle),
                        y + radius * np.sin(angle)
                    ))
                draw.polygon(points, fill=color, outline=None)
        
        # Add random lines
        num_lines = 2 + (seed % 5)
        for i in range(num_lines):
            x1 = np.random.randint(0, self.width)
            y1 = np.random.randint(0, self.height)
            x2 = np.random.randint(0, self.width)
            y2 = np.random.randint(0, self.height)
            
            color_seed = hashlib.sha256(f"{pattern_id}-line-{i}".encode()).digest()
            color = (color_seed[0], color_seed[1], color_seed[2], 100)
            width = 2 + (seed % 8)
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
        
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

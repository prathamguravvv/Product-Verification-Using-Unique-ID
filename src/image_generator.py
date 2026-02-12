"""
Image Generator Module
Developer: Sohan

Generates visually distinct images based on pattern identifiers.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import hashlib
import random


class ImageGenerator:
    """Generates unique images based on pattern identifiers."""
    
    def __init__(self, width=512, height=512, style="animal"):
        """
        Initialize the image generator.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            style: Generation style ("abstract", "animal", "geometric")
        """
        self.width = width
        self.height = height
        self.style = style
        
        # Animal emoji/shapes for simple generation
        self.animals = [
            "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
            "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
            "🐧", "🐦", "🐤", "🦆", "🦅", "🦉", "🦇", "🐺",
            "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞",
            "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐",
            "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋",
            "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🐘",
            "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🦬", "🐃"
        ]
        
    def generate_image(self, pattern_id):
        """
        Generate a unique image based on pattern ID.
        
        Args:
            pattern_id: Unique pattern identifier
            
        Returns:
            PIL.Image: Generated image
        """
        if self.style == "animal":
            return self.generate_animal_image(pattern_id)
        else:
            return self.generate_abstract_image(pattern_id)
    
    def generate_animal_image(self, pattern_id):
        """
        Generate animal-themed image.
        
        Args:
            pattern_id: Pattern identifier
            
        Returns:
            PIL.Image: Animal-themed image
        """
        # Use pattern_id as seed
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)
        np.random.seed(seed)
        
        # Create colorful background
        image = self.create_gradient_background(pattern_id)
        draw = ImageDraw.Draw(image, 'RGBA')
        
        # Select animal based on pattern_id
        animal_index = seed % len(self.animals)
        selected_animal = self.animals[animal_index]
        
        # Create animal silhouette/shape
        self.draw_animal_shape(draw, pattern_id, animal_index)
        
        # Add decorative elements
        self.add_decorative_elements(draw, pattern_id)
        
        # Add text label
        try:
            # Try to use emoji
            font_size = 120
            # Draw large emoji-style representation
            text_bbox = draw.textbbox((0, 0), selected_animal, font=None)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
            
            # Add shadow for depth
            draw.text((x+5, y+5), selected_animal, fill=(0, 0, 0, 100))
            draw.text((x, y), selected_animal, fill=(255, 255, 255, 255))
        except:
            # Fallback to text
            animal_names = ["Dog", "Cat", "Mouse", "Rabbit", "Fox", "Bear", "Panda", 
                          "Tiger", "Lion", "Cow", "Pig", "Frog", "Monkey", "Bird"]
            animal_name = animal_names[animal_index % len(animal_names)]
            
            # Draw text
            text_bbox = draw.textbbox((0, 0), animal_name)
            text_width = text_bbox[2] - text_bbox[0]
            x = (self.width - text_width) // 2
            y = self.height // 2
            
            draw.text((x+3, y+3), animal_name, fill=(0, 0, 0, 150))
            draw.text((x, y), animal_name, fill=(255, 255, 255, 255))
        
        # Apply slight blur for artistic effect
        image = image.filter(ImageFilter.SMOOTH)
        
        return image
    
    def draw_animal_shape(self, draw, pattern_id, animal_index):
        """Draw animal-inspired shapes."""
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)
        
        # Get colors from pattern_id
        hash_bytes = hashlib.sha256(pattern_id.encode()).digest()
        color = (hash_bytes[0], hash_bytes[1], hash_bytes[2], 180)
        
        # Draw animal-inspired geometric shapes
        center_x, center_y = self.width // 2, self.height // 2
        
        # Body (large circle/ellipse)
        body_size = random.randint(80, 150)
        draw.ellipse([
            center_x - body_size, center_y - body_size,
            center_x + body_size, center_y + body_size
        ], fill=color, outline=(255, 255, 255, 200), width=3)
        
        # Head (smaller circle)
        head_size = body_size // 2
        head_y = center_y - body_size - head_size // 2
        draw.ellipse([
            center_x - head_size, head_y - head_size,
            center_x + head_size, head_y + head_size
        ], fill=color, outline=(255, 255, 255, 200), width=3)
        
        # Ears/features
        ear_size = head_size // 3
        # Left ear
        draw.ellipse([
            center_x - head_size - ear_size, head_y - head_size,
            center_x - head_size + ear_size, head_y - head_size + ear_size * 2
        ], fill=color, outline=(255, 255, 255, 200), width=2)
        # Right ear
        draw.ellipse([
            center_x + head_size - ear_size, head_y - head_size,
            center_x + head_size + ear_size, head_y - head_size + ear_size * 2
        ], fill=color, outline=(255, 255, 255, 200), width=2)
    
    def create_gradient_background(self, pattern_id):
        """Create colorful gradient background."""
        hash_bytes = hashlib.sha256(pattern_id.encode()).digest()
        color1 = [hash_bytes[0], hash_bytes[1], hash_bytes[2]]
        color2 = [hash_bytes[3], hash_bytes[4], hash_bytes[5]]
        
        # Create gradient
        pattern = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for y in range(self.height):
            ratio = y / self.height
            for x in range(self.width):
                pattern[y, x] = [
                    int(color1[0] * (1 - ratio) + color2[0] * ratio),
                    int(color1[1] * (1 - ratio) + color2[1] * ratio),
                    int(color1[2] * (1 - ratio) + color2[2] * ratio)
                ]
        
        return Image.fromarray(pattern, 'RGB')
    
    def add_decorative_elements(self, draw, pattern_id):
        """Add decorative elements around the animal."""
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)
        
        # Add stars/sparkles
        num_stars = random.randint(5, 15)
        for _ in range(num_stars):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(3, 8)
            
            # Draw star shape
            points = []
            for i in range(5):
                angle = i * 144 * 3.14159 / 180
                px = x + size * np.cos(angle)
                py = y + size * np.sin(angle)
                points.append((px, py))
            
            draw.polygon(points, fill=(255, 255, 255, 150))
    
    def generate_abstract_image(self, pattern_id):
        """Generate abstract pattern (original method)."""
        base_pattern = self.create_base_pattern(pattern_id)
        image = Image.fromarray(base_pattern.astype('uint8'), 'RGB')
        image = self.add_visual_elements(image, pattern_id)
        return image
        
    def create_base_pattern(self, pattern_id):
        """Create base visual pattern from pattern ID."""
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(seed)
        
        pattern = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        hash_bytes = hashlib.sha256(pattern_id.encode()).digest()
        color1 = [hash_bytes[0], hash_bytes[1], hash_bytes[2]]
        color2 = [hash_bytes[3], hash_bytes[4], hash_bytes[5]]
        
        for y in range(self.height):
            ratio = y / self.height
            for x in range(self.width):
                pattern[y, x] = [
                    int(color1[0] * (1 - ratio) + color2[0] * ratio),
                    int(color1[1] * (1 - ratio) + color2[1] * ratio),
                    int(color1[2] * (1 - ratio) + color2[2] * ratio)
                ]
        
        noise = np.random.randint(-20, 20, (self.height, self.width, 3))
        pattern = np.clip(pattern + noise, 0, 255)
        
        return pattern
    
    def add_visual_elements(self, image, pattern_id):
        """Add visual elements for distinctiveness."""
        draw = ImageDraw.Draw(image)
        seed = int(hashlib.md5(pattern_id.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(seed)
        
        num_circles = 5 + (seed % 10)
        for _ in range(num_circles):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            radius = np.random.randint(20, 80)
            
            color_seed = hashlib.sha256(f"{pattern_id}-{x}-{y}".encode()).digest()
            color = (color_seed[0], color_seed[1], color_seed[2], 128)
            
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=color, outline=None)
        
        return image
    
    def ensure_visual_distinctiveness(self, image):
        """Ensure generated image is visually distinct."""
        img_array = np.array(image)
        variance = np.var(img_array)
        return variance > 100


if __name__ == "__main__":
    # Test the image generator
    print("Testing Image Generator with Animal Style...")
    
    generator = ImageGenerator(style="animal")
    
    # Generate test images
    for i in range(3):
        test_pattern = f"PATTERN-TEST{i:08d}"
        image = generator.generate_image(test_pattern)
        filename = f"test_animal_{i+1}.png"
        image.save(filename)
        print(f"Generated: {filename} with pattern {test_pattern}")
    
    print("\nDone! Check the generated images.")

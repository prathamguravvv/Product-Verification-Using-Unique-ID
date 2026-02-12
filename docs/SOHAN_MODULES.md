# Sohan's Modules Documentation

## Overview
This document covers the Pattern Generator and Image Generator modules developed by Sohan.

## Modules

### 1. Pattern Generator (`src/pattern_generator.py`)

Generates unique, cryptographically secure pattern identifiers.

#### Features
- Cryptographic hash-based ID generation
- Uniqueness guarantee through collision detection
- Deterministic generation support
- Batch generation capability
- Pattern validation

#### Pattern ID Format
```
PREFIX-HASH-TIMESTAMP
Example: IMG-768F27C5189B6CF4-28417
```

- **PREFIX**: Customizable identifier (default: "IMG")
- **HASH**: 16-character hexadecimal hash (SHA-256 based)
- **TIMESTAMP**: 6-digit timestamp for additional uniqueness

#### Usage

```python
from src.pattern_generator import PatternGenerator

# Initialize
generator = PatternGenerator(prefix="IMG")

# Generate single ID
pattern_id = generator.generate_pattern_id()
print(pattern_id)  # IMG-768F27C5189B6CF4-28417

# Validate ID
is_valid = generator.validate_pattern_id(pattern_id)
print(is_valid)  # True

# Extract hash
hash_part = generator.get_hash_from_pattern(pattern_id)
print(hash_part)  # 768F27C5189B6CF4

# Generate batch
batch = generator.generate_batch(10)
print(len(batch))  # 10 unique IDs

# Deterministic generation
det_id = generator.generate_deterministic_id("my-seed")
print(det_id)  # Same hash for same seed
```

#### API Reference

##### `PatternGenerator(prefix="IMG")`
Initialize the pattern generator.

**Parameters:**
- `prefix` (str): Prefix for pattern IDs

##### `generate_pattern_id(seed=None)`
Generate a unique pattern identifier.

**Parameters:**
- `seed` (str, optional): Seed for generation

**Returns:**
- `str`: Unique pattern identifier

##### `generate_batch(count=10)`
Generate multiple unique pattern IDs.

**Parameters:**
- `count` (int): Number of IDs to generate

**Returns:**
- `list`: List of unique pattern identifiers

##### `validate_pattern_id(pattern_id)`
Validate pattern ID format.

**Parameters:**
- `pattern_id` (str): Pattern ID to validate

**Returns:**
- `bool`: True if valid format

##### `get_hash_from_pattern(pattern_id)`
Extract hash component from pattern ID.

**Parameters:**
- `pattern_id` (str): Pattern identifier

**Returns:**
- `str`: Hash component or None if invalid

##### `generate_deterministic_id(seed_string)`
Generate deterministic pattern ID from seed.

**Parameters:**
- `seed_string` (str): Seed string for generation

**Returns:**
- `str`: Deterministic pattern identifier

---

### 2. Image Generator (`src/image_generator.py`)

Generates visually distinct images based on pattern identifiers.

#### Features
- Deterministic image generation from pattern IDs
- Geometric pattern-based visuals
- Gradient backgrounds
- Customizable image size and mode
- Watermark support

#### Usage

```python
from src.image_generator import ImageGenerator
from src.pattern_generator import PatternGenerator

# Initialize
pattern_gen = PatternGenerator()
image_gen = ImageGenerator(image_size=(512, 512))

# Generate pattern ID
pattern_id = pattern_gen.generate_pattern_id()

# Generate image
image = image_gen.generate_image(pattern_id)

# Save image
image_gen.save_image(image, "output.png")
```

#### API Reference

##### `ImageGenerator(image_size=(512, 512), mode='RGB')`
Initialize the image generator.

**Parameters:**
- `image_size` (tuple): Tuple of (width, height)
- `mode` (str): Image mode ('RGB', 'RGBA', etc.)

##### `generate_image(pattern_id)`
Generate a unique image based on pattern identifier.

**Parameters:**
- `pattern_id` (str): Pattern identifier

**Returns:**
- `PIL.Image`: Generated image

##### `save_image(image, filename)`
Save generated image to file.

**Parameters:**
- `image` (PIL.Image): Image to save
- `filename` (str): Output filename

---

## Integration with Other Modules

### With Steganography (Pratham's Module)

```python
from src.pattern_generator import PatternGenerator
from src.image_generator import ImageGenerator
from src.steganography import SteganographyEncoder

# Generate pattern and image
pattern_gen = PatternGenerator()
image_gen = ImageGenerator()
steg_encoder = SteganographyEncoder()

pattern_id = pattern_gen.generate_pattern_id()
image = image_gen.generate_image(pattern_id)

# Embed pattern ID into image
embedded_image = steg_encoder.embed_identity(image, pattern_id)
```

### With Crypto Verification (Vighnesh's Module)

```python
from src.pattern_generator import PatternGenerator
from src.crypto_verifier import CryptoVerifier

# Generate and verify
pattern_gen = PatternGenerator()
crypto = CryptoVerifier()

pattern_id = pattern_gen.generate_pattern_id()
hash_part = pattern_gen.get_hash_from_pattern(pattern_id)

# Verify hash integrity
is_valid = crypto.verify_hash(hash_part)
```

---

## Testing

Run tests for pattern generator:

```bash
pytest tests/test_pattern_generator.py -v
```

Run demo:

```bash
python examples/sohan_demo.py
```

---

## Performance

- **Pattern Generation**: O(1) - Constant time
- **Uniqueness Check**: O(1) - Hash set lookup
- **Image Generation**: O(n) - Linear with pixel count
- **Batch Generation**: O(k) - Linear with batch size

---

## Security Considerations

1. **Cryptographic Hashing**: Uses SHA-256 for secure hash generation
2. **Collision Resistance**: Tracks generated IDs to prevent duplicates
3. **Deterministic Safety**: Same seed produces same hash (useful for verification)
4. **Timestamp Entropy**: Additional uniqueness through timestamp

---

## Limitations

1. **Image Quality**: Generated images are geometric patterns, not photorealistic
2. **Storage**: Tracks all generated IDs in memory (consider persistence for large-scale)
3. **Seed Sensitivity**: Deterministic generation requires exact seed match

---

## Future Enhancements

1. Add support for advanced generative models (Stable Diffusion, DALL-E)
2. Implement persistent ID tracking (database/file)
3. Add more visual pattern types
4. Support for custom color schemes
5. Integration with blockchain for decentralized verification

---

## Dependencies

```
numpy>=1.21.0
Pillow>=9.0.0
hashlib (built-in)
uuid (built-in)
```

---

## Contact

Developer: Sohan
Module: Pattern Generation & Image Generation
Status: ✓ Complete and Tested

For questions or issues, please refer to the main project documentation.

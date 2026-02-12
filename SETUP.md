# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Demo

```bash
python demo.py
```

This will:
- Generate identifiable images
- Embed pattern IDs using steganography
- Extract and verify identities
- Demonstrate batch processing

### 3. Check Output

Generated images will be in the `demo_output/` directory.

## Usage Examples

### Generate Single Image

```python
from src.main import ImageIdentityFramework

# Initialize
framework = ImageIdentityFramework()

# Generate image with embedded identity
image, pattern_id, hash_value = framework.generate_identifiable_image("output.png")

print(f"Pattern ID: {pattern_id}")
print(f"Hash: {hash_value}")
```

### Verify Image

```python
# Verify an image
result = framework.verify_image("output.png")

print(f"Pattern ID: {result['pattern_id']}")
print(f"Valid: {result['is_valid']}")
print(f"Tampered: {result['tampered']}")
```

### Batch Generation

```python
# Generate multiple images
results = framework.batch_generate(count=10, output_dir="batch_output")

for item in results:
    print(f"{item['path']}: {item['pattern_id']}")
```

## Module Testing

### Test Individual Modules

```python
# Test Pattern Generator
from src.pattern_generator import PatternGenerator
gen = PatternGenerator()
pattern_id = gen.generate_pattern_id()
print(pattern_id)

# Test Image Generator
from src.image_generator import ImageGenerator
img_gen = ImageGenerator()
image = img_gen.generate_image(pattern_id)
image.save("test.png")

# Test Steganography
from src.steganography import SteganographyEncoder
from src.identity_extractor import IdentityExtractor

encoder = SteganographyEncoder()
extractor = IdentityExtractor()

# Embed and extract
embedded = encoder.embed_identity(image, pattern_id)
extracted = extractor.extract_identity(embedded)
print(f"Match: {extracted == pattern_id}")
```

## Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the project root:

```bash
cd Product-Verification-Using-Unique-ID
python demo.py
```

### PIL/Pillow Issues

```bash
pip install --upgrade Pillow
```

### NumPy Issues

```bash
pip install --upgrade numpy
```

## Project Structure

```
.
├── src/
│   ├── pattern_generator.py    # Pattern ID generation
│   ├── image_generator.py      # Image generation
│   ├── steganography.py        # Embedding (Pratham)
│   ├── identity_extractor.py   # Extraction (Pratham)
│   ├── crypto_verifier.py      # Verification
│   └── main.py                 # Main pipeline
├── tests/
│   └── test_steganography.py   # Tests
├── demo.py                     # Demo script
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## Next Steps

1. Run the demo: `python demo.py`
2. Check generated images in `demo_output/`
3. Modify parameters in demo.py
4. Explore individual modules
5. Add your own features!

## Support

For issues or questions, open an issue on GitHub.

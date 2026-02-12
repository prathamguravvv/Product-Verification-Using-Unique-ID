# Contributing Guidelines

## Team Members

- **Sohan**: Pattern Generation & Image Generation
- **Pratham**: Steganography & Identity Extraction
- **Vighnesh**: Cryptographic Verification & Security
- **Ronit**: API, CLI & Integration

## Development Workflow

### 1. Branch Strategy

```bash
# Create feature branch
git checkout -b feature/your-name-module-name

# Example:
git checkout -b feature/pratham-steganography
```

### 2. Development Process

1. Work on your assigned module
2. Write unit tests for your code
3. Ensure code passes all tests
4. Update documentation
5. Commit with clear messages

### 3. Commit Messages

Use clear, descriptive commit messages:

```
feat: Add LSB steganography implementation
fix: Resolve hash calculation bug
docs: Update API documentation
test: Add tests for pattern generator
```

### 4. Code Review

1. Push your branch to GitHub
2. Create Pull Request
3. Request review from team members
4. Address feedback
5. Merge after approval

### 5. Testing

Run tests before committing:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_steganography.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### 6. Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to all functions
- Keep functions focused and small
- Comment complex logic

### 7. Documentation

- Update README.md for major changes
- Add docstrings to all classes and methods
- Include usage examples
- Document API endpoints

## Module Dependencies

```
Pattern Generator (Sohan)
    ↓
Image Generator (Sohan)
    ↓
Steganography Encoder (Pratham)
    ↓
Identity Extractor (Pratham)
    ↓
Crypto Verifier (Vighnesh)
    ↓
Main Pipeline (Ronit)
```

## Communication

- Daily standups: Share progress
- Code reviews: Review each other's PRs
- Issues: Use GitHub issues for bugs
- Discussions: Use GitHub discussions for questions

## Getting Help

If stuck on your module:
1. Check documentation
2. Ask team members
3. Create GitHub issue
4. Review similar implementations

## Quality Checklist

Before submitting PR:
- [ ] Code runs without errors
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] No hardcoded values
- [ ] Error handling implemented
- [ ] Comments added for complex logic

## Module Integration

When your module is ready:
1. Ensure it works standalone
2. Test with dependent modules
3. Update main.py integration
4. Run integration tests
5. Update examples

Happy coding! 🚀

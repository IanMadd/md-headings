# Development Guide

## Project Structure

The project is now organized as a proper Python package:

```
md-headings/
├── md_headings/              # Core package modules
│   ├── __init__.py          # Package initialization
│   ├── converter.py         # Heading conversion logic
│   └── extractor.py         # Word extraction logic
├── tests/                   # Test suite
│   ├── run_tests.py        # Test runner
│   ├── test_converter.py   # Converter tests
│   └── test_word_extractor.py  # Extractor tests
├── docs/                    # Documentation
│   ├── README.md            # Converter documentation
│   ├── WORD_EXTRACTOR_README.md  # Extractor documentation
│   └── DEVELOPMENT.md       # This file
├── examples/                # Sample markdown files
├── convert_headings.py      # CLI for heading conversion
├── extract_words.py         # CLI for word extraction
├── setup.py                 # Package installation script
├── README.md                # Main project README
├── proper_nouns.txt         # Example proper nouns list
└── en_words.txt            # English dictionary
```

## Development Workflow

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run individual test
python tests/test_converter.py
python tests/test_word_extractor.py
```

### Using as a Module

```python
from md_headings import MarkdownHeadingsConverter, MarkdownHeadingWordExtractor

# Create converter
converter = MarkdownHeadingsConverter("proper_nouns.txt")
converter.process_directory("docs/", dry_run=True)

# Create extractor  
extractor = MarkdownHeadingWordExtractor("en_words.txt")
words = extractor.process_directory("docs/", verbose=False)
```

### Using CLI Scripts

```bash
# Convert headings
python convert_headings.py docs/ --proper-nouns proper_nouns.txt --dry-run

# Extract words
python extract_words.py docs/ --output technical_terms.txt
```

### Package Installation

For development:
```bash
pip install -e .
```

For production:
```bash
pip install .
```

After installation, you can use the console commands:
```bash
convert-headings docs/ --proper-nouns proper_nouns.txt
extract-words docs/ --output terms.txt
```

## Adding New Features

### Adding Tests

1. Create test file in `tests/` directory with `test_` prefix
2. Import modules from `md_headings` package
3. Use the test runner to verify functionality

### Modifying Core Logic

- **Converter logic**: Edit `md_headings/converter.py`
- **Extractor logic**: Edit `md_headings/extractor.py`
- **CLI interfaces**: Edit `convert_headings.py` or `extract_words.py`

### Documentation

- Update relevant files in `docs/` directory
- Update main `README.md` for user-facing changes
- Update this development guide for structural changes

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Include docstrings for all public methods
- Handle exceptions gracefully with informative error messages
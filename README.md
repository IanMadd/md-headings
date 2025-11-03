# Markdown Headings Tools

A Python package for processing and converting markdown headings with proper noun preservation and technical term extraction.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/IanMadd/md-headings.git
cd md-headings
```

### Usage

#### Convert Headings to Sentence Case

```bash
python convert_headings.py docs/ --proper-nouns proper_nouns.txt
```

#### Extract Non-English Words from Headings

```bash
python extract_words.py docs/ --output technical_terms.txt
```

## Features

- **Smart heading conversion**: Convert ALL CAPS and Title Case to sentence case
- **Proper noun preservation**: Maintain correct capitalization for brand names and technical terms
- **Word extraction**: Identify technical vocabulary not in standard dictionaries
- **Recursive processing**: Handle entire documentation trees
- **Dry-run support**: Preview changes before applying

## 🔧 Core Tools

### 1. `convert_headings.py` - Heading Converter

**Purpose**: Converts uppercase and titlecase headings to proper sentence case

- Converts ALL CAPS and Title Case headings to sentence case
- Preserves proper nouns using a custom list
- Processes all markdown files recursively
- Includes dry-run mode for safe testing
- Handles multi-word proper nouns (e.g., "Node.js", "VS Code")

### 2. `extract_words.py` - Word Extractor

**Purpose**: Finds non-English words in markdown headings

- Extracts words from all headings in markdown files
- Compares against a comprehensive English dictionary (`en_words.txt`)
- Outputs unique non-English words to a text file
- Perfect for identifying proper nouns, technical terms, and specialized vocabulary

## 🔄 Workflow Integration

The scripts work together perfectly:

```bash
# Step 1: Extract technical terms from your documentation
python extract_words.py docs/ --output tech_terms.txt

# Step 2: Review tech_terms.txt and keep only proper nouns/brand names

# Step 3: Convert headings using the curated proper nouns list
python convert_headings.py docs/ --proper-nouns tech_terms.txt --dry-run

# Step 4: Apply changes if satisfied with preview
python convert_headings.py docs/ --proper-nouns tech_terms.txt
```

## Project Structure

```
md-headings/
├── md_headings/              # Core package modules
│   ├── __init__.py          # Package initialization
│   ├── converter.py         # Heading conversion logic
│   └── extractor.py         # Word extraction logic
├── tests/                   # Test suite
│   ├── run_tests.py        # Test runner
│   ├── test_converter.py   # Converter tests (including titlecase)
│   └── test_word_extractor.py  # Extractor tests
├── docs/                    # Documentation
│   ├── README.md            # Converter documentation
│   ├── WORD_EXTRACTOR_README.md  # Extractor documentation
│   └── DEVELOPMENT.md       # Development guide
├── examples/                # Sample markdown files
│   ├── sample1.md
│   └── subdir/sample2.md
├── convert_headings.py      # CLI for heading conversion ⭐
├── extract_words.py         # CLI for word extraction ⭐
├── setup.py                 # Package installation script
├── README.md                # This file
├── proper_nouns.txt         # Example proper nouns list
├── non_english_words.txt    # Generated output from extractor
└── en_words.txt            # English dictionary (235K+ words)
```

## 🚀 Quick Start

### Extract Non-English Words

```bash
python extract_words.py your_docs_folder/
```

### Convert Headings

```bash
python convert_headings.py your_docs_folder/ --proper-nouns proper_nouns.txt
```

## ✨ Key Features

### Word Extractor

- ✅ Recursive directory processing
- ✅ Comprehensive English dictionary (235K+ words)
- ✅ Alphabetical sorting
- ✅ Duplicate removal
- ✅ Individual word analysis mode
- ✅ Custom dictionary support

### Heading Converter

- ✅ Smart sentence case conversion
- ✅ Proper noun preservation
- ✅ Multi-word proper nouns support
- ✅ Titlecase to sentence case conversion
- ✅ Dry-run preview mode
- ✅ Preposition/article handling
- ✅ Abbreviation detection

## 📊 Example Results

### Word Extractor Output

```text
APIs
AWS
Docker
JavaScript
MongoDB
OAuth
PostgreSQL
WebSockets
```

### Heading Conversion

```text
Before: # GETTING STARTED WITH JAVASCRIPT AND APIs ON AWS
After:  # Getting started with JavaScript and APIs on AWS

Before: ## Building Modern Web Applications With React
After:  ## Building modern web applications with React
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python tests/run_tests.py

# Run individual test files
python tests/test_converter.py
python tests/test_word_extractor.py
```

The test suite includes:

- **Titlecase to sentence case conversion** (15 test cases)
- **Edge case handling** (10 test cases)
- **Word extraction accuracy** validation
- **Proper noun preservation** verification

## Documentation

- [Heading Converter Guide](docs/README.md)
- [Word Extractor Guide](docs/WORD_EXTRACTOR_README.md)
- [Development Guide](docs/DEVELOPMENT.md)

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Package Installation

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

## License

MIT License

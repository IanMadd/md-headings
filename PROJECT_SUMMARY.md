# Markdown Heading Tools - Project Summary

This project contains two complementary Python scripts for processing markdown headings:

## 🔧 Scripts Overview

### 1. `extract_heading_words.py` - Word Extractor
**Purpose**: Finds non-English words in markdown headings
- Extracts words from all headings in markdown files
- Compares against a comprehensive English dictionary (`en_words.txt`)
- Outputs unique non-English words to a text file
- Perfect for identifying proper nouns, technical terms, and specialized vocabulary

### 2. `md_headings_converter.py` - Heading Converter  
**Purpose**: Converts uppercase headings to proper sentence case
- Converts ALL CAPS headings to sentence case
- Preserves proper nouns using a custom list
- Processes all markdown files recursively
- Includes dry-run mode for safe testing

## 🔄 Workflow Integration

The scripts work together perfectly:

```bash
# Step 1: Extract technical terms from your documentation
python extract_heading_words.py docs/ --output tech_terms.txt

# Step 2: Review tech_terms.txt and keep only proper nouns/brand names

# Step 3: Convert headings using the curated proper nouns list
python md_headings_converter.py docs/ --proper-nouns tech_terms.txt --dry-run

# Step 4: Apply changes if satisfied with preview
python md_headings_converter.py docs/ --proper-nouns tech_terms.txt
```

## 📁 Project Structure

```
md-headings/
├── extract_heading_words.py      # Word extraction script ⭐
├── md_headings_converter.py      # Heading conversion script ⭐
├── en_words.txt                  # English dictionary (235K+ words)
├── proper_nouns.txt              # Example proper nouns list
├── non_english_words.txt         # Generated output from extractor
├── examples/                     # Test markdown files
│   ├── sample1.md
│   └── subdir/sample2.md
├── README.md                     # Main documentation
├── WORD_EXTRACTOR_README.md      # Word extractor documentation
├── test_converter.py             # Test script for converter
├── test_word_extractor.py        # Test script for extractor
└── usage_examples.py             # Usage examples
```

## 🚀 Quick Start

### Extract Non-English Words
```bash
python extract_heading_words.py your_docs_folder/
```

### Convert Headings  
```bash
python md_headings_converter.py your_docs_folder/ --proper-nouns proper_nouns.txt
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
- ✅ Dry-run preview mode
- ✅ Preposition/article handling
- ✅ Abbreviation detection

## 📊 Example Results

### Word Extractor Output
```
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
```
Before: # GETTING STARTED WITH JAVASCRIPT AND APIs ON AWS
After:  # Getting started with JavaScript and APIs on AWS
```

## 🔧 Dependencies
- Python 3.6+ (uses only standard library)
- No external packages required

Both scripts are production-ready and handle edge cases gracefully!
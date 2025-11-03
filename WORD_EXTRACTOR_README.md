# Markdown Heading Word Extractor

This script extracts words from Markdown headings that are not found in a standard English dictionary. It's useful for identifying:

- **Proper nouns** (Microsoft, JavaScript, PostgreSQL)
- **Technical terms** (OAuth, JWT, WebSockets)
- **Acronyms** (API, CSS, AWS)
- **Brand names** (MongoDB, Docker, Kubernetes)
- **Specialized vocabulary** not in standard dictionaries

## Usage

### Basic Usage

```bash
python extract_heading_words.py /path/to/markdown/directory
```

This will:

1. Process all `.md` and `.markdown` files in the directory and subdirectories
2. Extract words from headings that aren't in `en_words.txt`
3. Save unique words to `non_english_words.txt`

### Advanced Options

```bash
# Specify custom English dictionary file
python extract_heading_words.py /path/to/markdown --english-words custom_dictionary.txt

# Specify custom output file
python extract_heading_words.py /path/to/markdown --output technical_terms.txt

# Analyze specific words
python extract_heading_words.py /path/to/markdown --analyze JavaScript PostgreSQL OAuth
```

### Command Line Options

- `directory`: Path to directory containing Markdown files (required)
- `--english-words`, `-e`: Path to English dictionary file (default: `en_words.txt`)
- `--output`, `-o`: Output file for non-English words (default: `non_english_words.txt`)
- `--analyze`, `-a`: Analyze specific words instead of processing files

## Example Output

Given these headings:

```markdown
# Getting Started with JavaScript and APIs
## Setting up PostgreSQL Databases
### Implementing OAuth Authentication
```

The script would identify these non-English words:

```
APIs
JavaScript
OAuth
PostgreSQL
```

Note: Words like "Getting", "Started", "Setting", etc. are in the English dictionary, so they won't be included.

## Output File Format

The output file contains one word per line, sorted alphabetically (case-insensitive):

```
APIs
AWS
JavaScript
MongoDB
OAuth
PostgreSQL
WebSockets
```

## Use Cases

1. **Creating proper nouns lists** for the heading converter script
2. **Identifying technical terminology** in documentation
3. **Building specialized dictionaries** for spell checkers
4. **Analyzing documentation vocabulary** to ensure consistency
5. **Finding brand names and product names** that need special capitalization

## Integration with Heading Converter

You can use the output of this script as input to the `md_headings_converter.py` script:

```bash
# 1. Extract non-English words from headings
python extract_heading_words.py docs/ --output technical_terms.txt

# 2. Review and edit technical_terms.txt to include only proper nouns

# 3. Use it with the heading converter
python md_headings_converter.py docs/ --proper-nouns technical_terms.txt
```

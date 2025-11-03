
# Markdown Headings Converter

A Python script that converts uppercase headings in Markdown documents to sentence case while preserving proper nouns.

## Features

- **Recursive Processing**: Processes all `.md` and `.markdown` files in a directory and its subdirectories
- **Proper Nouns Preservation**: Maintains correct capitalization for specified proper nouns (e.g., "Microsoft", "macOS", "JavaScript")
- **Smart Sentence Case**: Converts headings to sentence case while preserving abbreviations and proper nouns
- **Dry Run Mode**: Preview changes before applying them
- **Regex-Based**: Uses regular expressions to efficiently find and process Markdown headings

## Installation

No additional dependencies required - uses only Python standard library.

## Usage

### Basic Usage

```bash
python md_headings_converter.py /path/to/markdown/directory
```

### With Proper Nouns File

```bash
python md_headings_converter.py /path/to/markdown/directory --proper-nouns proper_nouns.txt
```

### Dry Run (Preview Changes)

```bash
python md_headings_converter.py /path/to/markdown/directory --proper-nouns proper_nouns.txt --dry-run
```

## Command Line Options

- `directory`: Path to the directory containing Markdown files (required)
- `--proper-nouns`, `-p`: Path to text file containing proper nouns (optional)
- `--dry-run`, `-d`: Show what would be changed without modifying files (optional)

## Proper Nouns File Format

Create a text file with one proper noun per line:

```
Microsoft
macOS
JavaScript
GitHub
API
JSON
```

- Lines starting with `#` are treated as comments and ignored
- Empty lines are ignored
- Each proper noun should be on its own line with the exact capitalization you want preserved

## Examples

### Before Processing

```markdown
# GETTING STARTED WITH PYTHON AND JAVASCRIPT
## SETTING UP YOUR DEVELOPMENT ENVIRONMENT
### INSTALLING VS CODE AND EXTENSIONS
#### CONNECTING TO POSTGRESQL DATABASES
```

### After Processing (with proper nouns file)

```markdown
# Getting started with Python and JavaScript
## Setting up your development environment
### Installing VS Code and extensions
#### Connecting to PostgreSQL databases
```

## How It Works

1. **Find Headings**: Uses regex pattern `^(#{1,6})\s+(.+)$` to match Markdown headings
2. **Analyze Words**: Splits heading text into words while preserving punctuation
3. **Apply Rules**:
   - First word is capitalized
   - Proper nouns maintain their specified capitalization
   - Short uppercase words (≤3 chars) are treated as abbreviations and kept uppercase
   - Other words are converted to lowercase
4. **Preserve Structure**: Maintains original Markdown heading levels and formatting

## Testing

The `examples/` directory contains sample Markdown files you can use to test the script:

```bash
# Test with dry run first
python md_headings_converter.py examples --proper-nouns proper_nouns.txt --dry-run

# Apply changes
python md_headings_converter.py examples --proper-nouns proper_nouns.txt
```

## License

MIT License - feel free to use and modify as needed.

#!/usr/bin/env python3
"""
Test script for code block handling in converter and extractor
"""

import os
import tempfile
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from md_headings.converter import MarkdownHeadingsConverter
from md_headings.extractor import MarkdownHeadingWordExtractor


def test_code_block_handling():
    """Test that converter and extractor ignore comments in code blocks"""
    
    # Test markdown content with code blocks
    test_markdown = """# TEST HEADING WITH CODE BLOCKS

## PYTHON DEVELOPMENT GUIDE

Here's some Python code:

```python
# This comment should be ignored
def hello_world():
    # Another comment to ignore
    return "Hello"  # Inline comment
```

### JAVASCRIPT FUNCTIONS

Indented code block:

    # This should also be ignored
    var x = 10;  // JavaScript comment
    // Another comment to ignore
    console.log(x);

## API ENDPOINTS DOCUMENTATION

More content here.

```bash
# Shell script comments should be ignored
echo "Hello World"  # This comment too
```

### DATABASE SCHEMA OVERVIEW

Final section."""
    
    print("Testing code block handling...")
    print("=" * 50)
    
    # Test converter
    print("1. Testing Converter:")
    print("-" * 30)
    
    # Create temporary markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_markdown)
        temp_file = f.name
    
    try:
        # Create converter
        converter = MarkdownHeadingsConverter()
        
        # Process the file
        modified = converter.process_markdown_file(Path(temp_file))
        
        # Read the result
        with open(temp_file, 'r', encoding='utf-8') as f:
            result = f.read()
        
        print(f"File was modified: {modified}")
        
        # Check that headings were converted
        expected_headings = [
            "# Test heading with code blocks",
            "## Python development guide", 
            "### Javascript functions",  # Note: 'Javascript' not 'JavaScript' - no proper noun
            "## Api endpoints documentation",
            "### Database schema overview"
        ]
        
        all_found = True
        for expected in expected_headings:
            if expected in result:
                print(f"✓ Found: {expected}")
            else:
                print(f"✗ Missing: {expected}")
                all_found = False
        
        # Check that comments in code blocks were preserved
        code_comments = [
            "# This comment should be ignored",
            "# Another comment to ignore", 
            "# This should also be ignored",
            "# Shell script comments should be ignored"
        ]
        
        comments_preserved = True
        for comment in code_comments:
            if comment in result:
                print(f"✓ Preserved code comment: {comment}")
            else:
                print(f"✗ Lost code comment: {comment}")
                comments_preserved = False
        
        converter_passed = all_found and comments_preserved
        print(f"Converter test: {'PASSED' if converter_passed else 'FAILED'}")
        
    finally:
        os.unlink(temp_file)
    
    print("\n2. Testing Extractor:")
    print("-" * 30)
    
    # Test extractor
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_markdown)
        temp_file = f.name
    
    # Create a minimal English words file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("""the
and
with
development
guide
functions
documentation
overview
code
blocks
here
content
final
section
more""")
        dict_file = f.name
    
    try:
        # Create extractor
        extractor = MarkdownHeadingWordExtractor(dict_file)
        
        # Process the file
        words = extractor.process_markdown_file(Path(temp_file), verbose=False)
        
        print(f"Non-English words found: {sorted(words)}")
        
        # Should find words from headings but not from code comments
        expected_words = {'TEST', 'HEADING', 'PYTHON', 'JAVASCRIPT', 'API', 'ENDPOINTS', 'DATABASE', 'SCHEMA'}
        unexpected_words = {'comment', 'should', 'ignored', 'Another', 'ignore', 'Inline', 'Shell', 'script', 'Hello', 'World', 'var', 'console', 'log', 'echo'}
        
        found_expected = expected_words.intersection(words)
        found_unexpected = unexpected_words.intersection(words)
        
        print(f"✓ Found expected words: {sorted(found_expected)}")
        if found_unexpected:
            print(f"✗ Found unexpected words from code: {sorted(found_unexpected)}")
        else:
            print("✓ No unexpected words from code blocks found")
        
        extractor_passed = len(found_expected) > 0 and len(found_unexpected) == 0
        print(f"Extractor test: {'PASSED' if extractor_passed else 'FAILED'}")
        
    finally:
        os.unlink(temp_file)
        os.unlink(dict_file)
    
    # Overall result
    print("\n" + "=" * 50)
    print("OVERALL RESULT")
    print("=" * 50)
    overall_passed = converter_passed and extractor_passed
    print(f"Code block handling: {'PASSED' if overall_passed else 'FAILED'}")
    
    return overall_passed


if __name__ == "__main__":
    test_code_block_handling()
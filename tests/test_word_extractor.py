#!/usr/bin/env python3
"""
Test script for the word extractor
"""

import tempfile
import os
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from md_headings.extractor import MarkdownHeadingWordExtractor

def test_word_extraction():
    """Test the word extractor with sample data"""
    
    # Create a small test dictionary
    test_dict_content = """the
and
with
development
web
mobile
setting
up
your
a
an
to
for
of
in
on
create
build
using"""
    
    # Create temporary dictionary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_dict_content)
        dict_file = f.name
    
    # Test markdown content
    test_markdown = """# BUILDING WEB APPLICATIONS WITH REACT

## SETTING UP NODEJS AND NPM

### CONNECTING TO POSTGRESQL DATABASES

#### IMPLEMENTING JWT AUTHENTICATION

##### DEPLOYING ON AWS INFRASTRUCTURE"""
    
    # Create temporary markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_markdown)
        md_file = f.name
    
    try:
        # Create extractor with test dictionary
        extractor = MarkdownHeadingWordExtractor(dict_file)
        
        # Process the markdown file
        from pathlib import Path
        non_english_words = extractor.process_markdown_file(Path(md_file))
        
        print("Test Results:")
        print("=" * 40)
        print("Non-English words found:")
        for word in sorted(non_english_words, key=str.lower):
            print(f"  {word}")
        
        print(f"\nTotal: {len(non_english_words)} words")
        
        # Expected words that should be flagged:
        expected = {
            'BUILDING', 'APPLICATIONS', 'REACT', 'NODEJS', 'NPM', 
            'CONNECTING', 'POSTGRESQL', 'DATABASES', 'IMPLEMENTING', 
            'JWT', 'AUTHENTICATION', 'DEPLOYING', 'AWS', 'INFRASTRUCTURE'
        }
        
        print(f"\nExpected: {len(expected)} words")
        print("Words correctly identified as non-English:")
        for word in expected:
            if word in non_english_words:
                print(f"  ✓ {word}")
            else:
                print(f"  ✗ {word} (missed)")
    
    finally:
        # Clean up
        os.unlink(dict_file)
        os.unlink(md_file)

if __name__ == "__main__":
    test_word_extraction()
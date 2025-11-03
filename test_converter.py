#!/usr/bin/env python3
"""
Test script for the Markdown Headings Converter
"""

import os
import tempfile
from md_headings_converter import MarkdownHeadingsConverter

def test_converter():
    """Test the converter with sample data"""
    
    # Create temporary proper nouns file
    proper_nouns_content = """Microsoft
JavaScript
API
APIs
VS Code
macOS
iOS"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(proper_nouns_content)
        proper_nouns_file = f.name
    
    # Test markdown content
    test_markdown = """# TESTING THE MARKDOWN CONVERTER

## GETTING STARTED WITH JAVASCRIPT AND APIs

### SETTING UP VS CODE ON MACOS

#### INTEGRATING WITH MICROSOFT SERVICES

##### WORKING WITH IOS APPLICATIONS"""
    
    # Create converter
    converter = MarkdownHeadingsConverter(proper_nouns_file)
    
    # Test each heading
    test_cases = [
        "TESTING THE MARKDOWN CONVERTER",
        "GETTING STARTED WITH JAVASCRIPT AND APIs", 
        "SETTING UP VS CODE ON MACOS",
        "INTEGRATING WITH MICROSOFT SERVICES",
        "WORKING WITH IOS APPLICATIONS"
    ]
    
    print("Testing heading conversions:")
    print("=" * 50)
    
    for heading in test_cases:
        converted = converter.convert_to_sentence_case(heading)
        print(f"Original: {heading}")
        print(f"Converted: {converted}")
        print("-" * 30)
    
    # Clean up
    os.unlink(proper_nouns_file)

if __name__ == "__main__":
    test_converter()
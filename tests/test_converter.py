#!/usr/bin/env python3
"""
Test script for the Markdown Headings Converter
"""

import os
import tempfile
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from md_headings.converter import MarkdownHeadingsConverter

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


def test_titlecase_to_sentence_case():
    """Test conversion from titlecase to sentence case"""
    
    # Create temporary proper nouns file
    proper_nouns_content = """JavaScript
Python
GitHub
API
APIs
CSS
HTML
JSON
React
Vue.js
Node.js
PostgreSQL
MongoDB
Docker
AWS
Microsoft
Google
Apple
iOS
macOS
VS Code
OAuth
JWT
Jest"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(proper_nouns_content)
        proper_nouns_file = f.name
    
    # Create converter
    converter = MarkdownHeadingsConverter(proper_nouns_file)
    
    # Test cases for titlecase to sentence case conversion
    titlecase_test_cases = [
        # Input, Expected Output
        ("Getting Started With JavaScript Development", "Getting started with JavaScript development"),
        ("Building Modern Web Applications With React", "Building modern web applications with React"),
        ("Setting Up Your Development Environment", "Setting up your development environment"),
        ("Understanding JSON And XML Data Formats", "Understanding JSON and XML data formats"),
        ("Deploying Applications To AWS Cloud Services", "Deploying applications to AWS cloud services"),
        ("Working With APIs And Database Connections", "Working with APIs and database connections"),
        ("Creating Responsive Designs With CSS And HTML", "Creating responsive designs with CSS and HTML"),
        ("Implementing Authentication With OAuth", "Implementing authentication with OAuth"),
        ("Using Docker For Container Management", "Using Docker for container management"),
        ("Integrating PostgreSQL With Node.js Applications", "Integrating PostgreSQL with Node.js applications"),
        ("Building Cross-Platform Apps With React Native", "Building cross-platform apps with React native"),
        ("Managing State In Vue.js Components", "Managing state in Vue.js components"),
        ("Optimizing Performance For Mobile Devices", "Optimizing performance for mobile devices"),
        ("Securing APIs With JWT Tokens", "Securing APIs with JWT tokens"),
        ("Testing JavaScript Code With Jest", "Testing JavaScript code with Jest"),
    ]
    
    print("\nTesting titlecase to sentence case conversions:")
    print("=" * 60)
    
    all_passed = True
    
    for i, (input_text, expected_output) in enumerate(titlecase_test_cases, 1):
        converted = converter.convert_to_sentence_case(input_text)
        passed = converted == expected_output
        
        if not passed:
            all_passed = False
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Test {i:2d}: {status}")
        print(f"  Input:    {input_text}")
        print(f"  Expected: {expected_output}")
        print(f"  Got:      {converted}")
        if not passed:
            print(f"  ❌ MISMATCH")
        print("-" * 40)
    
    # Summary
    passed_count = sum(1 for input_text, expected in titlecase_test_cases 
                      if converter.convert_to_sentence_case(input_text) == expected)
    total_count = len(titlecase_test_cases)
    
    print(f"\nTitlecase Test Summary:")
    print(f"Passed: {passed_count}/{total_count}")
    print(f"Success Rate: {(passed_count/total_count)*100:.1f}%")
    
    if all_passed:
        print("🎉 All titlecase tests passed!")
    else:
        print("⚠️  Some titlecase tests failed.")
    
    # Clean up
    os.unlink(proper_nouns_file)
    
    return all_passed


def test_edge_cases():
    """Test edge cases and special scenarios"""
    
    # Create converter without proper nouns
    converter = MarkdownHeadingsConverter()
    
    edge_case_tests = [
        # Input, Expected (basic sentence case without proper nouns)
        ("", ""),  # Empty string
        ("A", "A"),  # Single character
        ("THE QUICK BROWN FOX", "The quick brown fox"),  # All common words
        ("API INTEGRATION", "Api integration"),  # Without proper nouns file
        ("WORKING WITH APIs", "Working with apis"),  # Plural without proper nouns
        ("HTML/CSS DEVELOPMENT", "Html/css development"),  # With punctuation
        ("TWENTY-FIRST CENTURY", "Twenty-first century"),  # Hyphenated words
        ("JOHN'S PROGRAMMING GUIDE", "John's programming guide"),  # Possessive
        ("CHAPTER 1: INTRODUCTION", "Chapter 1: introduction"),  # With numbers and colon
        ("FAQ - FREQUENTLY ASKED QUESTIONS", "Faq - frequently asked questions"),  # With dash
    ]
    
    print("\nTesting edge cases:")
    print("=" * 40)
    
    all_passed = True
    
    for i, (input_text, expected_output) in enumerate(edge_case_tests, 1):
        converted = converter.convert_to_sentence_case(input_text)
        passed = converted == expected_output
        
        if not passed:
            all_passed = False
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Test {i:2d}: {status}")
        print(f"  Input:    '{input_text}'")
        print(f"  Expected: '{expected_output}'")
        print(f"  Got:      '{converted}'")
        if not passed:
            print(f"  ❌ MISMATCH")
        print("-" * 30)
    
    return all_passed


if __name__ == "__main__":
    print("Running all converter tests...")
    print("=" * 50)
    
    # Run original test
    test_converter()
    
    # Run titlecase tests
    titlecase_passed = test_titlecase_to_sentence_case()
    
    # Run edge case tests
    edge_cases_passed = test_edge_cases()
    
    # Overall summary
    print("\n" + "=" * 50)
    print("OVERALL TEST SUMMARY")
    print("=" * 50)
    print(f"Titlecase tests: {'PASSED' if titlecase_passed else 'FAILED'}")
    print(f"Edge case tests: {'PASSED' if edge_cases_passed else 'FAILED'}")
    
    if titlecase_passed and edge_cases_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed.")
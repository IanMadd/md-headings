#!/usr/bin/env python3
"""
Usage examples for the Markdown Headings Converter
"""

def show_usage():
    print("""
Markdown Headings Converter - Usage Examples
============================================

1. Basic usage (process all .md files in a directory):
   python md_headings_converter.py /path/to/markdown/files

2. With proper nouns file:
   python md_headings_converter.py /path/to/markdown/files --proper-nouns proper_nouns.txt

3. Dry run (preview changes without modifying files):
   python md_headings_converter.py /path/to/markdown/files --proper-nouns proper_nouns.txt --dry-run

4. Help:
   python md_headings_converter.py --help

Example proper nouns file content:
---------------------------------
Microsoft
macOS
JavaScript
API
APIs
VS Code
GitHub
Docker
Kubernetes

Example input heading:
---------------------
# GETTING STARTED WITH JAVASCRIPT AND APIs ON MACOS

Example output:
--------------
# Getting started with JavaScript and APIs on macOS

Features:
--------
✓ Processes all .md and .markdown files recursively
✓ Preserves proper nouns with exact capitalization
✓ Converts to proper sentence case
✓ Handles multi-word proper nouns (e.g., "VS Code")
✓ Keeps abbreviations uppercase (≤3 characters)
✓ Dry-run mode for safe testing
✓ Comprehensive error handling

""")

if __name__ == "__main__":
    show_usage()
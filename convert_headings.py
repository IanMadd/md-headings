#!/usr/bin/env python3
"""
Command-line interface for the Markdown Headings Converter
"""

import argparse
from md_headings.converter import MarkdownHeadingsConverter


def main():
    """Main entry point for the converter CLI."""
    parser = argparse.ArgumentParser(
        description="Convert uppercase headings in markdown files to sentence case"
    )
    parser.add_argument(
        'directory',
        help='Directory to process (will process recursively)'
    )
    parser.add_argument(
        '--proper-nouns',
        '-p',
        help='Path to text file containing proper nouns (one per line)'
    )
    parser.add_argument(
        '--dry-run',
        '-d',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    
    args = parser.parse_args()
    
    try:
        # Create converter instance
        converter = MarkdownHeadingsConverter(args.proper_nouns)
        
        # Process directory
        converter.process_directory(args.directory, args.dry_run)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
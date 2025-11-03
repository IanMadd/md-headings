#!/usr/bin/env python3
"""
Command-line interface for the Markdown Heading Word Extractor
"""

import argparse
from md_headings.extractor import MarkdownHeadingWordExtractor


def main():
    """Main entry point for the extractor CLI."""
    parser = argparse.ArgumentParser(
        description="Extract non-English words from markdown headings"
    )
    parser.add_argument(
        'directory',
        help='Directory to process (will process recursively)'
    )
    parser.add_argument(
        '--english-words',
        '-e',
        default='en_words.txt',
        help='Path to English words dictionary file (default: en_words.txt)'
    )
    parser.add_argument(
        '--output',
        '-o',
        default='non_english_words.txt',
        help='Output file for non-English words (default: non_english_words.txt)'
    )
    parser.add_argument(
        '--analyze',
        '-a',
        nargs='+',
        help='Analyze specific words (space-separated)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create extractor instance
        extractor = MarkdownHeadingWordExtractor(args.english_words)
        
        if args.analyze:
            # Analyze specific words
            extractor.analyze_specific_words(args.analyze)
        else:
            # Process directory
            extractor.process_directory(args.directory, args.output)
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
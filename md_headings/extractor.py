"""
Markdown Heading Word Extractor Module

This module provides the MarkdownHeadingWordExtractor class for extracting
non-English words from markdown headings.
"""

import re
from pathlib import Path
from typing import Set, List


class MarkdownHeadingWordExtractor:
    """
    A class for extracting words from markdown headings that are not found
    in a standard English dictionary.
    """
    
    def __init__(self, english_words_file: str = "en_words.txt"):
        """
        Initialize the word extractor.
        
        Args:
            english_words_file: Path to the English words dictionary file
            
        Raises:
            FileNotFoundError: If the English words file doesn't exist
            Exception: For other file reading errors
        """
        self.english_words = set()
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.word_pattern = re.compile(r'\b[a-zA-Z]+\b')  # Match alphabetic words only
        
        self.load_english_words(english_words_file)
    
    def load_english_words(self, filepath: str) -> None:
        """
        Load English words from the dictionary file.
        
        Args:
            filepath: Path to the English words file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: For other file reading errors
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        # Store both lowercase and original case for comparison
                        self.english_words.add(word.lower())
            
            print(f"Loaded {len(self.english_words)} English words from {filepath}")
        
        except FileNotFoundError:
            print(f"Error: English words file '{filepath}' not found.")
            raise
        except Exception as e:
            print(f"Error loading English words file: {e}")
            raise
    
    def extract_words_from_heading(self, heading_text: str) -> Set[str]:
        """
        Extract individual words from a heading text.
        
        Args:
            heading_text: The heading text to extract words from
            
        Returns:
            Set of words found in the heading
        """
        # Find all alphabetic words
        words = self.word_pattern.findall(heading_text)
        
        # Return unique words, preserving original case
        return set(words)
    
    def is_english_word(self, word: str) -> bool:
        """
        Check if a word is in the English dictionary.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is in English dictionary, False otherwise
        """
        return word.lower() in self.english_words
    
    def process_markdown_file(self, filepath: Path, verbose: bool = True) -> Set[str]:
        """
        Process a single markdown file and extract non-English words from headings.
        
        Args:
            filepath: Path to the markdown file
            verbose: Whether to print found words
            
        Returns:
            Set of non-English words found in headings
            
        Raises:
            Exception: For file reading errors
        """
        non_english_words = set()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all headings
            headings = self.heading_pattern.findall(content)
            
            for level, heading_text in headings:
                # Extract words from this heading
                words = self.extract_words_from_heading(heading_text)
                
                # Check each word against English dictionary
                for word in words:
                    if not self.is_english_word(word):
                        non_english_words.add(word)
                        if verbose:
                            print(f"  Found non-English word: '{word}' in heading: {level} {heading_text}")
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
        
        return non_english_words
    
    def process_directory(self, directory: str, output_file: str = "non_english_words.txt", verbose: bool = True) -> Set[str]:
        """
        Process all markdown files in a directory recursively.
        
        Args:
            directory: Path to the directory to process
            output_file: Path to the output file for non-English words
            verbose: Whether to print detailed progress
            
        Returns:
            Set of all non-English words found
        """
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"Error: Directory '{directory}' does not exist.")
            return set()
        
        # Find all markdown files
        markdown_files = list(directory_path.rglob('*.md')) + list(directory_path.rglob('*.markdown'))
        
        if not markdown_files:
            print(f"No markdown files found in '{directory}'")
            return set()
        
        if verbose:
            print(f"Found {len(markdown_files)} markdown files")
            print("=" * 60)
        
        all_non_english_words = set()
        
        for filepath in markdown_files:
            if verbose:
                print(f"Processing: {filepath}")
            words = self.process_markdown_file(filepath, verbose)
            all_non_english_words.update(words)
            
            if verbose:
                if not words:
                    print("  No non-English words found in headings")
                print("-" * 40)
        
        # Save results to file
        if all_non_english_words:
            # Sort words alphabetically (case-insensitive)
            sorted_words = sorted(all_non_english_words, key=str.lower)
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    for word in sorted_words:
                        f.write(f"{word}\n")
                
                if verbose:
                    print(f"\nResults saved to '{output_file}'")
                    print(f"Total unique non-English words found: {len(sorted_words)}")
                    print("\nFirst 20 words:")
                    for word in sorted_words[:20]:
                        print(f"  {word}")
                    
                    if len(sorted_words) > 20:
                        print(f"  ... and {len(sorted_words) - 20} more")
            
            except Exception as e:
                print(f"Error saving results to {output_file}: {e}")
        else:
            if verbose:
                print("\nNo non-English words found in any headings.")
        
        return all_non_english_words
    
    def analyze_specific_words(self, words: List[str]) -> None:
        """
        Analyze specific words to see if they're in the English dictionary.
        
        Args:
            words: List of words to analyze
        """
        print("Word Analysis:")
        print("=" * 30)
        
        for word in words:
            is_english = self.is_english_word(word)
            status = "English" if is_english else "Non-English"
            print(f"'{word}' -> {status}")
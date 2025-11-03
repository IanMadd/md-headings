"""
Markdown Headings Converter Module

This module provides the MarkdownHeadingsConverter class for converting uppercase
markdown headings to sentence case while preserving proper nouns.
"""

import re
from pathlib import Path
from typing import Set, Optional


class MarkdownHeadingsConverter:
    """
    A class for converting markdown headings from uppercase to sentence case
    while preserving proper nouns from a specified list.
    """
    
    def __init__(self, proper_nouns_file: Optional[str] = None):
        """
        Initialize the converter with optional proper nouns file.
        
        Args:
            proper_nouns_file: Path to text file containing proper nouns (one per line)
        """
        self.proper_nouns = set()
        if proper_nouns_file:
            self.load_proper_nouns(proper_nouns_file)
        
        # Regex pattern to match markdown headings (# to ######)
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    def load_proper_nouns(self, filepath: str) -> None:
        """
        Load proper nouns from a text file.
        
        Args:
            filepath: Path to the proper nouns file
            
        Raises:
            FileNotFoundError: If the proper nouns file doesn't exist
            Exception: For other file reading errors
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    noun = line.strip()
                    if noun and not noun.startswith('#'):  # Skip empty lines and comments
                        self.proper_nouns.add(noun)
            print(f"Loaded {len(self.proper_nouns)} proper nouns from {filepath}")
        except FileNotFoundError:
            print(f"Warning: Proper nouns file '{filepath}' not found. Proceeding without proper nouns.")
        except Exception as e:
            print(f"Error loading proper nouns file: {e}")
    
    def convert_to_sentence_case(self, text: str) -> str:
        """
        Convert text to sentence case while preserving proper nouns.
        
        Args:
            text: The heading text to convert
            
        Returns:
            Converted text in sentence case
        """
        # Common prepositions and articles that should be lowercase (unless first word)
        lowercase_words = {
            'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'nor', 
            'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet', 'with', 'from', 
            'into', 'onto', 'upon', 'over', 'under', 'above', 'below', 'across',
            'through', 'during', 'before', 'after', 'since', 'until', 'within'
        }
        
        # First, handle multi-word proper nouns
        result_text = text
        for noun in sorted(self.proper_nouns, key=len, reverse=True):
            if ' ' in noun or '.' in noun:  # Multi-word or dotted proper nouns
                # Create a case-insensitive pattern
                pattern = re.compile(re.escape(noun), re.IGNORECASE)
                result_text = pattern.sub(noun, result_text)
        
        # Now process individual words
        words = result_text.split()
        result = []
        
        for i, word in enumerate(words):
            # Extract the core word without punctuation for comparison
            word_clean = re.sub(r'[^\w.]', '', word)  # Keep dots for things like js, css
            
            # Check if this word is a single-word proper noun
            matching_noun = None
            for noun in self.proper_nouns:
                if ' ' not in noun and word_clean.lower() == noun.lower():
                    matching_noun = noun
                    break
            
            if matching_noun:
                # Use the proper noun's exact capitalization
                leading_punct = re.match(r'^[^\w.]*', word).group()
                trailing_punct = re.search(r'[^\w.]*$', word).group()
                result.append(leading_punct + matching_noun + trailing_punct)
            elif i == 0:
                # First word - always capitalize
                result.append(word.capitalize())
            elif word_clean.lower() in lowercase_words:
                # Common words that should be lowercase (unless first word)
                result.append(word.lower())
            elif word_clean.isupper() and len(word_clean) <= 3 and not word_clean.lower() in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'use', 'man', 'new', 'now', 'old', 'see', 'him', 'two', 'how', 'its', 'who', 'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye', 'car', 'cut', 'dog', 'end', 'few', 'fox', 'got', 'hat', 'hot', 'job', 'let', 'lot', 'men', 'mix', 'put', 'red', 'say', 'sun', 'ten', 'top', 'try', 'war', 'way', 'win', 'yes']:
                # Keep short uppercase words that are likely abbreviations (not common English words)
                result.append(word)
            else:
                # Default to lowercase for other words
                result.append(word.lower())
        
        return ' '.join(result)
    
    def process_heading(self, match) -> str:
        """
        Process a single heading match and convert it to sentence case.
        
        Args:
            match: Regex match object for a heading
            
        Returns:
            Processed heading string
        """
        heading_level = match.group(1)  # The # symbols
        heading_text = match.group(2)   # The actual heading text
        
        # Convert to sentence case
        converted_text = self.convert_to_sentence_case(heading_text)
        
        return f"{heading_level} {converted_text}"
    
    def process_markdown_file(self, filepath: Path) -> bool:
        """
        Process a single markdown file and convert headings.
        
        Args:
            filepath: Path to the markdown file
            
        Returns:
            True if file was modified, False otherwise
            
        Raises:
            Exception: For file reading/writing errors
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and process all headings
            original_content = content
            modified_content = self.heading_pattern.sub(self.process_heading, content)
            
            # Only write if content changed
            if modified_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return False
    
    def process_directory(self, directory: str, dry_run: bool = False) -> None:
        """
        Process all markdown files in a directory recursively.
        
        Args:
            directory: Path to the directory to process
            dry_run: If True, only show what would be changed without modifying files
        """
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"Error: Directory '{directory}' does not exist.")
            return
        
        # Find all markdown files
        markdown_files = list(directory_path.rglob('*.md')) + list(directory_path.rglob('*.markdown'))
        
        if not markdown_files:
            print(f"No markdown files found in '{directory}'")
            return
        
        print(f"Found {len(markdown_files)} markdown files")
        
        modified_count = 0
        
        for filepath in markdown_files:
            if dry_run:
                # In dry run mode, just check what would be changed
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    headings = self.heading_pattern.findall(content)
                    if headings:
                        print(f"\n{filepath}:")
                        for level, text in headings:
                            converted = self.convert_to_sentence_case(text)
                            if converted != text:
                                print(f"  {level} {text} → {level} {converted}")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
            else:
                # Actually process the file
                if self.process_markdown_file(filepath):
                    print(f"Modified: {filepath}")
                    modified_count += 1
                else:
                    print(f"No changes: {filepath}")
        
        if not dry_run:
            print(f"\nProcessing complete. Modified {modified_count} files.")
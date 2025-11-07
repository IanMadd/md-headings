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
        
        # Patterns for detecting code blocks
        self.fenced_code_pattern = re.compile(r'^```[\s\S]*?^```', re.MULTILINE)
        self.indented_code_pattern = re.compile(r'^(    |\t).*$', re.MULTILINE)
        
        # Patterns for detecting TOML frontmatter
        self.toml_frontmatter_pattern = re.compile(r'^(\+\+\+\n)(.*?)(\n\+\+\+)', re.DOTALL)
        # Pattern to match title fields in TOML (title, linkTitle, description)
        self.toml_title_pattern = re.compile(r'^(\s*)(title|linkTitle|description)(\s*=\s*)"([^"]*)"', re.MULTILINE)
        # Additional pattern for nested menu titles (handles [menu.xxx] sections with title fields)
        self.toml_menu_title_pattern = re.compile(r'(\[menu\.[^\]]+\].*?)(\s+title\s*=\s*)"([^"]*)"', re.DOTALL | re.MULTILINE)
    
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
    
    def remove_code_blocks(self, content: str) -> str:
        """
        Remove code blocks from markdown content to avoid processing comments within them.
        
        Args:
            content: Markdown content
            
        Returns:
            Content with code blocks removed
        """
        # Remove fenced code blocks (```...```)
        content_without_fenced = self.fenced_code_pattern.sub('', content)
        
        # Split into lines to handle indented code blocks
        lines = content_without_fenced.split('\n')
        filtered_lines = []
        in_code_block = False
        
        for line in lines:
            # Check if this line is indented code (4 spaces or 1 tab at start)
            if re.match(r'^(    |\t)', line):
                in_code_block = True
                continue  # Skip this line
            else:
                # If we were in a code block and now we're not, we've exited
                if in_code_block and line.strip() == '':
                    continue  # Skip empty lines after code blocks
                in_code_block = False
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
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
        
        # First, identify and protect multi-word proper nouns
        # Create a list of (start, end, replacement) tuples
        replacements = []
        
        for noun in sorted(self.proper_nouns, key=len, reverse=True):
            if ' ' in noun or '.' in noun:  # Multi-word or dotted proper nouns
                # Find all occurrences (case-insensitive)
                pattern = re.compile(re.escape(noun), re.IGNORECASE)
                for match in pattern.finditer(text):
                    start, end = match.span()
                    # Check if this range overlaps with any existing replacement
                    overlaps = False
                    for pstart, pend, _ in replacements:
                        if not (end <= pstart or start >= pend):
                            overlaps = True
                            break
                    if not overlaps:
                        replacements.append((start, end, noun))
        
        # Sort replacements by start position (reverse order for building result)
        replacements.sort(reverse=True)
        
        # Apply replacements from end to start to maintain positions
        result_text = text
        for start, end, noun in replacements:
            result_text = result_text[:start] + noun + result_text[end:]
        
        # Now process individual words
        words = result_text.split()
        result = []
        
        for i, word in enumerate(words):
            # Extract the core word without punctuation for comparison
            word_clean = re.sub(r'[^\w.]', '', word)  # Keep dots for things like js, css
            
            # Check if this word is part of a multi-word proper noun that was already handled
            # If the word is already in the correct case from multi-word replacement, preserve it
            word_lower = word_clean.lower()
            
            # Check if this word is a single-word proper noun
            matching_noun = None
            for noun in self.proper_nouns:
                if ' ' not in noun and '.' not in noun and word_lower == noun.lower():
                    matching_noun = noun
                    break
            
            if matching_noun:
                # Use the proper noun's exact capitalization
                leading_punct = re.match(r'^[^\w.]*', word).group()
                trailing_punct = re.search(r'[^\w.]*$', word).group()
                result.append(leading_punct + matching_noun + trailing_punct)
            elif i == 0:
                # First word - always capitalize (unless it's already correct from multi-word noun)
                if word_clean == word_clean.capitalize() or (len(words) > 1 and any(
                    noun.startswith(word_clean) and ' ' in noun 
                    for noun in self.proper_nouns
                )):
                    result.append(word)
                else:
                    result.append(word.capitalize())
            elif word_lower in lowercase_words:
                # Common words that should be lowercase
                result.append(word.lower())
            elif word_clean.isupper() and len(word_clean) <= 3 and word_lower not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'use', 'man', 'new', 'now', 'old', 'see', 'him', 'two', 'how', 'its', 'who', 'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye', 'car', 'cut', 'dog', 'end', 'few', 'fox', 'got', 'hat', 'hot', 'job', 'let', 'lot', 'men', 'mix', 'put', 'red', 'say', 'sun', 'ten', 'top', 'try', 'war', 'way', 'win', 'yes']:
                # Keep short uppercase words that are likely abbreviations
                result.append(word)
            else:
                # Check if this word is part of a multi-word proper noun (preserve its case)
                is_part_of_multiword = False
                for noun in self.proper_nouns:
                    if (' ' in noun or '.' in noun) and word_clean in noun.split():
                        # This word is part of a multi-word proper noun, check if case matches
                        if word_clean in noun:
                            is_part_of_multiword = True
                            result.append(word)
                            break
                
                if not is_part_of_multiword:
                    # Default to lowercase
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
    
    def process_toml_frontmatter(self, frontmatter_content: str) -> str:
        """
        Process TOML frontmatter and convert title fields to sentence case.
        
        Args:
            frontmatter_content: The TOML frontmatter content (without +++ delimiters)
            
        Returns:
            Processed frontmatter content with converted titles
        """
        def replace_title(match):
            indent = match.group(1)
            field_name = match.group(2)
            equals_and_space = match.group(3)
            title_text = match.group(4)
            
            # Convert to sentence case
            converted_text = self.convert_to_sentence_case(title_text)
            
            return f'{indent}{field_name}{equals_and_space}"{converted_text}"'
        
        def replace_menu_title(match):
            menu_section = match.group(1)
            title_part = match.group(2)
            title_text = match.group(3)
            
            # Convert to sentence case
            converted_text = self.convert_to_sentence_case(title_text)
            
            return f'{menu_section}{title_part}"{converted_text}"'
        
        # Replace regular title fields first
        result = self.toml_title_pattern.sub(replace_title, frontmatter_content)
        
        # Then replace nested menu title fields
        result = self.toml_menu_title_pattern.sub(replace_menu_title, result)
        
        return result
    
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
            
            # Process content while avoiding code blocks
            original_content = content
            modified_content = self.process_content_avoiding_code_blocks(content)
            
            # Only write if content changed
            if modified_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return False
    
    def process_content_avoiding_code_blocks(self, content: str) -> str:
        """
        Process markdown content to convert headings while avoiding code blocks.
        
        Args:
            content: Original markdown content
            
        Returns:
            Modified content with converted headings
        """
        # First, check for and process TOML frontmatter
        frontmatter_match = self.toml_frontmatter_pattern.match(content)
        
        if frontmatter_match:
            # Extract frontmatter components
            opening_delimiter = frontmatter_match.group(1)  # "+++\n"
            frontmatter_content = frontmatter_match.group(2)  # The TOML content
            closing_delimiter = frontmatter_match.group(3)  # "\n+++"
            
            # Process the frontmatter
            processed_frontmatter = self.process_toml_frontmatter(frontmatter_content)
            
            # Get the rest of the content after frontmatter
            content_after_frontmatter = content[frontmatter_match.end():]
            
            # Process the markdown content (headings) after frontmatter
            processed_content = self._process_markdown_content(content_after_frontmatter)
            
            # Combine processed frontmatter with processed content
            return opening_delimiter + processed_frontmatter + closing_delimiter + processed_content
        else:
            # No frontmatter, just process markdown content
            return self._process_markdown_content(content)
    
    def _process_markdown_content(self, content: str) -> str:
        """
        Internal method to process markdown content for headings.
        
        Args:
            content: Markdown content (without frontmatter)
            
        Returns:
            Modified content with converted headings
        """
        # Split content into chunks, identifying code blocks
        chunks = []
        current_pos = 0
        
        # Find all fenced code blocks first
        for match in self.fenced_code_pattern.finditer(content):
            # Add content before the code block
            before_code = content[current_pos:match.start()]
            if before_code:
                chunks.append(('text', before_code))
            
            # Add the code block as-is
            chunks.append(('code', match.group()))
            current_pos = match.end()
        
        # Add remaining content after last code block
        if current_pos < len(content):
            remaining = content[current_pos:]
            chunks.append(('text', remaining))
        
        # Process each chunk
        result_chunks = []
        for chunk_type, chunk_content in chunks:
            if chunk_type == 'code':
                # Don't modify code blocks
                result_chunks.append(chunk_content)
            else:
                # Process headings in text chunks, but avoid indented code blocks
                processed = self.process_text_chunk_avoiding_indented_code(chunk_content)
                result_chunks.append(processed)
        
        return ''.join(result_chunks)
    
    def process_text_chunk_avoiding_indented_code(self, text: str) -> str:
        """
        Process a text chunk while avoiding indented code blocks.
        
        Args:
            text: Text chunk to process
            
        Returns:
            Processed text with converted headings
        """
        lines = text.split('\n')
        result_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check if this line is indented code (4 spaces or 1 tab at start)
            if re.match(r'^(    |\t)', line):
                # This is indented code, copy it as-is and skip until we exit the code block
                result_lines.append(line)
                i += 1
                
                # Continue copying indented lines and empty lines
                while i < len(lines):
                    next_line = lines[i]
                    if re.match(r'^(    |\t)', next_line) or next_line.strip() == '':
                        result_lines.append(next_line)
                        i += 1
                    else:
                        break
            else:
                # Check if this is a heading
                heading_match = self.heading_pattern.match(line)
                if heading_match:
                    # Process the heading
                    converted_heading = self.process_heading(heading_match)
                    result_lines.append(converted_heading)
                else:
                    # Regular line, keep as-is
                    result_lines.append(line)
                i += 1
        
        return '\n'.join(result_lines)
    
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
                    
                    # Remove code blocks before finding headings for dry run
                    content_without_code = self.remove_code_blocks(content)
                    headings = self.heading_pattern.findall(content_without_code)
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
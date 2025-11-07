"""
Tests for error handling in the converter module.
"""

import sys
import os
import tempfile
import pytest

# Add the parent directory to the path so we can import md_headings
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from md_headings.converter import MarkdownHeadingsConverter


def test_proper_nouns_file_not_found():
    """Test that FileNotFoundError is raised when proper nouns file doesn't exist."""
    
    # Try to create converter with non-existent file
    with pytest.raises(FileNotFoundError) as exc_info:
        MarkdownHeadingsConverter("nonexistent_file.txt")
    
    assert "nonexistent_file.txt" in str(exc_info.value)
    assert "not found" in str(exc_info.value)
    print("✓ FileNotFoundError correctly raised for missing proper nouns file")


def test_proper_nouns_file_exists():
    """Test that converter works correctly when proper nouns file exists."""
    
    # Create a temporary proper nouns file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("JavaScript\n")
        f.write("API\n")
        f.write("PostgreSQL\n")
        proper_nouns_file = f.name
    
    try:
        # This should work without raising an exception
        converter = MarkdownHeadingsConverter(proper_nouns_file)
        
        # Verify proper nouns were loaded
        assert len(converter.proper_nouns) == 3
        assert "JavaScript" in converter.proper_nouns
        assert "API" in converter.proper_nouns
        assert "PostgreSQL" in converter.proper_nouns
        
        print("✓ Converter successfully created with existing proper nouns file")
        
    finally:
        # Clean up
        os.unlink(proper_nouns_file)


def test_converter_without_proper_nouns():
    """Test that converter works correctly without proper nouns file."""
    
    # This should work fine
    converter = MarkdownHeadingsConverter()
    
    # Should have empty proper nouns set
    assert len(converter.proper_nouns) == 0
    
    # Should still be able to convert text
    result = converter.convert_to_sentence_case("THIS AND THAT EXAMPLE HEADING")
    assert result == "This and that example heading"
    
    print("✓ Converter works correctly without proper nouns file")


def test_proper_nouns_file_reading_error():
    """Test handling of file reading errors (permissions, etc.)."""
    
    # Create a file and then make it unreadable (on Unix-like systems)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test\n")
        proper_nouns_file = f.name
    
    try:
        # Try to make it unreadable (this might not work on all systems)
        try:
            os.chmod(proper_nouns_file, 0o000)
            
            # This should raise an exception (might be PermissionError or other)
            with pytest.raises(Exception) as exc_info:
                MarkdownHeadingsConverter(proper_nouns_file)
            
            # The error message should mention the file loading error
            assert "Error loading proper nouns file" in str(exc_info.value)
            print("✓ File reading error correctly handled")
            
        except (OSError, PermissionError):
            # If we can't change permissions, skip this test
            print("⚠ Skipping permission test (unable to change file permissions)")
            
    finally:
        # Clean up - restore permissions first
        try:
            os.chmod(proper_nouns_file, 0o644)
        except (OSError, PermissionError):
            pass
        try:
            os.unlink(proper_nouns_file)
        except (OSError, PermissionError):
            pass


if __name__ == '__main__':
    print("Running error handling tests...\n")
    print("=" * 60)
    
    test_proper_nouns_file_not_found()
    test_proper_nouns_file_exists()
    test_converter_without_proper_nouns()
    test_proper_nouns_file_reading_error()
    
    print("\n" + "=" * 60)
    print("All error handling tests passed! ✓")
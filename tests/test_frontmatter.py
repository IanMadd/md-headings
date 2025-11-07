"""
Tests for TOML frontmatter processing in the converter module.
"""

import tempfile
from pathlib import Path
import sys
import os

# Add the parent directory to the path so we can import md_headings
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from md_headings.converter import MarkdownHeadingsConverter


def test_toml_frontmatter_conversion():
    """Test that TOML frontmatter title fields are converted to sentence case."""
    
    # Create a temporary proper nouns file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Chef Habitat\n")  # Multi-word proper noun should be processed first
        proper_nouns_file = f.name
    
    try:
        # Initialize converter
        converter = MarkdownHeadingsConverter(proper_nouns_file)
        
        # Test content with TOML frontmatter
        test_content = """+++
title = "Chef Habitat and Containers"
description = "Chef Habitat and Containers"
linkTitle = "Containers"
list_pages = true

[menu.containers]
    title = "Chef Habitat and Containers"
    identifier = "containers/containers"
    parent = "containers"
    weight = 10

+++

## GETTING STARTED WITH CHEF HABITAT

This is some content.
"""
        
        expected_content = """+++
title = "Chef Habitat and containers"
description = "Chef Habitat and containers"
linkTitle = "Containers"
list_pages = true

[menu.containers]
    title = "Chef Habitat and containers"
    identifier = "containers/containers"
    parent = "containers"
    weight = 10

+++

## Getting started with Chef Habitat

This is some content.
"""
        
        result = converter.process_content_avoiding_code_blocks(test_content)
        
        print("Input:")
        print(test_content)
        print("\nExpected:")
        print(expected_content)
        print("\nActual Result:")
        print(result)
        
        # Check frontmatter fields
        assert 'title = "Chef Habitat and containers"' in result, \
            "Top-level title should be converted to sentence case"
        assert 'linkTitle = "Containers"' in result, \
            "linkTitle should be preserved as-is (already sentence case)"
        assert 'description = "Chef Habitat and containers"' in result, \
            "description should be converted to sentence case"
        
        # Check nested menu title
        assert '    title = "Chef Habitat and containers"' in result, \
            "Nested menu title should be converted to sentence case"
        
        # Check that markdown heading was also converted
        assert '## Getting started with Chef Habitat' in result, \
            "Markdown heading should also be converted"
        
        # Check that other fields are unchanged
        assert 'identifier = "containers/containers"' in result, \
            "Non-title fields should not be modified"
        assert 'weight = 10' in result, \
            "Numeric fields should not be modified"
        
        print("\n✓ All frontmatter conversion tests passed!")
        
    finally:
        # Clean up
        os.unlink(proper_nouns_file)


def test_frontmatter_with_multiple_proper_nouns():
    """Test frontmatter conversion with multiple proper nouns."""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("PostgreSQL\n")
        f.write("Node.js\n")
        f.write("API\n")
        proper_nouns_file = f.name
    
    try:
        converter = MarkdownHeadingsConverter(proper_nouns_file)
        
        test_content = """+++
title = "DEPLOYING NODE.JS WITH POSTGRESQL AND API"
description = "GUIDE TO DEPLOYMENT"
+++

## DEPLOYMENT STEPS
"""
        
        result = converter.process_content_avoiding_code_blocks(test_content)
        
        print("\n\nTest 2 - Multiple Proper Nouns:")
        print("Input:")
        print(test_content)
        print("\nResult:")
        print(result)
        
        assert 'title = "Deploying Node.js with PostgreSQL and API"' in result, \
            "All proper nouns should be preserved in title"
        assert 'description = "Guide to deployment"' in result, \
            "Description should be converted to sentence case"
        assert '## Deployment steps' in result, \
            "Heading should be converted to sentence case"
        
        print("✓ Multiple proper nouns test passed!")
        
    finally:
        os.unlink(proper_nouns_file)


def test_no_frontmatter():
    """Test that files without frontmatter still work correctly."""
    
    converter = MarkdownHeadingsConverter()
    
    test_content = """## GETTING STARTED

This is content without frontmatter.
"""
    
    result = converter.process_content_avoiding_code_blocks(test_content)
    
    print("\n\nTest 3 - No Frontmatter:")
    print("Input:")
    print(test_content)
    print("\nResult:")
    print(result)
    
    assert '## Getting started' in result, \
        "Heading should be converted even without frontmatter"
    
    print("✓ No frontmatter test passed!")


def test_yaml_frontmatter_ignored():
    """Test that YAML frontmatter (---) is not processed (only TOML +++ is supported)."""
    
    converter = MarkdownHeadingsConverter()
    
    test_content = """---
title: "CHEF HABITAT AND CONTAINERS"
---

## GETTING STARTED
"""
    
    result = converter.process_content_avoiding_code_blocks(test_content)
    
    print("\n\nTest 4 - YAML Frontmatter (should be ignored):")
    print("Input:")
    print(test_content)
    print("\nResult:")
    print(result)
    
    # YAML frontmatter should not be processed
    assert 'title: "CHEF HABITAT AND CONTAINERS"' in result, \
        "YAML frontmatter should not be modified"
    
    # But markdown heading should still be converted
    assert '## Getting started' in result, \
        "Heading should still be converted"
    
    print("✓ YAML frontmatter ignored test passed!")


def test_nested_menu_title_conversion():
    """Test that nested menu titles in TOML frontmatter are properly converted."""
    
    # Create a temporary proper nouns file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Chef\nHabitat\nDocker\nContainers\n")
        proper_nouns_file = f.name
    
    try:
        converter = MarkdownHeadingsConverter(proper_nouns_file)
        
        test_content = """+++
title = "Main Title Here"

[menu.containers]
  parent = "habitat"
  weight = 10
  title = "Chef Habitat And Containers"

[menu.other]
  title = "Another Menu Title Here"
  weight = 20
+++

## SOME HEADING
"""
        
        result = converter.process_content_avoiding_code_blocks(test_content)
        
        print("\n\nTest 5 - Nested Menu Titles:")
        print("Input:")
        print(test_content)
        print("\nResult:")
        print(result)
        
        # Check that nested menu titles are converted
        assert '  title = "Chef Habitat and Containers"' in result, \
            "First nested menu title should be converted with proper nouns preserved"
        assert '  title = "Another menu title here"' in result, \
            "Second nested menu title should be converted to sentence case"
        
        # Check that top-level title is also converted
        assert 'title = "Main title here"' in result, \
            "Top-level title should be converted"
        
        # Check that regular headings are converted
        assert '## Some heading' in result, \
            "Regular headings should still be converted"
        
        print("✓ Nested menu titles test passed!")
        
    finally:
        os.unlink(proper_nouns_file)


if __name__ == '__main__':
    print("Running TOML frontmatter conversion tests...\n")
    print("=" * 60)
    
    test_toml_frontmatter_conversion()
    test_frontmatter_with_multiple_proper_nouns()
    test_no_frontmatter()
    test_yaml_frontmatter_ignored()
    test_nested_menu_title_conversion()
    
    print("\n" + "=" * 60)
    print("All frontmatter tests passed! ✓")

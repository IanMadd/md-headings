"""
Markdown Headings Processing Tools

This package provides tools for processing and converting markdown headings:
- HeadingsConverter: Convert uppercase headings to sentence case with proper noun preservation
- WordExtractor: Extract non-English words from markdown headings
"""

from .converter import MarkdownHeadingsConverter
from .extractor import MarkdownHeadingWordExtractor

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = ["MarkdownHeadingsConverter", "MarkdownHeadingWordExtractor"]
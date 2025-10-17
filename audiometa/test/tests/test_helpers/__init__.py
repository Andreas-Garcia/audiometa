"""Test helpers for audio metadata testing.

This module provides a unified interface for creating temporary test files
with metadata and performing external tool operations for testing.
"""

from .temp_file_with_metadata import TempFileWithMetadata

__all__ = [
    'TempFileWithMetadata'
]

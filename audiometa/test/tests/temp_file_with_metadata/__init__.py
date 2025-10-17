"""Temporary file with metadata utilities for testing.

This module provides specialized helper classes for creating temporary test files
with specific metadata configurations, with automatic cleanup support and header detection.
"""

from .base import TempFileWithMetadata
from .id3v1_version import TempFileWithId3v1Version
from .id3v2_version import TempFileWithId3v2Version

__all__ = [
    'TempFileWithMetadata',
    'TempFileWithId3v1Version',
    'TempFileWithId3v2Version'
]

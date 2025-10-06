"""Metadata writing strategy constants for audio metadata handling."""
from enum import Enum


class MetadataWritingStrategy(str, Enum):
    """Strategy for handling metadata when writing to files with existing metadata in other formats."""
    
    PRESERVE = 'preserve'
    """Write to native format only, preserve existing metadata in other formats (default)"""
    
    CLEANUP = 'cleanup'
    """Write to native format and remove all non-native metadata formats"""
    
    SYNC = 'sync'
    """Write to native format and synchronize other metadata formats that are already present"""
    
    IGNORE = 'ignore'
    """Write to native format only, ignore other formats completely (same as PRESERVE)"""

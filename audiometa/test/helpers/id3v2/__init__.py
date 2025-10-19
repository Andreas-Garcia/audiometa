"""ID3v2 metadata format helpers."""

# Core operations (following RIFF pattern)
from .id3v2_header_verifier import ID3HeaderVerifier
from .id3v2_metadata_deleter import ID3v2MetadataDeleter
from .id3v2_metadata_setter import ID3v2MetadataSetter, ID3v1MetadataSetter
from .id3v2_metadata_verifier import ID3v2MetadataVerifier

# Specialized managers
from .id3v2_multiple_metadata_manager import ID3v2MultipleMetadataManager

# Advanced tools
from .id3v2_frame_manual_creator import ManualID3v2FrameCreator

# External tool wrappers
from .id3v2_metadata_deleter import ExternalMetadataToolError

__all__ = [
    # Core operations
    "ID3HeaderVerifier",
    "ID3v2MetadataDeleter",
    "ID3v2MetadataSetter",
    "ID3v1MetadataSetter",
    "ID3v2MetadataVerifier",
    
    # Specialized managers
    "ID3v2MultipleMetadataManager",
    
    # Advanced tools
    "ManualID3v2FrameCreator",
    
    # External tool wrappers
    "ExternalMetadataToolError"
]
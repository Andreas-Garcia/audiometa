"""ID3v2 metadata format helpers."""

# Core operations (following RIFF pattern)
from .id3v2_header_verifier import ID3HeaderVerifier
from .id3v2_metadata_deleter import ID3v2MetadataDeleter, ID3v1MetadataDeleter
from .id3v2_metadata_setter import ID3v2MetadataSetter, ID3v1MetadataSetter
from .id3v2_metadata_verifier import ID3v2MetadataVerifier

# Specialized managers
from .id3v2_multiple_metadata_manager import ID3v2MultipleMetadataManager
from .id3v2_separator_metadata_manager import ID3v2SeparatorMetadataManager

# Advanced tools
from .manual_id3v2_frame_creator import ManualID3v2FrameCreator

# External tool wrappers
from .mid3v2_tool import Mid3v2Tool, ExternalMetadataToolError
from .id3v2_tool import Id3v2Tool

__all__ = [
    # Core operations
    "ID3HeaderVerifier",
    "ID3v2MetadataDeleter",
    "ID3v1MetadataDeleter",
    "ID3v2MetadataSetter",
    "ID3v1MetadataSetter",
    "ID3v2MetadataVerifier",
    
    # Specialized managers
    "ID3v2MultipleMetadataManager",
    "ID3v2SeparatorMetadataManager",
    
    # Advanced tools
    "ManualID3v2FrameCreator",
    
    # External tool wrappers
    "Mid3v2Tool",
    "ExternalMetadataToolError",
    "Id3v2Tool"
]
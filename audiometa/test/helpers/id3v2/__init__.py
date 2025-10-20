"""ID3v2 metadata format helpers."""

# Core operations (following RIFF pattern)
from .id3v2_header_verifier import ID3V2HeaderVerifier
from .id3v2_metadata_deleter import ID3v2MetadataDeleter
from .id3v2_metadata_setter import ID3v2MetadataSetter, ID3v1MetadataSetter
from .id3v2_metadata_inspector import ID3v2MetadataInspector

# Specialized managers (moved to ID3v2MetadataSetter)

# Advanced tools
from .id3v2_frame_manual_creator import ManualID3v2FrameCreator

# External tool wrappers
from ..common.external_tool_runner import ExternalMetadataToolError

__all__ = [
    # Core operations
    "ID3V2HeaderVerifier",
    "ID3v2MetadataDeleter",
    "ID3v2MetadataSetter",
    "ID3v1MetadataSetter",
    "ID3v2MetadataInspector",
    
    # Specialized managers (moved to ID3v2MetadataSetter)
    
    # Advanced tools
    "ManualID3v2FrameCreator",
    
    # External tool wrappers
    "ExternalMetadataToolError"
]
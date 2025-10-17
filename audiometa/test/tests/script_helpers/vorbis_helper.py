"""Helper class for Vorbis metadata operations using external tools."""

from pathlib import Path
from .base_helper import BaseHelper


class VorbisHelper(BaseHelper):
    """Helper class for Vorbis metadata operations (FLAC, OGG)."""
    
    @staticmethod
    def set_max_metadata(file_path: Path):
        """Set maximum Vorbis metadata using external script."""
        return VorbisHelper._run_script("set-vorbis-max-metadata.sh", file_path)
    
    @staticmethod
    def set_artists_one_two_three(file_path: Path):
        """Set specific artists metadata using external script."""
        return VorbisHelper._run_script("set-artists-One-Two-Three-vorbis.sh", file_path)
    
    @staticmethod
    def has_comments(file_path: Path) -> bool:
        """Check if file has Vorbis comments using metaflac."""
        try:
            result = VorbisHelper._run_external_tool(
                ['metaflac', '--list', str(file_path)],
                check=True
            )
            return 'VORBIS_COMMENT' in result.stdout
        except (RuntimeError, FileNotFoundError):
            return False

"""ID3v1 metadata setting operations."""

from pathlib import Path
from typing import Dict, Any

from ..common.external_tool_runner import run_external_tool


class ID3v1MetadataSetter:
    """Static utility class for ID3v1 metadata setting using external tools."""

    @staticmethod
    def set_genre(file_path: Path, genre_code: str) -> None:
        """Set ID3v1 genre using external id3v2 tool."""
        ID3v1MetadataSetter.set_genre(file_path, genre_code)

    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        """Set ID3v1 comment using external id3v2 tool."""
        ID3v1MetadataSetter.set_comment(file_path, comment)

    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        """Set ID3v1 title using external id3v2 tool."""
        ID3v1MetadataSetter.set_title(file_path, title)

    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        """Set ID3v1 artist using external id3v2 tool."""
        ID3v1MetadataSetter.set_artist(file_path, artist)

    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        """Set ID3v1 album using external id3v2 tool."""
        ID3v1MetadataSetter.set_album(file_path, album)

    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        """Set maximum ID3v1 metadata using external script."""
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-id3v1-max-metadata.sh", file_path, scripts_dir)
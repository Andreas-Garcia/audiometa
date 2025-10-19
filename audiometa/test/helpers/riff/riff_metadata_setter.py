"""RIFF metadata setting operations."""

from pathlib import Path
from .bwfmetaedit_tool import BwfmetaeditTool
from .exiftool_tool import ExiftoolTool
from ..id3v2.mid3v2_tool import ExternalMetadataToolError


class RIFFMetadataSetter:
    """Static utility class for RIFF metadata setting using external tools."""
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        """Set RIFF comment using bwfmetaedit tool."""
        BwfmetaeditTool.set_comment(file_path, comment)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        """Set RIFF title using bwfmetaedit tool."""
        BwfmetaeditTool.set_title(file_path, title)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        """Set RIFF artist using bwfmetaedit tool."""
        BwfmetaeditTool.set_artist(file_path, artist)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        """Set RIFF album using bwfmetaedit tool."""
        BwfmetaeditTool.set_album(file_path, album)
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        """Set RIFF genre using bwfmetaedit tool."""
        BwfmetaeditTool.set_genre(file_path, genre)
    
    @staticmethod
    def set_genre_text(file_path: Path, genre_text: str) -> None:
        """Set RIFF genre using external exiftool or bwfmetaedit tool."""
        try:
            # Try exiftool first
            ExiftoolTool.set_riff_genre(file_path, genre_text)
        except ExternalMetadataToolError:
            try:
                # Fallback to bwfmetaedit
                BwfmetaeditTool.set_genre(file_path, genre_text)
            except ExternalMetadataToolError as e:
                raise RuntimeError(f"Failed to set RIFF genre: {e}") from e
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        """Set RIFF lyrics using bwfmetaedit tool."""
        BwfmetaeditTool.set_lyrics(file_path, lyrics)
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        """Set RIFF language using bwfmetaedit tool."""
        BwfmetaeditTool.set_language(file_path, language)
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        """Set maximum RIFF metadata using external script."""
        from ..common.script_runner import ScriptRunner
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        script_runner = ScriptRunner(scripts_dir)
        script_runner.run_script("set-riff-max-metadata.sh", file_path)
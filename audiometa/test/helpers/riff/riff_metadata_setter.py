"""RIFF metadata setting operations."""

from pathlib import Path
from .bwfmetaedit_tool import BwfmetaeditTool
from ..id3v2.mid3v2_tool import ExternalMetadataToolError
from ..common.external_tool_runner import run_external_tool


class RIFFMetadataSetter:
    """Static utility class for RIFF metadata setting using external tools."""
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        BwfmetaeditTool.set_comment(file_path, comment)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        BwfmetaeditTool.set_title(file_path, title)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        BwfmetaeditTool.set_artist(file_path, artist)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        BwfmetaeditTool.set_album(file_path, album)
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        BwfmetaeditTool.set_genre(file_path, genre)
    
    @staticmethod
    def set_genre_text(file_path: Path, genre_text: str) -> None:
        try:
            # Try exiftool first
            RIFFMetadataSetter.set_riff_genre(file_path, genre_text)
        except ExternalMetadataToolError:
            try:
                # Fallback to bwfmetaedit
                BwfmetaeditTool.set_genre(file_path, genre_text)
            except ExternalMetadataToolError as e:
                raise RuntimeError(f"Failed to set RIFF genre: {e}") from e
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        BwfmetaeditTool.set_lyrics(file_path, lyrics)
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        BwfmetaeditTool.set_language(file_path, language)
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.script_runner import ScriptRunner
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        script_runner = ScriptRunner(scripts_dir)
        script_runner.run_script("set-riff-max-metadata.sh", file_path)
    
    @staticmethod
    def set_separator_artists(file_path: Path, artists_string: str):
        """Set RIFF artists as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--IART={artists_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_separator_genres(file_path: Path, genres_string: str):
        command = ["bwfmetaedit", f"--IGNR={genres_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_separator_composers(file_path: Path, composers_string: str):
        command = ["bwfmetaedit", f"--ICMP={composers_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_separator_album_artists(file_path: Path, album_artists_string: str):
        # RIFF doesn't have a standard album artist field, using a custom approach
        command = ["bwfmetaedit", f"--IAAR={album_artists_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_riff_genre(file_path: Path, genre: str) -> None:
        """Set RIFF genre using exiftool."""
        command = [
            "exiftool", "-overwrite_original", 
            f"-Genre={genre}",
            str(file_path)
        ]
        run_external_tool(command, "exiftool")
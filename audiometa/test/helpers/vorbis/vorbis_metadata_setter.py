"""Vorbis metadata setting operations."""

from pathlib import Path
from .metaflac_tool import MetaflacTool


class VorbisMetadataSetter:
    """Static utility class for Vorbis metadata setting using external tools."""
    
    @staticmethod
    def set_genre(file_path: Path, genre_text: str) -> None:
        MetaflacTool.set_genre(file_path, genre_text)
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        MetaflacTool.set_comment(file_path, comment)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        MetaflacTool.set_title(file_path, title)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        MetaflacTool.set_artist(file_path, artist)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        MetaflacTool.set_album(file_path, album)
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        MetaflacTool.set_lyrics(file_path, lyrics)
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        MetaflacTool.set_language(file_path, language)
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        MetaflacTool.set_bpm(file_path, bpm)
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.script_runner import ScriptRunner
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        script_runner = ScriptRunner(scripts_dir)
        script_runner.run_script("set-vorbis-max-metadata.sh", file_path)
    
    @staticmethod
    def set_artists_one_two_three(file_path: Path) -> None:
        from ..common.script_runner import ScriptRunner
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        script_runner = ScriptRunner(scripts_dir)
        script_runner.run_script("set-artists-One-Two-Three-vorbis.sh", file_path)
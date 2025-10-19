"""RIFF metadata setting operations."""

from pathlib import Path
from typing import Dict, Any, List
from ..id3v2.id3v2_metadata_deleter import ExternalMetadataToolError
from ..common.external_tool_runner import run_external_tool


class RIFFMetadataSetter:
    """Static utility class for RIFF metadata setting using external tools."""
    
    @staticmethod
    def set_wav_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        """Set WAV metadata using bwfmetaedit tool."""
        cmd = ["bwfmetaedit"]
        
        # Map common metadata keys to bwfmetaedit arguments
        key_mapping = {
            'title': '--INAM',
            'artist': '--IART',
            'album': '--IPRD',
            'genre': '--IGNR',
            'date': '--ICRD',
            'comment': '--ICMT',
            'track': '--ITRK'
        }
        
        for key, value in metadata.items():
            if key.lower() in key_mapping:
                cmd.extend([f"{key_mapping[key.lower()]}={value}"])
        
        cmd.append(str(file_path))
        run_external_tool(cmd, "bwfmetaedit")
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        command = ["bwfmetaedit", f"--ICMT={comment}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        command = ["bwfmetaedit", f"--INAM={title}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        command = ["bwfmetaedit", f"--IART={artist}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        command = ["bwfmetaedit", f"--IPRD={album}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        command = ["bwfmetaedit", f"--IGNR={genre}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_genre_text(file_path: Path, genre_text: str) -> None:
        """Set RIFF genre using external exiftool or bwfmetaedit tool."""
        try:
            # Try exiftool first
            RIFFMetadataSetter.set_riff_genre(file_path, genre_text)
        except ExternalMetadataToolError:
            try:
                # Fallback to bwfmetaedit
                RIFFMetadataSetter.set_genre(file_path, genre_text)
            except ExternalMetadataToolError as e:
                raise RuntimeError(f"Failed to set RIFF genre: {e}") from e
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        command = ["bwfmetaedit", f"--ILYT={lyrics}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        command = ["bwfmetaedit", f"--ILNG={language}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-riff-max-metadata.sh", file_path, scripts_dir)
    
    @staticmethod
    def set_separator_artists(file_path: Path, artists_string: str):
        command = ["bwfmetaedit", f"--IART={artists_string}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_separator_genres(file_path: Path, genres_string: str):
        command = ["bwfmetaedit", f"--IGNR={genres_string}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_separator_composers(file_path: Path, composers_string: str):
        command = ["bwfmetaedit", f"--ICMP={composers_string}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_separator_album_artists(file_path: Path, album_artists_string: str):
        # RIFF doesn't have a standard album artist field, using a custom approach
        command = ["bwfmetaedit", f"--IAAR={album_artists_string}", str(file_path)]
        run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_riff_genre(file_path: Path, genre: str) -> None:
        command = [
            "exiftool", "-overwrite_original", 
            f"-Genre={genre}",
            str(file_path)
        ]
        run_external_tool(command, "exiftool")
    
    @staticmethod
    def set_multiple_artists(file_path: Path, artists: List[str]):
        # For testing multiple instances, we'd need to use a more sophisticated approach
        # For now, just set the first artist
        if artists:
            command = ["bwfmetaedit", f"--IART={artists[0]}", str(file_path)]
            run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_multiple_genres(file_path: Path, genres: List[str]):
        # For now, just set the first genre
        if genres:
            command = ["bwfmetaedit", f"--IGNR={genres[0]}", str(file_path)]
            run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_multiple_composers(file_path: Path, composers: List[str]):
        # For now, just set the first composer
        if composers:
            command = ["bwfmetaedit", f"--ICMP={composers[0]}", str(file_path)]
            run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_multiple_album_artists(file_path: Path, album_artists: List[str]):
        # For now, just set the first album artist
        if album_artists:
            command = ["bwfmetaedit", f"--IAAR={album_artists[0]}", str(file_path)]
            run_external_tool(command, "bwfmetaedit")
    
    @staticmethod
    def set_multiple_comments(file_path: Path, comments: List[str]):
        # For now, just set the first comment
        if comments:
            command = ["bwfmetaedit", f"--ICMT={comments[0]}", str(file_path)]
            run_external_tool(command, "bwfmetaedit")
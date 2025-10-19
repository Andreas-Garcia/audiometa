"""Metaflac external tool wrapper for FLAC metadata operations."""

import subprocess
from pathlib import Path
from typing import Dict, Any, List

from ..id3v2.mid3v2_tool import ExternalMetadataToolError


class MetaflacTool:
    """Wrapper for metaflac external tool operations."""
    
    @staticmethod
    def run_command(command: List[str]) -> subprocess.CompletedProcess:
        """Run a metaflac command with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise ExternalMetadataToolError(f"metaflac failed: {e}") from e
    
    @staticmethod
    def set_flac_metadata(file_path: Path, metadata: Dict[str, Any]) -> None:
        """Set FLAC metadata using metaflac tool."""
        cmd = ["metaflac"]
        
        # Map common metadata keys to metaflac arguments
        key_mapping = {
            'title': 'TITLE',
            'artist': 'ARTIST',
            'album': 'ALBUM',
            'date': 'DATE',
            'genre': 'GENRE',
            'comment': 'COMMENT',
            'tracknumber': 'TRACKNUMBER'
        }
        
        for key, value in metadata.items():
            if key.lower() in key_mapping:
                cmd.extend([f"--set-tag={key_mapping[key.lower()]}={value}"])
        
        cmd.append(str(file_path))
        MetaflacTool.run_command(cmd)
    
    @staticmethod
    def set_multiple_tags(file_path: Path, tag_name: str, values: List[str]) -> None:
        """Set multiple Vorbis comment tags with the same name."""
        # First remove existing tags
        try:
            command = ["metaflac", "--remove-tag", tag_name, str(file_path)]
            MetaflacTool.run_command(command)
        except ExternalMetadataToolError:
            # Ignore if tags don't exist
            pass
        
        # Add each value as a separate tag
        for value in values:
            command = ["metaflac", "--set-tag", f"{tag_name}={value}", str(file_path)]
            MetaflacTool.run_command(command)
    
    @staticmethod
    def delete_tag(file_path: Path, tag_name: str) -> None:
        """Delete a specific Vorbis comment tag using metaflac tool."""
        command = ["metaflac", "--remove-tag", tag_name, str(file_path)]
        try:
            MetaflacTool.run_command(command)
        except ExternalMetadataToolError:
            # Ignore if tag doesn't exist
            pass
    
    @staticmethod
    def get_metadata_info(file_path: Path) -> str:
        """Get metadata info using metaflac --list command."""
        command = ["metaflac", "--list", str(file_path)]
        result = MetaflacTool.run_command(command)
        return result.stdout
    
    @staticmethod
    def set_genre(file_path: Path, genre_text: str) -> None:
        """Set Vorbis genre using metaflac tool."""
        command = ["metaflac", "--set-tag", f"GENRE={genre_text}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        """Set Vorbis comment using metaflac tool."""
        command = ["metaflac", "--set-tag", f"COMMENT={comment}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        """Set Vorbis title using metaflac tool."""
        command = ["metaflac", "--set-tag", f"TITLE={title}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        """Set Vorbis artist using metaflac tool."""
        command = ["metaflac", "--set-tag", f"ARTIST={artist}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        """Set Vorbis album using metaflac tool."""
        command = ["metaflac", "--set-tag", f"ALBUM={album}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        """Set Vorbis lyrics using metaflac tool."""
        command = ["metaflac", "--set-tag", f"LYRICS={lyrics}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        """Set Vorbis language using metaflac tool."""
        command = ["metaflac", "--set-tag", f"LANGUAGE={language}", str(file_path)]
        MetaflacTool.run_command(command)
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        """Set Vorbis BPM using metaflac tool."""
        command = ["metaflac", "--set-tag", f"BPM={bpm}", str(file_path)]
        MetaflacTool.run_command(command)
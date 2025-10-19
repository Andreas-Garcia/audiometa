"""Consolidated temporary file with metadata utilities for testing.

This module provides a unified TempFileWithMetadata class that combines
file management, external tool operations, and metadata verification
in a single, clean API.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List

from .id3v2 import Mid3v2Tool, Id3v2Tool, ID3v2MetadataVerifier, ID3v2MultipleMetadataManager, ID3v2SeparatorMetadataManager
from .vorbis import MetaflacTool, VorbisMetadataVerifier, VorbisMultipleMetadataManager
from .riff import BwfmetaeditTool, RIFFMetadataVerifier, RIFFMultipleMetadataManager, RIFFSeparatorMetadataManager
from .common import AudioFileCreator, ScriptRunner, MetadataHeaderVerifier, ComprehensiveMetadataVerifier


class TempFileWithMetadata:
    """Context manager for test files with comprehensive metadata operations.
    
    This class provides a unified interface for:
    - Creating temporary test files with metadata
    - Performing external tool operations
    - Verifying metadata and headers
    - Automatic cleanup
    
    Example:
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Set additional metadata using external tools
            test_file.set_id3v1_genre("17")
            test_file.set_id3v2_genre("Rock")
            
            # Verify headers
            assert test_file.has_id3v2_header()
            
            # Use test_file.path for testing
            metadata = get_merged_unified_metadata(test_file.path)
    """
    
    def __init__(self, metadata: dict, format_type: str):
        """Initialize the context manager.
        
        Args:
            metadata: Dictionary of metadata to set on the test file
            format_type: Audio format ('mp3', 'id3v1', 'id3v2.3', 'id3v2.4', 'flac', 'wav')
        """
        self.metadata = metadata
        self.format_type = format_type
        self.test_file = None
    
    @property
    def path(self) -> Path:
        """Get the path to the test file.
        
        Returns:
            Path to the test file
        """
        if not self.test_file:
            raise RuntimeError("Test file not created yet. Use within context manager.")
        return self.test_file
    
    def __enter__(self):
        """Create the test file and return the manager instance.
        
        Returns:
            The TempFileWithMetadata instance for method access
        """
        self.test_file = self._create_test_file_with_metadata(self.metadata, self.format_type)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test file when exiting the context.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if self.test_file and self.test_file.exists():
            self.test_file.unlink()
    
    # =============================================================================
    # File Creation and Metadata Setting (consolidated from internal_helpers)
    # =============================================================================
    
    def _create_test_file_with_metadata(self, metadata: dict, format_type: str) -> Path:
        """Create a test file with specific metadata values.
        
        This function uses external tools to set specific metadata values
        without using the app's update functions, improving test isolation.
        
        Args:
            metadata: Dictionary of metadata to set
            format_type: Audio format ('mp3', 'id3v1', 'flac', 'wav')
            
        Returns:
            Path to the created file with metadata
        """
        # Create temporary file with correct extension
        # For id3v1, id3v2.3, id3v2.4, use .mp3 extension since they're still MP3 files
        if format_type.lower() in ['id3v1', 'id3v2.3', 'id3v2.4']:
            actual_extension = 'mp3'
        else:
            actual_extension = format_type.lower()
        with tempfile.NamedTemporaryFile(suffix=f'.{actual_extension}', delete=False) as tmp_file:
            target_file = Path(tmp_file.name)
        
        # Create minimal audio file based on format
        self._create_minimal_audio_file(target_file, format_type)
        
        # Use appropriate external tool based on format
        if format_type.lower() == 'mp3':
            # Use mid3v2 for MP3 files
            self._set_mp3_metadata_with_mid3v2(target_file, metadata)
        elif format_type.lower() == 'id3v1':
            # Use id3v2 --id3v1-only for ID3v1 metadata
            self._set_mp3_metadata_with_id3v1(target_file, metadata)
        elif format_type.lower() in ['id3v2.3', 'id3v2.4']:
            # Use mid3v2 for ID3v2.3 and ID3v2.4 metadata
            self._set_mp3_metadata_with_mid3v2(target_file, metadata)
        elif format_type.lower() == 'flac':
            # Use metaflac for FLAC files
            self._set_flac_metadata_with_metaflac(target_file, metadata)
        elif format_type.lower() == 'wav':
            # Use bwfmetaedit for WAV files
            self._set_wav_metadata_with_bwfmetaedit(target_file, metadata)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
        
        return target_file
    
    def _set_mp3_metadata_with_mid3v2(self, file_path: Path, metadata: dict) -> None:
        """Set MP3 metadata using mid3v2 tool."""
        Mid3v2Tool.set_mp3_metadata(file_path, metadata)
    
    def _set_mp3_metadata_with_id3v1(self, file_path: Path, metadata: dict) -> None:
        """Set MP3 metadata using id3v2 tool with --id3v1-only flag."""
        Id3v2Tool.set_id3v1_metadata(file_path, metadata)
    
    def _set_flac_metadata_with_metaflac(self, file_path: Path, metadata: dict) -> None:
        """Set FLAC metadata using metaflac tool."""
        MetaflacTool.set_flac_metadata(file_path, metadata)
    
    def _set_wav_metadata_with_bwfmetaedit(self, file_path: Path, metadata: dict) -> None:
        """Set WAV metadata using bwfmetaedit tool."""
        BwfmetaeditTool.set_wav_metadata(file_path, metadata)
    
    def _create_minimal_audio_file(self, file_path: Path, format_type: str) -> None:
        """Create a minimal audio file for testing."""
        test_files_dir = Path(__file__).parent.parent.parent / "test" / "data" / "audio_files"
        AudioFileCreator.create_minimal_audio_file(file_path, format_type, test_files_dir)
    
    def _get_scripts_dir(self) -> Path:
        """Get the scripts directory path."""
        return Path(__file__).parent.parent.parent / "test" / "data" / "scripts"
    
    def _run_script(self, script_name: str, check: bool = True) -> subprocess.CompletedProcess:
        """Run an external script with proper error handling."""
        scripts_dir = self._get_scripts_dir()
        script_runner = ScriptRunner(scripts_dir)
        return script_runner.run_script(script_name, self.test_file)
    
    def _run_external_tool(self, command: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run an external tool with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"External tool failed: {e}") from e
    
    def _create_multiple_id3v2_frames(self, frame_id: str, texts: list[str]) -> None:
        """Create multiple separate ID3v2 frames using manual binary construction.
        
        This uses the ManualID3v2FrameCreator to bypass standard tools that 
        consolidate multiple frames of the same type, allowing creation of 
        truly separate frames for testing purposes.
        
        Args:
            frame_id: The ID3v2 frame identifier (e.g., 'TPE1', 'TPE2', 'TCON', 'TCOM')
            texts: List of text values, one per frame
        """
        from .id3v2 import ManualID3v2FrameCreator
        
        creator = ManualID3v2FrameCreator(self.test_file)
        
        # Create frames based on the frame type
        if frame_id == 'TPE1':
            creator.create_multiple_tpe1_frames(texts)
        elif frame_id == 'TPE2':
            creator.create_multiple_tpe2_frames(texts)
        elif frame_id == 'TCON':
            creator.create_multiple_tcon_frames(texts)
        elif frame_id == 'TCOM':
            creator.create_multiple_tcom_frames(texts)
        else:
            # Generic frame creation for other frame types
            frames = []
            for text in texts:
                frame_data = creator._create_text_frame(frame_id, text)
                frames.append(frame_data)
            creator._write_id3v2_tag(frames)
    
    # =============================================================================
    # ID3v1 Format Operations
    # =============================================================================
    
    def set_id3v1_genre(self, genre_code: str):
        """Set ID3v1 genre using external id3v2 tool."""
        command = [
            "id3v2", "--id3v1-only", 
            f"--genre={genre_code}",
            str(self.test_file)
        ]
        return self._run_external_tool(command)
    
    def set_id3v1_max_metadata(self):
        """Set maximum ID3v1 metadata using external script."""
        return self._run_script("set-id3v1-max-metadata.sh")
    
    def remove_id3v1_metadata(self):
        """Remove ID3v1 metadata using external script."""
        return self._run_script("remove_id3.py")
    
    # =============================================================================
    # ID3v2 Format Operations
    # =============================================================================
    
    def set_id3v2_genre(self, genre: str):
        """Set ID3v2 genre using external mid3v2 tool."""
        command = ["mid3v2", "--genre", genre, str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_multiple_genres(self, genres: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple genres using external mid3v2 tool or manual frame creation."""
        manager = ID3v2MultipleMetadataManager(self.test_file)
        manager.set_multiple_genres(genres, in_separate_frames)
    
    def set_id3v2_multiple_artists(self, artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple artists using external mid3v2 tool or manual frame creation."""
        manager = ID3v2MultipleMetadataManager(self.test_file)
        manager.set_multiple_artists(artists, in_separate_frames)
    
    def set_id3v2_3_multiple_artists(self, artists: list[str]):
        """Set ID3v2.3 multiple artists using external mid3v2 tool."""
        # Try to delete existing TPE1 tags, but don't fail if they don't exist
        try:
            command = ["mid3v2", "--delete", "TPE1", str(self.test_file)]
            self._run_external_tool(command)
        except RuntimeError:
            # Ignore if TPE1 tags don't exist
            pass
        
        # Set all artists in a single command
        command = ["mid3v2"]
        for artist in artists:
            command.extend(["--TPE1", artist])
        command.append(str(self.test_file))
        self._run_external_tool(command)
    
    def set_id3v2_4_multiple_artists(self, artists: list[str]):
        """Set ID3v2.4 multiple artists using external mid3v2 tool."""
        # Try to delete existing TPE1 tags, but don't fail if they don't exist
        try:
            command = ["mid3v2", "--delete", "TPE1", str(self.test_file)]
            self._run_external_tool(command)
        except RuntimeError:
            # Ignore if TPE1 tags don't exist
            pass
        
        # Set all artists in a single command
        command = ["mid3v2"]
        for artist in artists:
            command.extend(["--TPE1", artist])
        command.append(str(self.test_file))
        self._run_external_tool(command)
        
    def set_id3v2_4_single_artist(self, artist: str):
        """Set ID3v2.4 single artist using external mid3v2 tool."""
        # Try to delete existing TPE1 tags, but don't fail if they don't exist
        try:
            command = ["mid3v2", "--delete", "TPE1", str(self.test_file)]
            self._run_external_tool(command)
        except RuntimeError:
            # Ignore if TPE1 tags don't exist
            pass
        
        command = ["mid3v2"]
        command.extend(["--TPE1", artist])
        command.append(str(self.test_file))
        self._run_external_tool(command)
        
    def get_id3v2_4_all_raw_data(self) -> str:
        """Get all raw data from ID3v2.4 using external mid3v2 tool."""
        command = ["mid3v2", "--list", str(self.test_file)]
        return self._run_external_tool(command).stdout
    
    def set_id3v2_multiple_album_artists(self, album_artists: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple album artists using external mid3v2 tool or manual frame creation."""
        manager = ID3v2MultipleMetadataManager(self.test_file)
        manager.set_multiple_album_artists(album_artists, in_separate_frames)
    
    def set_id3v2_multiple_composers(self, composers: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple composers using external mid3v2 tool or manual frame creation."""
        manager = ID3v2MultipleMetadataManager(self.test_file)
        manager.set_multiple_composers(composers, in_separate_frames)
    
    def set_id3v2_max_metadata(self):
        """Set maximum ID3v2 metadata using external script."""
        return self._run_script("set-id3v2-max-metadata.sh")
    
    def set_id3v2_3_max_metadata(self):
        """Set maximum ID3v2.3 metadata using external script."""
        return self._run_script("set-id3v2-max-metadata.sh")
    
    def set_id3v2_4_max_metadata(self):
        """Set maximum ID3v2.4 metadata using external script."""
        return self._run_script("set-id3v2-max-metadata.sh")
    
    def remove_id3v2_metadata(self):
        """Remove ID3v2 metadata using external script."""
        return self._run_script("remove_id3.py")
    
    # =============================================================================
    # Vorbis Format Operations
    # =============================================================================
    
    def set_vorbis_max_metadata(self):
        """Set maximum Vorbis metadata using external script."""
        return self._run_script("set-vorbis-max-metadata.sh")
    
    def set_vorbis_artists_one_two_three(self):
        """Set specific artists metadata using external script."""
        return self._run_script("set-artists-One-Two-Three-vorbis.sh")
    
    def set_vorbis_genre(self, genre_text: str):
        """Set Vorbis genre using external metaflac tool."""
        command = [
            "metaflac", "--set-tag", f"GENRE={genre_text}",
            str(self.test_file)
        ]
        return self._run_external_tool(command)
    
    # =============================================================================
    # RIFF Format Operations
    # =============================================================================
    
    def set_riff_max_metadata(self):
        """Set maximum RIFF metadata using external script."""
        return self._run_script("set-riff-max-metadata.sh")
    
    def set_riff_genre_text(self, genre_text: str):
        """Set RIFF genre using external exiftool or bwfmetaedit tool."""
        try:
            # Try exiftool first
            command = [
                "exiftool", "-overwrite_original", 
                f"-Genre={genre_text}",
                str(self.test_file)
            ]
            return self._run_external_tool(command)
        except RuntimeError:
            try:
                # Fallback to bwfmetaedit
                command = [
                    "bwfmetaedit", f"--IGNR={genre_text}", str(self.test_file)
                ]
                return self._run_external_tool(command)
            except RuntimeError as e:
                raise RuntimeError(f"Failed to set RIFF genre: {e}") from e
    
    def remove_riff_metadata(self):
        """Remove RIFF metadata using external script."""
        return self._run_script("remove_riff.py")
    
    # =============================================================================
    # Individual Metadata Field Operations
    # =============================================================================
    
    def set_id3v2_comment(self, comment: str):
        """Set ID3v2 comment using external mid3v2 tool."""
        command = ["mid3v2", "--comment", comment, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_comment(self):
        """Delete ID3v2 comment using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "COMM", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v1_comment(self, comment: str):
        """Set ID3v1 comment using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--comment", comment, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v1_comment(self):
        """Delete ID3v1 comment using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--delete", "COMM", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_comment(self, comment: str):
        """Set RIFF comment using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--ICMT={comment}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_comment(self):
        """Delete RIFF comment using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/ICMT", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_comment(self, comment: str):
        """Set Vorbis comment using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"COMMENT={comment}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_comment(self):
        """Delete Vorbis comment using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "COMMENT", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_title(self, title: str):
        """Set ID3v2 title using external id3v2 tool with --id3v2-only flag."""
        command = ["id3v2", "--id3v2-only", "--song", title, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_title(self):
        """Delete ID3v2 title using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "TIT2", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v1_title(self, title: str):
        """Set ID3v1 title using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--song", title, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v1_title(self):
        """Delete ID3v1 title using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--delete", "TIT2", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_title(self, title: str):
        """Set RIFF title using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--INAM={title}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_title(self):
        """Delete RIFF title using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/INAM", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_title(self, title: str):
        """Set Vorbis title using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"TITLE={title}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_title(self):
        """Delete Vorbis title using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "TITLE", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_artist(self, artist: str):
        """Set ID3v2 artist using external id3v2 tool with --id3v2-only flag."""
        command = ["id3v2", "--id3v2-only", "--artist", artist, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_artist(self):
        """Delete ID3v2 artist using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "TPE1", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v1_artist(self, artist: str):
        """Set ID3v1 artist using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--artist", artist, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v1_artist(self):
        """Delete ID3v1 artist using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--delete", "TPE1", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_artist(self, artist: str):
        """Set RIFF artist using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--IART={artist}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_artist(self):
        """Delete RIFF artist using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/IART", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_artist(self, artist: str):
        """Set Vorbis artist using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"ARTIST={artist}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_artist(self):
        """Delete Vorbis artist using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "ARTIST", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_album(self, album: str):
        """Set ID3v2 album using external mid3v2 tool."""
        command = ["mid3v2", "--album", album, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_album(self):
        """Delete ID3v2 album using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "TALB", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v1_album(self, album: str):
        """Set ID3v1 album using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--album", album, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v1_album(self):
        """Delete ID3v1 album using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--delete", "TALB", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_album(self, album: str):
        """Set RIFF album using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--IPRD={album}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_album(self):
        """Delete RIFF album using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/IPRD", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_album(self, album: str):
        """Set Vorbis album using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"ALBUM={album}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_album(self):
        """Delete Vorbis album using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "ALBUM", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_genre(self, genre: str):
        """Set ID3v2 genre using external mid3v2 tool."""
        command = ["mid3v2", "--genre", genre, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_genre(self):
        """Delete ID3v2 genre using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "TCON", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v1_genre(self, genre: str):
        """Set ID3v1 genre using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--genre", genre, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v1_genre(self):
        """Delete ID3v1 genre using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--delete", "TCON", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_genre(self, genre: str):
        """Set RIFF genre using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--IGNR={genre}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_genre(self):
        """Delete RIFF genre using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/IGNR", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_genre(self, genre: str):
        """Set Vorbis genre using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"GENRE={genre}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_multiple_artists(self, artists: List[str]):
        """Set Vorbis multiple artists using external metaflac tool."""
        manager = VorbisMultipleMetadataManager(self.test_file)
        manager.set_multiple_artists(artists)
    
    def set_vorbis_multiple_album_artists(self, album_artists: List[str]):
        """Set Vorbis multiple album artists using external metaflac tool."""
        manager = VorbisMultipleMetadataManager(self.test_file)
        manager.set_multiple_album_artists(album_artists)
    
    def set_vorbis_multiple_composers(self, composers: List[str]):
        """Set Vorbis multiple composers using external metaflac tool."""
        manager = VorbisMultipleMetadataManager(self.test_file)
        manager.set_multiple_composers(composers)
    
    def set_vorbis_multiple_genres(self, genres: List[str]):
        """Set Vorbis multiple genres using external metaflac tool."""
        manager = VorbisMultipleMetadataManager(self.test_file)
        manager.set_multiple_genres(genres)
    
    def set_vorbis_multiple_performers(self, performers: List[str]):
        """Set Vorbis multiple performers using external metaflac tool."""
        manager = VorbisMultipleMetadataManager(self.test_file)
        manager.set_multiple_performers(performers)
    
    def set_vorbis_multiple_comments(self, comments: List[str]):
        """Set Vorbis multiple comments using external metaflac tool."""
        manager = VorbisMultipleMetadataManager(self.test_file)
        manager.set_multiple_comments(comments)
    
    def delete_vorbis_genre(self):
        """Delete Vorbis genre using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "GENRE", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_lyrics(self, lyrics: str):
        """Set ID3v2 lyrics using external mid3v2 tool."""
        command = ["mid3v2", "--USLT", f"eng:{lyrics}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_lyrics(self):
        """Delete ID3v2 lyrics using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "USLT", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v1_lyrics(self, lyrics: str):
        """Set ID3v1 lyrics using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--USLT", f"eng:{lyrics}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v1_lyrics(self):
        """Delete ID3v1 lyrics using external id3v2 tool."""
        command = ["id3v2", "--id3v1-only", "--delete", "USLT", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_lyrics(self, lyrics: str):
        """Set RIFF lyrics using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--ILYT={lyrics}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_lyrics(self):
        """Delete RIFF lyrics using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/ILYT", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_lyrics(self, lyrics: str):
        """Set Vorbis lyrics using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"LYRICS={lyrics}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_lyrics(self):
        """Delete Vorbis lyrics using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "LYRICS", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_language(self, language: str):
        """Set ID3v2 language using external mid3v2 tool."""
        command = ["mid3v2", "--TLAN", language, str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_language(self):
        """Delete ID3v2 language using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "TLAN", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_riff_language(self, language: str):
        """Set RIFF language using external bwfmetaedit tool."""
        command = ["bwfmetaedit", f"--ILNG={language}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_riff_language(self):
        """Delete RIFF language using external bwfmetaedit tool."""
        command = ["bwfmetaedit", "--remove-chunks=INFO/ILNG", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_language(self, language: str):
        """Set Vorbis language using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"LANGUAGE={language}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_language(self):
        """Delete Vorbis language using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "LANGUAGE", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_bpm(self, bpm: int):
        """Set ID3v2 BPM using external mid3v2 tool."""
        command = ["mid3v2", "--TBPM", str(bpm), str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_id3v2_bpm(self):
        """Delete ID3v2 BPM using external mid3v2 tool."""
        command = ["mid3v2", "--delete", "TBPM", str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_vorbis_bpm(self, bpm: int):
        """Set Vorbis BPM using external metaflac tool."""
        command = ["metaflac", "--set-tag", f"BPM={bpm}", str(self.test_file)]
        return self._run_external_tool(command)
    
    def delete_vorbis_bpm(self):
        """Delete Vorbis BPM using external metaflac tool."""
        command = ["metaflac", "--remove-tag", "BPM", str(self.test_file)]
        return self._run_external_tool(command)

    def has_id3v2_header(self) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes."""
        if not self.test_file:
            return False
        return MetadataHeaderVerifier.has_id3v2_header(self.test_file)
    
    def has_id3v1_header(self) -> bool:
        """Check if file has ID3v1 header by reading the last 128 bytes."""
        if not self.test_file:
            return False
        return MetadataHeaderVerifier.has_id3v1_header(self.test_file)
    
    def has_vorbis_comments(self) -> bool:
        """Check if file has Vorbis comments using metaflac."""
        if not self.test_file:
            return False
        return MetadataHeaderVerifier.has_vorbis_comments(self.test_file)
    
    def has_riff_info_chunk(self) -> bool:
        """Check if file has RIFF INFO chunk by reading file structure."""
        if not self.test_file:
            return False
        return MetadataHeaderVerifier.has_riff_info_chunk(self.test_file)
    
    def get_metadata_headers_present(self) -> Dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file."""
        if not self.test_file:
            return {}
        return MetadataHeaderVerifier.get_metadata_headers_present(self.test_file)
    
    def verify_headers_removed(self, expected_removed: List[str] = None) -> Dict[str, bool]:
        """Verify that specified metadata headers have been removed."""
        if not self.test_file:
            return {}
        return ComprehensiveMetadataVerifier.verify_headers_removed(self.test_file, expected_removed)
    
    def check_metadata_with_external_tools(self) -> Dict[str, Any]:
        """Check metadata using external tools for comprehensive verification."""
        if not self.test_file:
            return {}
        return ComprehensiveMetadataVerifier.check_metadata_with_external_tools(self.test_file)
    
    def verify_id3v2_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw ID3v2 data using external tools."""
        if not self.test_file:
            return {'success': False, 'error': 'No test file available'}
        return ID3v2MetadataVerifier.verify_multiple_entries_in_raw_data(self.test_file, tag_name, expected_count)
    
    def verify_id3v2_4_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw ID3v2.4 data using external tools.
        
        This method is kept for backward compatibility but delegates to the general method.
        """
        return self.verify_id3v2_multiple_entries_in_raw_data(tag_name, expected_count)
            
    def verify_vorbis_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw Vorbis comments using external tools."""
        if not self.test_file:
            return {'success': False, 'error': 'No test file available'}
        return VorbisMetadataVerifier.verify_multiple_entries_in_raw_data(self.test_file, tag_name, expected_count)
    
    def verify_riff_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw RIFF data using external tools."""
        if not self.test_file:
            return {'success': False, 'error': 'No test file available'}
        return RIFFMetadataVerifier.verify_multiple_entries_in_raw_data(self.test_file, tag_name, expected_count)
    
    # =============================================================================
    # Separator-based metadata methods (for testing single-field separator parsing)
    # =============================================================================
    
    def set_id3v2_separator_artists(self, artists_string: str, version: str = "2.3"):
        """Set ID3v2 artists as a single field with separators using external tool."""
        manager = ID3v2SeparatorMetadataManager(self.test_file)
        manager.set_separator_artists(artists_string, version)
    
    def set_id3v2_separator_genres(self, genres_string: str, version: str = "2.3"):
        """Set ID3v2 genres as a single field with separators using external tool."""
        manager = ID3v2SeparatorMetadataManager(self.test_file)
        manager.set_separator_genres(genres_string, version)
    
    def set_id3v2_separator_composers(self, composers_string: str, version: str = "2.3"):
        """Set ID3v2 composers as a single field with separators using external tool."""
        manager = ID3v2SeparatorMetadataManager(self.test_file)
        manager.set_separator_composers(composers_string, version)
    
    def set_riff_separator_artists(self, artists_string: str):
        """Set RIFF artists as a single field with separators using external tool."""
        manager = RIFFSeparatorMetadataManager(self.test_file)
        manager.set_separator_artists(artists_string)
    
    def set_riff_separator_genres(self, genres_string: str):
        """Set RIFF genres as a single field with separators using external tool."""
        manager = RIFFSeparatorMetadataManager(self.test_file)
        manager.set_separator_genres(genres_string)
    
    def set_riff_separator_composers(self, composers_string: str):
        """Set RIFF composers as a single field with separators using external tool."""
        manager = RIFFSeparatorMetadataManager(self.test_file)
        manager.set_separator_composers(composers_string)
    
    def set_riff_separator_album_artists(self, album_artists_string: str):
        """Set RIFF album artists as a single field with separators using external tool."""
        manager = RIFFSeparatorMetadataManager(self.test_file)
        manager.set_separator_album_artists(album_artists_string)
    
    def set_riff_multiple_artists(self, artists: List[str]):
        """Set RIFF multiple artists using external tool (creates multiple chunks)."""
        manager = RIFFMultipleMetadataManager(self.test_file)
        manager.set_multiple_artists(artists)
    
    def set_riff_multiple_genres(self, genres: List[str]):
        """Set RIFF multiple genres using external tool."""
        manager = RIFFMultipleMetadataManager(self.test_file)
        manager.set_multiple_genres(genres)
    
    def set_riff_multiple_composers(self, composers: List[str]):
        """Set RIFF multiple composers using external tool."""
        manager = RIFFMultipleMetadataManager(self.test_file)
        manager.set_multiple_composers(composers)
    
    def set_riff_multiple_album_artists(self, album_artists: List[str]):
        """Set RIFF multiple album artists using external tool."""
        manager = RIFFMultipleMetadataManager(self.test_file)
        manager.set_multiple_album_artists(album_artists)
    
    def set_riff_multiple_comments(self, comments: List[str]):
        """Set RIFF multiple comments using external tool."""
        manager = RIFFMultipleMetadataManager(self.test_file)
        manager.set_multiple_comments(comments)
    
    def set_id3v2_multiple_comments(self, comments: List[str], in_separate_frames: bool = False):
        """Set ID3v2 multiple comments using external mid3v2 tool."""
        manager = ID3v2MultipleMetadataManager(self.test_file)
        manager.set_multiple_comments(comments, in_separate_frames)

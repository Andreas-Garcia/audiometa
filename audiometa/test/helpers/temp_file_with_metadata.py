"""Consolidated temporary file with metadata utilities for testing.

This module provides a unified TempFileWithMetadata class that combines
file management, external tool operations, and metadata verification
in a single, clean API.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from .id3v2 import Mid3v2Tool, Id3v2Tool, ID3v2MetadataVerifier, ID3v2MultipleMetadataManager, ID3v2SeparatorMetadataManager, ID3HeaderVerifier, ID3v2MetadataDeleter, ID3v1MetadataDeleter, ID3v2MetadataSetter, ID3v1MetadataSetter
from .vorbis import MetaflacTool, VorbisMetadataVerifier, VorbisMultipleMetadataManager, VorbisHeaderVerifier, VorbisMetadataDeleter, VorbisMetadataSetter
from .riff import BwfmetaeditTool, RIFFMetadataVerifier, RIFFMultipleMetadataManager, RIFFSeparatorMetadataManager, RIFFHeaderVerifier, RIFFMetadataDeleter, RIFFMetadataSetter
from .common import AudioFileCreator, ScriptRunner, ComprehensiveMetadataVerifier


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
    # File Creation and Metadata Setting
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
        Mid3v2Tool.set_mp3_metadata(file_path, metadata)
    
    def _set_mp3_metadata_with_id3v1(self, file_path: Path, metadata: dict) -> None:
        Id3v2Tool.set_id3v1_metadata(file_path, metadata)
    
    def _set_flac_metadata_with_metaflac(self, file_path: Path, metadata: dict) -> None:
        MetaflacTool.set_flac_metadata(file_path, metadata)
    
    def _set_wav_metadata_with_bwfmetaedit(self, file_path: Path, metadata: dict) -> None:
        BwfmetaeditTool.set_wav_metadata(file_path, metadata)
    
    def _create_minimal_audio_file(self, file_path: Path, format_type: str) -> None:
        test_files_dir = Path(__file__).parent.parent.parent / "test" / "data" / "audio_files"
        AudioFileCreator.create_minimal_audio_file(file_path, format_type, test_files_dir)
    
    def _get_scripts_dir(self) -> Path:
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
        ID3v2MultipleMetadataManager._create_multiple_id3v2_frames(self.test_file, frame_id, texts)
    
    # =============================================================================
    # ID3v1 Format Operations
    # =============================================================================
    
    def set_id3v1_genre(self, genre_code: str):
        ID3v1MetadataSetter.set_genre(self.test_file, genre_code)
    
    def set_id3v1_max_metadata(self):
        ID3v1MetadataSetter.set_max_metadata(self.test_file)
    
    def remove_id3v1_metadata(self):
        return self._run_script("remove_id3.py")
    
    # =============================================================================
    # ID3v2 Format Operations
    # =============================================================================
    
    def set_id3v2_genre(self, genre: str):
        ID3v2MetadataSetter.set_genre(self.test_file, genre)
    
    def set_id3v2_multiple_genres(self, genres: List[str], in_separate_frames: bool = False):
        ID3v2MultipleMetadataManager.set_multiple_genres(self.test_file, genres, in_separate_frames)
    
    def set_id3v2_multiple_artists(self, artists: List[str], in_separate_frames: bool = False):
        ID3v2MultipleMetadataManager.set_multiple_artists(self.test_file, artists, in_separate_frames)
    
    def set_id3v2_3_multiple_artists(self, artists: list[str]):
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
        command = ["mid3v2", "--list", str(self.test_file)]
        return self._run_external_tool(command).stdout
    
    def set_id3v2_multiple_album_artists(self, album_artists: List[str], in_separate_frames: bool = False):
        ID3v2MultipleMetadataManager.set_multiple_album_artists(self.test_file, album_artists, in_separate_frames)
    
    def set_id3v2_multiple_composers(self, composers: List[str], in_separate_frames: bool = False):
        ID3v2MultipleMetadataManager.set_multiple_composers(self.test_file, composers, in_separate_frames)
    
    def set_id3v2_max_metadata(self):
        ID3v2MetadataSetter.set_max_metadata(self.test_file)
    
    def set_id3v2_3_max_metadata(self):
        ID3v2MetadataSetter.set_max_metadata(self.test_file)
    
    def set_id3v2_4_max_metadata(self):
        ID3v2MetadataSetter.set_max_metadata(self.test_file)
    
    def remove_id3v2_metadata(self):
        return self._run_script("remove_id3.py")
    
    # =============================================================================
    # Vorbis Format Operations
    # =============================================================================
    
    def set_vorbis_max_metadata(self):
        VorbisMetadataSetter.set_max_metadata(self.test_file)
    
    def set_vorbis_artists_one_two_three(self):
        VorbisMetadataSetter.set_artists_one_two_three(self.test_file)
    
    def set_vorbis_genre(self, genre_text: str):
        VorbisMetadataSetter.set_genre(self.test_file, genre_text)
    
    # =============================================================================
    # RIFF Format Operations
    # =============================================================================
    
    def set_riff_max_metadata(self):
        RIFFMetadataSetter.set_max_metadata(self.test_file)
    
    def set_riff_genre_text(self, genre_text: str):
        RIFFMetadataSetter.set_genre_text(self.test_file, genre_text)
    
    def remove_riff_metadata(self):
        return self._run_script("remove_riff.py")
    
    # =============================================================================
    # Individual Metadata Field Operations
    # =============================================================================
    
    def set_id3v2_comment(self, comment: str):
        ID3v2MetadataSetter.set_comment(self.test_file, comment)
    
    def delete_id3v2_comment(self):
        ID3v2MetadataDeleter.delete_comment(self.test_file)
    
    def set_id3v1_comment(self, comment: str):
        ID3v1MetadataSetter.set_comment(self.test_file, comment)
    
    def delete_id3v1_comment(self):
        ID3v1MetadataDeleter.delete_comment(self.test_file)
    
    def set_riff_comment(self, comment: str):
        RIFFMetadataSetter.set_comment(self.test_file, comment)
    
    def delete_riff_comment(self):
        RIFFMetadataDeleter.delete_comment(self.test_file)
    
    def set_vorbis_comment(self, comment: str):
        VorbisMetadataSetter.set_comment(self.test_file, comment)
    
    def delete_vorbis_comment(self):
        VorbisMetadataDeleter.delete_comment(self.test_file)
    
    def set_id3v2_title(self, title: str):
        ID3v2MetadataSetter.set_title(self.test_file, title)
    
    def delete_id3v2_title(self):
        ID3v2MetadataDeleter.delete_title(self.test_file)
    
    def set_id3v1_title(self, title: str):
        ID3v1MetadataSetter.set_title(self.test_file, title)
    
    def delete_id3v1_title(self):
        ID3v1MetadataDeleter.delete_title(self.test_file)
    
    def set_riff_title(self, title: str):
        RIFFMetadataSetter.set_title(self.test_file, title)
    
    def delete_riff_title(self):
        RIFFMetadataDeleter.delete_title(self.test_file)
    
    def set_vorbis_title(self, title: str):
        VorbisMetadataSetter.set_title(self.test_file, title)
    
    def delete_vorbis_title(self):
        VorbisMetadataDeleter.delete_title(self.test_file)
    
    def set_id3v2_artist(self, artist: str):
        ID3v2MetadataSetter.set_artist(self.test_file, artist)
    
    def delete_id3v2_artist(self):
        ID3v2MetadataDeleter.delete_artist(self.test_file)
    
    def set_id3v1_artist(self, artist: str):
        ID3v1MetadataSetter.set_artist(self.test_file, artist)
    
    def delete_id3v1_artist(self):
        ID3v1MetadataDeleter.delete_artist(self.test_file)
    
    def set_riff_artist(self, artist: str):
        RIFFMetadataSetter.set_artist(self.test_file, artist)
    
    def delete_riff_artist(self):
        RIFFMetadataDeleter.delete_artist(self.test_file)
    
    def set_vorbis_artist(self, artist: str):
        VorbisMetadataSetter.set_artist(self.test_file, artist)
    
    def delete_vorbis_artist(self):
        VorbisMetadataDeleter.delete_artist(self.test_file)
    
    def set_id3v2_album(self, album: str):
        ID3v2MetadataSetter.set_album(self.test_file, album)
    
    def delete_id3v2_album(self):
        ID3v2MetadataDeleter.delete_album(self.test_file)
    
    def set_id3v1_album(self, album: str):
        ID3v1MetadataSetter.set_album(self.test_file, album)
    
    def delete_id3v1_album(self):
        ID3v1MetadataDeleter.delete_album(self.test_file)
    
    def set_riff_album(self, album: str):
        RIFFMetadataSetter.set_album(self.test_file, album)
    
    def delete_riff_album(self):
        RIFFMetadataDeleter.delete_album(self.test_file)
    
    def set_vorbis_album(self, album: str):
        VorbisMetadataSetter.set_album(self.test_file, album)
    
    def delete_vorbis_album(self):
        VorbisMetadataDeleter.delete_album(self.test_file)
    
    def set_id3v2_genre(self, genre: str):
        ID3v2MetadataSetter.set_genre(self.test_file, genre)
    
    def delete_id3v2_genre(self):
        ID3v2MetadataDeleter.delete_genre(self.test_file)
    
    def set_id3v1_genre(self, genre: str):
        ID3v1MetadataSetter.set_genre(self.test_file, genre)
    
    def delete_id3v1_genre(self):
        ID3v1MetadataDeleter.delete_genre(self.test_file)
    
    def set_riff_genre(self, genre: str):
        RIFFMetadataSetter.set_genre(self.test_file, genre)
    
    def delete_riff_genre(self):
        RIFFMetadataDeleter.delete_genre(self.test_file)
    
    def set_vorbis_genre(self, genre: str):
        VorbisMetadataSetter.set_genre(self.test_file, genre)
    
    def set_vorbis_multiple_artists(self, artists: List[str]):
        VorbisMultipleMetadataManager.set_multiple_artists(self.test_file, artists)
    
    def set_vorbis_multiple_album_artists(self, album_artists: List[str]):
        VorbisMultipleMetadataManager.set_multiple_album_artists(self.test_file, album_artists)
    
    def set_vorbis_multiple_composers(self, composers: List[str]):
        VorbisMultipleMetadataManager.set_multiple_composers(self.test_file, composers)
    
    def set_vorbis_multiple_genres(self, genres: List[str]):
        VorbisMultipleMetadataManager.set_multiple_genres(self.test_file, genres)
    
    def set_vorbis_multiple_performers(self, performers: List[str]):
        VorbisMultipleMetadataManager.set_multiple_performers(self.test_file, performers)
    
    def set_vorbis_multiple_comments(self, comments: List[str]):
        VorbisMultipleMetadataManager.set_multiple_comments(self.test_file, comments)
    
    def delete_vorbis_genre(self):
        VorbisMetadataDeleter.delete_genre(self.test_file)
    
    def set_id3v2_lyrics(self, lyrics: str):
        ID3v2MetadataSetter.set_lyrics(self.test_file, lyrics)
    
    def delete_id3v2_lyrics(self):
        ID3v2MetadataDeleter.delete_lyrics(self.test_file)
    
    def set_riff_lyrics(self, lyrics: str):
        RIFFMetadataSetter.set_lyrics(self.test_file, lyrics)
    
    def delete_riff_lyrics(self):
        RIFFMetadataDeleter.delete_lyrics(self.test_file)
    
    def set_vorbis_lyrics(self, lyrics: str):
        VorbisMetadataSetter.set_lyrics(self.test_file, lyrics)
    
    def delete_vorbis_lyrics(self):
        VorbisMetadataDeleter.delete_lyrics(self.test_file)
    
    def set_id3v2_language(self, language: str):
        ID3v2MetadataSetter.set_language(self.test_file, language)
    
    def delete_id3v2_language(self):
        ID3v2MetadataDeleter.delete_language(self.test_file)
    
    def set_riff_language(self, language: str):
        RIFFMetadataSetter.set_language(self.test_file, language)
    
    def delete_riff_language(self):
        RIFFMetadataDeleter.delete_language(self.test_file)
    
    def set_vorbis_language(self, language: str):
        VorbisMetadataSetter.set_language(self.test_file, language)
    
    def delete_vorbis_language(self):
        VorbisMetadataDeleter.delete_language(self.test_file)
    
    def set_id3v2_bpm(self, bpm: int):
        ID3v2MetadataSetter.set_bpm(self.test_file, bpm)
    
    def delete_id3v2_bpm(self):
        ID3v2MetadataDeleter.delete_bpm(self.test_file)
    
    def set_vorbis_bpm(self, bpm: int):
        VorbisMetadataSetter.set_bpm(self.test_file, bpm)
    
    def delete_vorbis_bpm(self):
        VorbisMetadataDeleter.delete_bpm(self.test_file)

    def has_id3v2_header(self) -> bool:
        return ID3HeaderVerifier.has_id3v2_header(self.test_file)
    
    def has_id3v1_header(self) -> bool:
        return ID3HeaderVerifier.has_id3v1_header(self.test_file)
    
    def has_vorbis_comments(self) -> bool:
        return VorbisHeaderVerifier.has_vorbis_comments(self.test_file)
    
    def has_riff_info_chunk(self) -> bool:
        return RIFFHeaderVerifier.has_riff_info_chunk(self.test_file)
    
    def get_metadata_headers_present(self) -> Dict[str, bool]:
        return ComprehensiveMetadataVerifier.get_metadata_headers_present(self.test_file)
    
    def verify_headers_removed(self, expected_removed: List[str] = None) -> Dict[str, bool]:
        return ComprehensiveMetadataVerifier.verify_headers_removed(self.test_file, expected_removed)
    
    def check_metadata_with_external_tools(self) -> Dict[str, Any]:
        return ComprehensiveMetadataVerifier.check_metadata_with_external_tools(self.test_file)
    
    def verify_id3v2_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        return ID3v2MetadataVerifier.verify_multiple_entries_in_raw_data(self.test_file, tag_name, expected_count)
    
    def verify_id3v2_4_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        return self.verify_id3v2_multiple_entries_in_raw_data(tag_name, expected_count)
            
    def verify_vorbis_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        return VorbisMetadataVerifier.verify_multiple_entries_in_raw_data(self.test_file, tag_name, expected_count)
    
    def verify_riff_multiple_entries_in_raw_data(self, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        return RIFFMetadataVerifier.verify_multiple_entries_in_raw_data(self.test_file, tag_name, expected_count)
    
    # =============================================================================
    # Separator-based metadata methods (for testing single-field separator parsing)
    # =============================================================================
    
    def set_id3v2_separator_artists(self, artists_string: str, version: str = "2.3"):
        ID3v2SeparatorMetadataManager.set_separator_artists(self.test_file, artists_string, version)
    
    def set_id3v2_separator_genres(self, genres_string: str, version: str = "2.3"):
        ID3v2SeparatorMetadataManager.set_separator_genres(self.test_file, genres_string, version)
    
    def set_id3v2_separator_composers(self, composers_string: str, version: str = "2.3"):
        ID3v2SeparatorMetadataManager.set_separator_composers(self.test_file, composers_string, version)
    
    def set_riff_separator_artists(self, artists_string: str):
        RIFFSeparatorMetadataManager.set_separator_artists(self.test_file, artists_string)
    
    def set_riff_separator_genres(self, genres_string: str):
        RIFFSeparatorMetadataManager.set_separator_genres(self.test_file, genres_string)
    
    def set_riff_separator_composers(self, composers_string: str):
        RIFFSeparatorMetadataManager.set_separator_composers(self.test_file, composers_string)
    
    def set_riff_separator_album_artists(self, album_artists_string: str):
        RIFFSeparatorMetadataManager.set_separator_album_artists(self.test_file, album_artists_string)
    
    def set_riff_multiple_artists(self, artists: List[str]):
        RIFFMultipleMetadataManager.set_multiple_artists(self.test_file, artists)
    
    def set_riff_multiple_genres(self, genres: List[str]):
        RIFFMultipleMetadataManager.set_multiple_genres(self.test_file, genres)
    
    def set_riff_multiple_composers(self, composers: List[str]):
        RIFFMultipleMetadataManager.set_multiple_composers(self.test_file, composers)
    
    def set_riff_multiple_album_artists(self, album_artists: List[str]):
        RIFFMultipleMetadataManager.set_multiple_album_artists(self.test_file, album_artists)
    
    def set_riff_multiple_comments(self, comments: List[str]):
        RIFFMultipleMetadataManager.set_multiple_comments(self.test_file, comments)
    
    def set_id3v2_multiple_comments(self, comments: List[str], in_separate_frames: bool = False):
        ID3v2MultipleMetadataManager.set_multiple_comments(self.test_file, comments, in_separate_frames)

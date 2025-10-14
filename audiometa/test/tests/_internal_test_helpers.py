"""Internal test helper functions.

This module contains internal helper functions that should not be used directly
in tests. These functions are meant to be used by other test utilities like
TempFileWithMetadata.

WARNING: Do not import these functions directly in test files!
Use TempFileWithMetadata instead for proper test file management.
"""

import tempfile
import subprocess
import shutil
from pathlib import Path


def create_test_file_with_metadata(
    metadata: dict,
    format_type: str,
) -> Path:
    """Create a test file with specific metadata values.
    
    This function uses external tools to set specific metadata values
    without using the app's update functions, improving test isolation.
    
    Args:
        metadata: Dictionary of metadata to set
        format_type: Audio format ('mp3', 'id3v1', 'flac', 'wav')
        
    Returns:
        Path to the created file with metadata
        
    WARNING: This function should not be used directly in tests!
    Use TempFileWithMetadata instead for proper cleanup.
    """
    # Create temporary file with correct extension
    # For id3v1, use .mp3 extension since it's still an MP3 file
    actual_extension = 'mp3' if format_type.lower() == 'id3v1' else format_type.lower()
    with tempfile.NamedTemporaryFile(suffix=f'.{actual_extension}', delete=False) as tmp_file:
        target_file = Path(tmp_file.name)
    
    # Create minimal audio file based on format
    _create_minimal_audio_file(target_file, format_type)
    
    # Use appropriate external tool based on format
    if format_type.lower() == 'mp3':
        # Use mid3v2 for MP3 files
        _set_mp3_metadata_with_mid3v2(target_file, metadata)
    elif format_type.lower() == 'id3v1':
        # Use id3v2 --id3v1-only for ID3v1 metadata
        _set_mp3_metadata_with_id3v1(target_file, metadata)
    elif format_type.lower() == 'flac':
        # Use metaflac for FLAC files
        _set_flac_metadata_with_metaflac(target_file, metadata)
    elif format_type.lower() == 'wav':
        # Use bwfmetaedit for WAV files
        _set_wav_metadata_with_bwfmetaedit(target_file, metadata)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")
    
    return target_file


def _set_mp3_metadata_with_mid3v2(file_path: Path, metadata: dict) -> None:
    """Set MP3 metadata using mid3v2 tool."""
    cmd = ["mid3v2"]
    
    # Map common metadata keys to mid3v2 arguments
    key_mapping = {
        'title': '--song',
        'artist': '--artist', 
        'album': '--album',
        'year': '--year',
        'genre': '--genre',
        'comment': '--comment',
        'track': '--track'
    }
    
    for key, value in metadata.items():
        if key.lower() in key_mapping:
            cmd.extend([key_mapping[key.lower()], str(value)])
    
    cmd.append(str(file_path))
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"mid3v2 failed: {e.stderr}") from e


def _set_mp3_metadata_with_id3v1(file_path: Path, metadata: dict) -> None:
    """Set MP3 metadata using id3v2 tool with --id3v1-only flag."""
    cmd = ["id3v2", "--id3v1-only"]
    
    # Map common metadata keys to id3v2 arguments
    key_mapping = {
        'title': '--song',
        'artist': '--artist', 
        'album': '--album',
        'year': '--year',
        'genre': '--genre',
        'comment': '--comment',
        'track': '--track'
    }
    
    for key, value in metadata.items():
        if key.lower() in key_mapping:
            cmd.extend([key_mapping[key.lower()], str(value)])
    
    cmd.append(str(file_path))
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"id3v2 failed: {e.stderr}") from e


def _set_flac_metadata_with_metaflac(file_path: Path, metadata: dict) -> None:
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
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"metaflac failed: {e.stderr}") from e


def _set_wav_metadata_with_bwfmetaedit(file_path: Path, metadata: dict) -> None:
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
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"bwfmetaedit failed: {e.stderr}") from e


def _create_minimal_audio_file(file_path: Path, format_type: str) -> None:
    """Create a minimal audio file for testing.
    
    Args:
        file_path: Path where to create the file
        format_type: Audio format ('mp3', 'flac', 'wav')
    """
    # Use existing sample files as templates
    test_files_dir = Path(__file__).parent.parent / "data" / "audio_files"
    
    if format_type.lower() in ['mp3', 'id3v1']:
        template_file = test_files_dir / "metadata=none.mp3"
    elif format_type.lower() == 'flac':
        template_file = test_files_dir / "metadata=none.flac"
    elif format_type.lower() == 'wav':
        template_file = test_files_dir / "metadata=none.wav"
    else:
        raise ValueError(f"Unsupported format type: {format_type}")
    
    if not template_file.exists():
        # Fallback: create a minimal file using ffmpeg if available
        try:
            # For id3v1, use mp3 format for ffmpeg
            actual_format = 'mp3' if format_type.lower() == 'id3v1' else format_type.lower()
            _create_minimal_audio_with_ffmpeg(file_path, actual_format)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Last resort: copy from any available sample file
            # For id3v1, look for mp3 files
            search_format = 'mp3' if format_type.lower() == 'id3v1' else format_type.lower()
            sample_files = list(test_files_dir.glob(f"*.{search_format}"))
            if sample_files:
                shutil.copy2(sample_files[0], file_path)
            else:
                raise RuntimeError(f"No template file found for {format_type}")
    else:
        # Copy from template
        shutil.copy2(template_file, file_path)


def _create_minimal_audio_with_ffmpeg(file_path: Path, format_type: str) -> None:
    """Create a minimal audio file using ffmpeg."""
    # Create 1 second of silence
    cmd = [
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=duration=1",
        "-acodec", format_type.lower(), "-y", str(file_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)

"""Helper functions for using external scripts in tests.

This module provides Python functions that call the external scripts
in audiometa/test/data/scripts/ to set up test files with metadata
without using the app's own update functions. This prevents circular
dependencies in tests where writing logic could mask reading bugs.
"""

import subprocess
from pathlib import Path
from typing import Optional


class ScriptHelper:
    
    def __init__(self, scripts_dir: Optional[Path] = None):
        if scripts_dir is None:
            # Default to the scripts directory relative to this file
            self.scripts_dir = Path(__file__).parent.parent / "data" / "scripts"
        else:
            self.scripts_dir = scripts_dir
    
    def _run_script(self, script_name: str, file_path: Path, check: bool = True) -> subprocess.CompletedProcess:
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        if not script_path.is_file():
            raise FileNotFoundError(f"Script is not a file: {script_path}")
        
        # Make script executable
        script_path.chmod(0o755)
        
        try:
            result = subprocess.run(
                [str(script_path), str(file_path)],
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Script {script_name} failed: {e.stderr}") from e
    
    def set_id3v2_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        """Set maximum ID3v2 metadata using external script."""
        return self._run_script("set-id3v2-max-metadata.sh", file_path)
    
    def set_vorbis_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        """Set maximum Vorbis metadata using external script."""
        return self._run_script("set-vorbis-max-metadata.sh", file_path)
    
    def set_riff_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        """Set maximum RIFF metadata using external script."""
        return self._run_script("set-riff-max-metadata.sh", file_path)
    
    def set_id3v1_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        """Set maximum ID3v1 metadata using external script."""
        return self._run_script("set-id3v1-max-metadata.sh", file_path)
    
    def set_artists_one_two_three_vorbis(self, file_path: Path) -> subprocess.CompletedProcess:
        """Set artists 'One Two Three' using Vorbis script."""
        return self._run_script("set-artists-One-Two-Three-vorbis.sh", file_path)
    
    def remove_id3_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        """Remove ID3 metadata using external script."""
        return self._run_script("remove_id3.py", file_path)
    
    def remove_riff_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        """Remove RIFF metadata using external script."""
        return self._run_script("remove_riff.py", file_path)


def create_test_file_with_metadata(
    source_file: Path, 
    target_file: Path, 
    metadata_type: str,
    scripts_dir: Optional[Path] = None
) -> Path:
    """Create a test file with specific metadata using external scripts.
    
    Args:
        source_file: Source audio file to copy
        target_file: Target path for the new file
        metadata_type: Type of metadata to set ('id3v2', 'vorbis', 'riff', 'id3v1')
        scripts_dir: Optional path to scripts directory
        
    Returns:
        Path to the created file with metadata
        
    Raises:
        ValueError: If metadata_type is not supported
        RuntimeError: If script execution fails
    """
    import shutil
    
    # Copy source file to target
    shutil.copy2(source_file, target_file)
    
    # Initialize script helper
    helper = ScriptHelper(scripts_dir)
    
    # Set metadata based on type
    if metadata_type.lower() == 'id3v2':
        helper.set_id3v2_max_metadata(target_file)
    elif metadata_type.lower() == 'vorbis':
        helper.set_vorbis_max_metadata(target_file)
    elif metadata_type.lower() == 'riff':
        helper.set_riff_max_metadata(target_file)
    elif metadata_type.lower() == 'id3v1':
        helper.set_id3v1_max_metadata(target_file)
    else:
        raise ValueError(f"Unsupported metadata type: {metadata_type}")
    
    return target_file


def create_test_file_with_metadata(
    metadata: dict,
    format_type: str,
) -> Path:
    """Create a test file with specific metadata values.
    
    This function uses external tools to set specific metadata values
    without using the app's update functions, preventing circular dependencies.
    
    Args:
        metadata: Dictionary of metadata to set
        format_type: Audio format ('mp3', 'flac', 'wav')
        
    Returns:
        Path to the created file with metadata
    """
    import shutil
    import subprocess
    import tempfile
    
    # Create temporary file with correct extension
    with tempfile.NamedTemporaryFile(suffix=f'.{format_type.lower()}', delete=False) as tmp_file:
        target_file = Path(tmp_file.name)
    
    # Create minimal audio file based on format
    _create_minimal_audio_file(target_file, format_type)
    
    # Use appropriate external tool based on format
    if format_type.lower() == 'mp3':
        # Use mid3v2 for MP3 files
        _set_mp3_metadata_with_mid3v2(target_file, metadata)
    elif format_type.lower() == 'flac':
        # Use metaflac for FLAC files
        _set_flac_metadata_with_metaflac(target_file, metadata)
    elif format_type.lower() == 'wav':
        # Use bwfmetaedit for WAV files
        _set_wav_metadata_with_bwfmetaedit(target_file, metadata)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")
    
    return target_file




def create_test_file_with_specific_metadata(
    source_file: Path,
    target_file: Path,
    metadata: dict,
    format_type: str,
) -> Path:
    """Create a test file with specific metadata values (legacy function).
    
    This function is kept for backward compatibility but is deprecated.
    Use create_test_file_with_metadata() instead.
    """
    import shutil
    
    # Copy source file to target
    shutil.copy2(source_file, target_file)
    
    # Use appropriate external tool based on format
    if format_type.lower() == 'mp3':
        # Use mid3v2 for MP3 files
        _set_mp3_metadata_with_mid3v2(target_file, metadata)
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
    import shutil
    import tempfile
    import subprocess
    
    # Use existing sample files as templates
    test_files_dir = Path(__file__).parent.parent / "data" / "audio_files"
    
    if format_type.lower() == 'mp3':
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
            _create_minimal_audio_with_ffmpeg(file_path, format_type)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Last resort: copy from any available sample file
            sample_files = list(test_files_dir.glob(f"*.{format_type.lower()}"))
            if sample_files:
                shutil.copy2(sample_files[0], file_path)
            else:
                raise RuntimeError(f"No template file found for {format_type}")
    else:
        # Copy from template
        shutil.copy2(template_file, file_path)


def _create_minimal_audio_with_ffmpeg(file_path: Path, format_type: str) -> None:
    """Create a minimal audio file using ffmpeg."""
    import subprocess
    
    # Create 1 second of silence
    cmd = [
        "ffmpeg", "-f", "lavfi", "-i", "anullsrc=duration=1",
        "-acodec", format_type.lower(), "-y", str(file_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)

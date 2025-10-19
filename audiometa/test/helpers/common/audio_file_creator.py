"""Audio file creator utilities for testing."""

import subprocess
import shutil
from pathlib import Path


class AudioFileCreator:
    """Utilities for creating minimal audio files for testing."""
    
    @staticmethod
    def create_minimal_audio_file(file_path: Path, format_type: str, test_files_dir: Path) -> None:
        """Create a minimal audio file for testing.
        
        Args:
            file_path: Path where to create the file
            format_type: Audio format ('mp3', 'flac', 'wav')
            test_files_dir: Directory containing template files
        """
        if format_type.lower() in ['mp3', 'id3v1', 'id3v2.3', 'id3v2.4']:
            template_file = test_files_dir / "metadata=none.mp3"
        elif format_type.lower() == 'flac':
            template_file = test_files_dir / "metadata=none.flac"
        elif format_type.lower() == 'wav':
            template_file = test_files_dir / "metadata=none.wav"
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
        
        if template_file.exists():
            # Copy from template
            shutil.copy2(template_file, file_path)
        else:
            # Fallback: create a minimal file using ffmpeg if available
            try:
                # For id3v1, id3v2.3, id3v2.4, use mp3 format for ffmpeg
                if format_type.lower() in ['id3v1', 'id3v2.3', 'id3v2.4']:
                    actual_format = 'mp3'
                else:
                    actual_format = format_type.lower()
                AudioFileCreator._create_minimal_audio_with_ffmpeg(file_path, actual_format)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Last resort: copy from any available sample file
                if format_type.lower() in ['id3v1', 'id3v2.3', 'id3v2.4']:
                    search_format = 'mp3'
                else:
                    search_format = format_type.lower()
                sample_files = list(test_files_dir.glob(f"*.{search_format}"))
                if sample_files:
                    shutil.copy2(sample_files[0], file_path)
                else:
                    raise RuntimeError(f"No template file found for {format_type}")
    
    @staticmethod
    def _create_minimal_audio_with_ffmpeg(file_path: Path, format_type: str) -> None:
        """Create a minimal audio file using ffmpeg."""
        # Create 1 second of silence
        cmd = [
            "ffmpeg", "-f", "lavfi", "-i", "anullsrc=duration=1",
            "-acodec", format_type.lower(), "-y", str(file_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
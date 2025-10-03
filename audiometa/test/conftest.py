"""Test configuration for audiometa-python tests."""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def test_files_dir() -> Path:
    """Return the path to the test audio files directory."""
    return Path(__file__).parent / "data" / "audio_files"


@pytest.fixture
def temp_audio_file() -> Generator[Path, None, None]:
    """Create a temporary audio file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        temp_path = Path(tmp_file.name)
    
    yield temp_path
    
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def sample_mp3_file(test_files_dir: Path) -> Path:
    """Return path to a sample MP3 file."""
    return test_files_dir / "sample.mp3"


@pytest.fixture
def sample_flac_file(test_files_dir: Path) -> Path:
    """Return path to a sample FLAC file."""
    return test_files_dir / "sample.flac"


@pytest.fixture
def sample_wav_file(test_files_dir: Path) -> Path:
    """Return path to a sample WAV file."""
    return test_files_dir / "sample.wav"


@pytest.fixture
def sample_ogg_file(test_files_dir: Path) -> Path:
    """Return path to a sample OGG file."""
    return test_files_dir / "sample.ogg"
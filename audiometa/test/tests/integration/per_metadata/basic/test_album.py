"""Tests for album metadata."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestAlbumMetadata:
    """Test cases for album metadata."""

    def test_album_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test album metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_album = "Test Album Name"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_album_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test album metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_album = "FLAC Test Album"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_album_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test album metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_album = "WAV Test Album"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(temp_audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_album_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test album metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_album = "AudioFile Test Album"
        test_metadata = {UnifiedMetadataKey.ALBUM_NAME: test_album}
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_unified_metadata(audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album

    def test_album_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test album metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test short album name
        short_album = "A"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ALBUM_NAME: short_album})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == short_album
        
        # Test long album name
        long_album = "A" * 1000
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ALBUM_NAME: long_album})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) is not None
        assert len(metadata.get(UnifiedMetadataKey.ALBUM_NAME)) > 0
        
        # Test empty album name
        empty_album = ""
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ALBUM_NAME: empty_album})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == empty_album

    def test_album_metadata_formats(self, album_koko_id3v2_mp3, album_koko_id3v2_wav, album_koko_vorbis_flac):
        """Test album metadata across different formats."""
        # ID3v2 album (MP3)
        metadata = get_merged_unified_metadata(album_koko_id3v2_mp3)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "koko"
        
        # ID3v2 album (WAV)
        metadata = get_merged_unified_metadata(album_koko_id3v2_wav)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "koko"
        
        # Vorbis album (FLAC)
        metadata = get_merged_unified_metadata(album_koko_vorbis_flac)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "koko"

    def test_album_metadata_reading(self, album_koko_id3v2_mp3, album_koko_id3v2_wav, album_koko_vorbis_flac):
        """Test reading album metadata from different formats."""
        # ID3v2 album (MP3)
        metadata = get_merged_unified_metadata(album_koko_id3v2_mp3)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "koko"
        
        # ID3v2 album (WAV)
        metadata = get_merged_unified_metadata(album_koko_id3v2_wav)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "koko"
        
        # Vorbis album (FLAC)
        metadata = get_merged_unified_metadata(album_koko_vorbis_flac)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "koko"

    def test_album_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        """Test writing album metadata to different formats."""
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_album = "Test Album MP3"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ALBUM_NAME: test_album})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_album = "Test Album FLAC"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ALBUM_NAME: test_album})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_album = "Test Album WAV"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ALBUM_NAME: test_album})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == test_album


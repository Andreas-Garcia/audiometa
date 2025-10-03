"""Tests for advanced metadata fields (cover art, MusicBrainz, ReplayGain, etc.)."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_app_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.utils.TagFormat import MetadataFormat


class TestAdvancedMetadata:
    """Test cases for advanced metadata fields."""

    def test_cover_art_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test cover art metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Create a small test image data
        test_cover_art = b"fake_image_data_for_testing"
        test_metadata = {AppMetadataKey.COVER_ART: test_cover_art}
        update_file_metadata(temp_audio_file, test_metadata)
        
        cover_art = get_specific_metadata(temp_audio_file, AppMetadataKey.COVER_ART)
        assert cover_art == test_cover_art

    def test_cover_art_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test cover art metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_cover_art = b"flac_cover_art_data"
        test_metadata = {AppMetadataKey.COVER_ART: test_cover_art}
        update_file_metadata(temp_audio_file, test_metadata)
        
        cover_art = get_specific_metadata(temp_audio_file, AppMetadataKey.COVER_ART)
        assert cover_art == test_cover_art

    def test_cover_art_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that cover art is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support cover art, so this should be ignored
        test_metadata = {AppMetadataKey.COVER_ART: b"wav_cover_art_data"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Cover art should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.COVER_ART not in metadata or metadata.get(AppMetadataKey.COVER_ART) is None

    def test_compilation_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test compilation metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test True
        test_metadata = {AppMetadataKey.COMPILATION: True}
        update_file_metadata(temp_audio_file, test_metadata)
        
        compilation = get_specific_metadata(temp_audio_file, AppMetadataKey.COMPILATION)
        assert compilation is True
        
        # Test False
        test_metadata = {AppMetadataKey.COMPILATION: False}
        update_file_metadata(temp_audio_file, test_metadata)
        
        compilation = get_specific_metadata(temp_audio_file, AppMetadataKey.COMPILATION)
        assert compilation is False

    def test_compilation_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test compilation metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COMPILATION: True}
        update_file_metadata(temp_audio_file, test_metadata)
        
        compilation = get_specific_metadata(temp_audio_file, AppMetadataKey.COMPILATION)
        assert compilation is True

    def test_compilation_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that compilation is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support compilation, so this should be ignored
        test_metadata = {AppMetadataKey.COMPILATION: True}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Compilation should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.COMPILATION not in metadata or metadata.get(AppMetadataKey.COMPILATION) is None

    def test_media_type_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test media type metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.MEDIA_TYPE: "Digital Media"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        media_type = get_specific_metadata(temp_audio_file, AppMetadataKey.MEDIA_TYPE)
        assert media_type == "Digital Media"

    def test_media_type_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test media type metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.MEDIA_TYPE: "Lossless Audio"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        media_type = get_specific_metadata(temp_audio_file, AppMetadataKey.MEDIA_TYPE)
        assert media_type == "Lossless Audio"

    def test_media_type_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test media type metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.MEDIA_TYPE: "Uncompressed Audio"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        media_type = get_specific_metadata(temp_audio_file, AppMetadataKey.MEDIA_TYPE)
        assert media_type == "Uncompressed Audio"

    def test_file_owner_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test file owner metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.FILE_OWNER: "Test Owner"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        file_owner = get_specific_metadata(temp_audio_file, AppMetadataKey.FILE_OWNER)
        assert file_owner == "Test Owner"

    def test_file_owner_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test file owner metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.FILE_OWNER: "FLAC Owner"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        file_owner = get_specific_metadata(temp_audio_file, AppMetadataKey.FILE_OWNER)
        assert file_owner == "FLAC Owner"

    def test_file_owner_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that file owner is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support file owner, so this should be ignored
        test_metadata = {AppMetadataKey.FILE_OWNER: "WAV Owner"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # File owner should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.FILE_OWNER not in metadata or metadata.get(AppMetadataKey.FILE_OWNER) is None

    def test_recording_date_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test recording date metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.RECORDING_DATE: "2024-01-15"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        recording_date = get_specific_metadata(temp_audio_file, AppMetadataKey.RECORDING_DATE)
        assert recording_date == "2024-01-15"

    def test_recording_date_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test recording date metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.RECORDING_DATE: "2024-02-20"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        recording_date = get_specific_metadata(temp_audio_file, AppMetadataKey.RECORDING_DATE)
        assert recording_date == "2024-02-20"

    def test_recording_date_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that recording date is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support recording date, so this should be ignored
        test_metadata = {AppMetadataKey.RECORDING_DATE: "2024-03-10"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Recording date should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.RECORDING_DATE not in metadata or metadata.get(AppMetadataKey.RECORDING_DATE) is None

    def test_encoder_settings_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test encoder settings metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ENCODER_SETTINGS: "VBR 0"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        encoder_settings = get_specific_metadata(temp_audio_file, AppMetadataKey.ENCODER_SETTINGS)
        assert encoder_settings == "VBR 0"

    def test_encoder_settings_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test encoder settings metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ENCODER_SETTINGS: "Level 8"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        encoder_settings = get_specific_metadata(temp_audio_file, AppMetadataKey.ENCODER_SETTINGS)
        assert encoder_settings == "Level 8"

    def test_encoder_settings_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that encoder settings is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support encoder settings, so this should be ignored
        test_metadata = {AppMetadataKey.ENCODER_SETTINGS: "PCM 16-bit"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Encoder settings should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.ENCODER_SETTINGS not in metadata or metadata.get(AppMetadataKey.ENCODER_SETTINGS) is None

    def test_replaygain_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test ReplayGain metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.REPLAYGAIN: "Track Gain: -3.2 dB"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        replaygain = get_specific_metadata(temp_audio_file, AppMetadataKey.REPLAYGAIN)
        assert replaygain == "Track Gain: -3.2 dB"

    def test_replaygain_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test ReplayGain metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.REPLAYGAIN: "Album Gain: -2.8 dB"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        replaygain = get_specific_metadata(temp_audio_file, AppMetadataKey.REPLAYGAIN)
        assert replaygain == "Album Gain: -2.8 dB"

    def test_replaygain_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that ReplayGain is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support ReplayGain, so this should be ignored
        test_metadata = {AppMetadataKey.REPLAYGAIN: "Track Gain: -1.5 dB"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # ReplayGain should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.REPLAYGAIN not in metadata or metadata.get(AppMetadataKey.REPLAYGAIN) is None

    def test_musicbrainz_id_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test MusicBrainz ID metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_mbid = "4a45b00b-273d-40ed-9ecd-42f387f59c22"
        test_metadata = {AppMetadataKey.MUSICBRAINZ_ID: test_mbid}
        update_file_metadata(temp_audio_file, test_metadata)
        
        mbid = get_specific_metadata(temp_audio_file, AppMetadataKey.MUSICBRAINZ_ID)
        assert mbid == test_mbid

    def test_musicbrainz_id_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test MusicBrainz ID metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_mbid = "b8f8f8f8-273d-40ed-9ecd-42f387f59c22"
        test_metadata = {AppMetadataKey.MUSICBRAINZ_ID: test_mbid}
        update_file_metadata(temp_audio_file, test_metadata)
        
        mbid = get_specific_metadata(temp_audio_file, AppMetadataKey.MUSICBRAINZ_ID)
        assert mbid == test_mbid

    def test_musicbrainz_id_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that MusicBrainz ID is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support MusicBrainz ID, so this should be ignored
        test_metadata = {AppMetadataKey.MUSICBRAINZ_ID: "c9f9f9f9-273d-40ed-9ecd-42f387f59c22"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # MusicBrainz ID should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.MUSICBRAINZ_ID not in metadata or metadata.get(AppMetadataKey.MUSICBRAINZ_ID) is None

    def test_original_date_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test original date metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ORIGINAL_DATE: "2020-01-01"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        original_date = get_specific_metadata(temp_audio_file, AppMetadataKey.ORIGINAL_DATE)
        assert original_date == "2020-01-01"

    def test_original_date_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test original date metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ORIGINAL_DATE: "2019-06-15"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        original_date = get_specific_metadata(temp_audio_file, AppMetadataKey.ORIGINAL_DATE)
        assert original_date == "2019-06-15"

    def test_original_date_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that original date is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support original date, so this should be ignored
        test_metadata = {AppMetadataKey.ORIGINAL_DATE: "2018-12-25"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Original date should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.ORIGINAL_DATE not in metadata or metadata.get(AppMetadataKey.ORIGINAL_DATE) is None

    def test_remixer_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test remixer metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.REMIXER: "Test Remixer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        remixer = get_specific_metadata(temp_audio_file, AppMetadataKey.REMIXER)
        assert remixer == "Test Remixer"

    def test_remixer_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test remixer metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.REMIXER: "FLAC Remixer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        remixer = get_specific_metadata(temp_audio_file, AppMetadataKey.REMIXER)
        assert remixer == "FLAC Remixer"

    def test_remixer_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that remixer is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support remixer, so this should be ignored
        test_metadata = {AppMetadataKey.REMIXER: "WAV Remixer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Remixer should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.REMIXER not in metadata or metadata.get(AppMetadataKey.REMIXER) is None

    def test_conductor_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test conductor metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.CONDUCTOR: "Test Conductor"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        conductor = get_specific_metadata(temp_audio_file, AppMetadataKey.CONDUCTOR)
        assert conductor == "Test Conductor"

    def test_conductor_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test conductor metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.CONDUCTOR: "FLAC Conductor"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        conductor = get_specific_metadata(temp_audio_file, AppMetadataKey.CONDUCTOR)
        assert conductor == "FLAC Conductor"

    def test_conductor_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test conductor metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.CONDUCTOR: "WAV Conductor"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        conductor = get_specific_metadata(temp_audio_file, AppMetadataKey.CONDUCTOR)
        assert conductor == "WAV Conductor"

    def test_complete_advanced_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all advanced metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.COVER_ART: b"test_cover_art_data",
            AppMetadataKey.COMPILATION: True,
            AppMetadataKey.MEDIA_TYPE: "Digital Media",
            AppMetadataKey.FILE_OWNER: "Test Owner",
            AppMetadataKey.RECORDING_DATE: "2024-01-15",
            AppMetadataKey.ENCODER_SETTINGS: "VBR 0",
            AppMetadataKey.REPLAYGAIN: "Track Gain: -3.2 dB",
            AppMetadataKey.MUSICBRAINZ_ID: "4a45b00b-273d-40ed-9ecd-42f387f59c22",
            AppMetadataKey.ORIGINAL_DATE: "2020-01-01",
            AppMetadataKey.REMIXER: "Test Remixer",
            AppMetadataKey.CONDUCTOR: "Test Conductor"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.COVER_ART) == b"test_cover_art_data"
        assert metadata.get(AppMetadataKey.COMPILATION) is True
        assert metadata.get(AppMetadataKey.MEDIA_TYPE) == "Digital Media"
        assert metadata.get(AppMetadataKey.FILE_OWNER) == "Test Owner"
        assert metadata.get(AppMetadataKey.RECORDING_DATE) == "2024-01-15"
        assert metadata.get(AppMetadataKey.ENCODER_SETTINGS) == "VBR 0"
        assert metadata.get(AppMetadataKey.REPLAYGAIN) == "Track Gain: -3.2 dB"
        assert metadata.get(AppMetadataKey.MUSICBRAINZ_ID) == "4a45b00b-273d-40ed-9ecd-42f387f59c22"
        assert metadata.get(AppMetadataKey.ORIGINAL_DATE) == "2020-01-01"
        assert metadata.get(AppMetadataKey.REMIXER) == "Test Remixer"
        assert metadata.get(AppMetadataKey.CONDUCTOR) == "Test Conductor"

    def test_advanced_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test advanced metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.COMPILATION: True,
            AppMetadataKey.MEDIA_TYPE: "AudioFile Media",
            AppMetadataKey.CONDUCTOR: "AudioFile Conductor"
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.COMPILATION) is True
        assert metadata.get(AppMetadataKey.MEDIA_TYPE) == "AudioFile Media"
        assert metadata.get(AppMetadataKey.CONDUCTOR) == "AudioFile Conductor"

    def test_empty_advanced_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing advanced metadata."""
        # Test reading from file with no advanced metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific advanced metadata that doesn't exist
        cover_art = get_specific_metadata(sample_mp3_file, AppMetadataKey.COVER_ART)
        assert cover_art is None or isinstance(cover_art, bytes)
        
        compilation = get_specific_metadata(sample_mp3_file, AppMetadataKey.COMPILATION)
        assert compilation is None or isinstance(compilation, bool)
        
        musicbrainz_id = get_specific_metadata(sample_mp3_file, AppMetadataKey.MUSICBRAINZ_ID)
        assert musicbrainz_id is None or isinstance(musicbrainz_id, str)




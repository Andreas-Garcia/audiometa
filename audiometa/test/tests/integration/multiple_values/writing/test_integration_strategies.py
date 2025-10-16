import pytest
from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


class TestMultipleValuesIntegrationStrategies:
    def test_write_multiple_values_with_sync_strategy(self, temp_audio_file: Path, sample_mp3_file: Path):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Write multiple values with SYNC strategy
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist One", "New Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["New Composer One", "New Composer Two"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_strategy=MetadataWritingStrategy.SYNC)
            
            # Verify values were written
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "New Artist One" in artists
            assert "New Artist Two" in artists
            
            assert isinstance(composers, list)
            assert len(composers) == 2
            assert "New Composer One" in composers
            assert "New Composer Two" in composers

    def test_write_multiple_values_with_preserve_strategy(self, temp_audio_file: Path, sample_mp3_file: Path):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Write multiple values with PRESERVE strategy
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Preserved Artist One", "Preserved Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["Preserved Composer One", "Preserved Composer Two"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
            
            # Verify values were written
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Preserved Artist One" in artists
            assert "Preserved Artist Two" in artists
            
            assert isinstance(composers, list)
            assert len(composers) == 2
            assert "Preserved Composer One" in composers
            assert "Preserved Composer Two" in composers

    def test_write_multiple_values_with_cleanup_strategy(self, temp_audio_file: Path, sample_mp3_file: Path):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Write multiple values with CLEANUP strategy
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Cleanup Artist One", "Cleanup Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["Cleanup Composer One", "Cleanup Composer Two"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
            
            # Verify values were written
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Cleanup Artist One" in artists
            assert "Cleanup Artist Two" in artists
            
            assert isinstance(composers, list)
            assert len(composers) == 2
            assert "Cleanup Composer One" in composers
            assert "Cleanup Composer Two" in composers

    def test_write_multiple_values_with_existing_metadata(self, temp_audio_file: Path, sample_mp3_file: Path):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # First, write some initial metadata
            initial_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Initial Artist One", "Initial Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["Initial Composer One", "Initial Composer Two"]
            }
            update_file_metadata(test_file.path, initial_metadata)
            
            # Verify initial metadata was written
            unified_metadata = get_merged_unified_metadata(test_file.path)
            initial_artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            initial_composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(initial_artists, list)
            assert len(initial_artists) == 2
            assert "Initial Artist One" in initial_artists
            assert "Initial Artist Two" in initial_artists
            
            # Now write new metadata
            new_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["New Artist One", "New Artist Two", "New Artist Three"],
                UnifiedMetadataKey.COMPOSER: ["New Composer One", "New Composer Two"]
            }
            update_file_metadata(test_file.path, new_metadata)
            
            # Verify new metadata replaced the old
            unified_metadata = get_merged_unified_metadata(test_file.path)
            new_artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            new_composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(new_artists, list)
            assert len(new_artists) == 3
            assert "New Artist One" in new_artists
            assert "New Artist Two" in new_artists
            assert "New Artist Three" in new_artists
            assert "Initial Artist One" not in new_artists
            assert "Initial Artist Two" not in new_artists
            
            assert isinstance(new_composers, list)
            assert len(new_composers) == 2
            assert "New Composer One" in new_composers
            assert "New Composer Two" in new_composers
            assert "Initial Composer One" not in new_composers
            assert "Initial Composer Two" not in new_composers

    def test_write_multiple_values_with_partial_update(self, temp_audio_file: Path, sample_mp3_file: Path):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # First, write some initial metadata
            initial_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Initial Artist One", "Initial Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["Initial Composer One", "Initial Composer Two"],
                UnifiedMetadataKey.TITLE: "Initial Title"
            }
            update_file_metadata(test_file.path, initial_metadata)
            
            # Now write partial update (only artists)
            partial_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Updated Artist One", "Updated Artist Two", "Updated Artist Three"]
            }
            update_file_metadata(test_file.path, partial_metadata)
            
            # Verify partial update
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            title = unified_metadata.get(UnifiedMetadataKey.TITLE)
            
            # Artists should be updated
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Updated Artist One" in artists
            assert "Updated Artist Two" in artists
            assert "Updated Artist Three" in artists
            
            # Composers should remain unchanged
            assert isinstance(composers, list)
            assert len(composers) == 2
            assert "Initial Composer One" in composers
            assert "Initial Composer Two" in composers
            
            # Title should remain unchanged
            assert title == "Initial Title"

    def test_write_multiple_values_with_cleanup_after_preserve(self, temp_audio_file: Path, sample_mp3_file: Path):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Write with PRESERVE strategy first
            preserve_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Preserve Artist One", "Preserve Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["Preserve Composer One", "Preserve Composer Two"]
            }
            update_file_metadata(test_file.path, preserve_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
            
            # Then write with CLEANUP strategy
            cleanup_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Cleanup Artist One", "Cleanup Artist Two"],
                UnifiedMetadataKey.COMPOSER: ["Cleanup Composer One", "Cleanup Composer Two"]
            }
            update_file_metadata(test_file.path, cleanup_metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
            
            # Verify final state
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Cleanup Artist One" in artists
            assert "Cleanup Artist Two" in artists
            
            assert isinstance(composers, list)
            assert len(composers) == 2
            assert "Cleanup Composer One" in composers
            assert "Cleanup Composer Two" in composers

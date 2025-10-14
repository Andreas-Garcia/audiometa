import pytest
import shutil
from pathlib import Path

from audiometa import delete_all_metadata, update_file_metadata, get_single_format_app_metadata
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.tests.test_version_helpers import TempFileWithId3v1Version
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestComprehensiveID3v1Deletion:

    def test_comprehensive_id3v1_deletion_mp3(self):
        # Test both ID3v1.0 and ID3v1.1 versions
        for version in ['1.0', '1.1']:
            with self._create_test_file_with_id3v1_version(version) as test_file:
                # Verify ID3v1 metadata exists before deletion
                assert test_file.has_id3v1_metadata(), f"ID3v1.{version} metadata should exist before deletion"
                
                # Get comprehensive metadata before deletion
                before_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
                assert before_metadata.get(UnifiedMetadataKey.TITLE) is not None, f"ID3v1.{version} should have metadata before deletion"
                
                # Delete all metadata
                result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V1)
                assert result is True, f"ID3v1.{version} deletion should succeed"
                
                # Verify ID3v1 metadata is completely removed
                after_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
                assert after_metadata.get(UnifiedMetadataKey.TITLE) is None, f"ID3v1.{version} metadata should be completely removed"
                
                # Verify file no longer has ID3v1 tag at end
                assert not test_file.has_id3v1_metadata(), f"ID3v1.{version} tag should be removed from file"

    def test_id3v1_deletion_with_track_number(self):
        # Test ID3v1.1 with track number
        id3v1_metadata = {
            "title": "Test Title with Track",
            "artist": "Test Artist",
            "album": "Test Album",
            "year": "2023",
            "genre": "Rock",
            "comment": "Test comment",
            "track": 5
        }
        
        with TempFileWithMetadata(id3v1_metadata, "mp3") as test_file:
            # Verify track number is present
            before_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert before_metadata.get(UnifiedMetadataKey.TRACK_NUMBER) == 5, "Track number should be present"
            
            # Delete ID3v1 metadata
            result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V1)
            assert result is True, "ID3v1 deletion with track number should succeed"
            
            # Verify all metadata including track number is removed
            after_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert after_metadata.get(UnifiedMetadataKey.TRACK_NUMBER) is None, "Track number should be removed"
            assert after_metadata.get(UnifiedMetadataKey.TITLE) is None, "Title should be removed"

    def test_id3v1_deletion_without_existing_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Test deletion when no ID3v1 metadata exists
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Verify no ID3v1 metadata exists
        before_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        assert before_metadata.get(UnifiedMetadataKey.TITLE) is None, "No ID3v1 metadata should exist"
        
        # Delete ID3v1 metadata (should succeed even if none exists)
        result = delete_all_metadata(temp_audio_file, tag_format=MetadataFormat.ID3V1)
        assert result is True, "ID3v1 deletion should succeed even when no metadata exists"
        
        # Verify still no metadata
        after_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        assert after_metadata.get(UnifiedMetadataKey.TITLE) is None, "Still no ID3v1 metadata should exist"

    def test_id3v1_deletion_mixed_with_id3v2(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Test ID3v1 deletion when mixed with ID3v2
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Add ID3v1 metadata using external script
        id3v1_metadata = {
            "title": "ID3v1 Title",
            "artist": "ID3v1 Artist",
            "album": "ID3v1 Album"
        }
        
        with TempFileWithMetadata(id3v1_metadata, "mp3") as id3v1_file:
            # Copy the ID3v1 file to our temp location
            shutil.copy2(id3v1_file.path, temp_audio_file)
            
            # Add ID3v2 metadata
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(temp_audio_file, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Verify both formats have metadata
            id3v1_before = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
            id3v2_before = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
            assert id3v1_before.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            assert id3v2_before.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Delete only ID3v1 metadata
            result = delete_all_metadata(temp_audio_file, tag_format=MetadataFormat.ID3V1)
            assert result is True, "ID3v1 deletion should succeed"
            
            # Verify ID3v1 is removed but ID3v2 remains
            id3v1_after = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
            id3v2_after = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None, "ID3v1 should be removed"
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title", "ID3v2 should remain"

    def test_id3v1_deletion_all_formats_removes_id3v1(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Test that delete_all_metadata removes ID3v1 when no specific format is specified
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Add ID3v1 metadata
        id3v1_metadata = {
            "title": "ID3v1 Title",
            "artist": "ID3v1 Artist"
        }
        
        with TempFileWithMetadata(id3v1_metadata, "mp3") as id3v1_file:
            # Copy the ID3v1 file to our temp location
            shutil.copy2(id3v1_file.path, temp_audio_file)
            
            # Verify ID3v1 metadata exists
            before_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
            assert before_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Delete all metadata (should include ID3v1)
            result = delete_all_metadata(temp_audio_file)
            assert result is True, "Delete all metadata should succeed"
            
            # Verify ID3v1 is removed
            after_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
            assert after_metadata.get(UnifiedMetadataKey.TITLE) is None, "ID3v1 should be removed by delete_all_metadata"

    def test_id3v1_deletion_edge_cases(self):
        # Test various edge cases for ID3v1 deletion
        edge_cases = [
            # Empty title
            {"title": "", "artist": "Artist", "album": "Album"},
            # Maximum length fields
            {"title": "A" * 30, "artist": "B" * 30, "album": "C" * 30},
            # Special characters
            {"title": "Test & Title", "artist": "Artist/Name", "album": "Album (2023)"},
            # Genre edge cases
            {"title": "Test", "artist": "Artist", "album": "Album", "genre": "Unknown"},
        ]
        
        for i, metadata in enumerate(edge_cases):
            with TempFileWithMetadata(metadata, "mp3") as test_file:
                # Verify metadata exists
                before_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
                assert before_metadata.get(UnifiedMetadataKey.TITLE) is not None, f"Edge case {i} should have metadata"
                
                # Delete metadata
                result = delete_all_metadata(test_file.path, tag_format=MetadataFormat.ID3V1)
                assert result is True, f"Edge case {i} deletion should succeed"
                
                # Verify metadata is removed
                after_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
                assert after_metadata.get(UnifiedMetadataKey.TITLE) is None, f"Edge case {i} should have no metadata after deletion"

    def _create_test_file_with_id3v1_version(self, id3v1_version):
        """Create a test file with specific ID3v1 version using external script."""
        return TempFileWithId3v1Version(id3v1_version)

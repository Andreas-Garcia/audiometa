"""
End-to-end tests for metadata deletion workflows.

These tests verify complete deletion workflows that real users would perform,
including full metadata deletion, partial deletion, and cross-format deletion.
"""
import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    delete_all_metadata,
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.test_helpers import TempFileWithMetadata


@pytest.mark.e2e
class TestDeletionWorkflows:

    def test_complete_metadata_deletion_workflow_mp3(self):
        # Complete e2e deletion workflow for MP3
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist",
            "album": "Original Album",
            "year": "2023",
            "genre": "Rock",
            "comment": "Original comment"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # 1. Verify initial metadata exists
            initial_metadata_result = get_merged_unified_metadata(test_file)
            assert initial_metadata_result.get(UnifiedMetadataKey.TITLE) == "Original Title"
            assert initial_metadata_result.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Original Artist"]
            assert initial_metadata_result.get(UnifiedMetadataKey.ALBUM_NAME) == "Original Album"
            
            # 2. Add more metadata using app's function
            additional_metadata = {
                UnifiedMetadataKey.RATING: 85,
                UnifiedMetadataKey.BPM: 120,
                UnifiedMetadataKey.COMMENT: "Updated comment"
            }
            update_file_metadata(test_file.path, additional_metadata, normalized_rating_max_value=100)
            
            # 3. Verify metadata was added
            updated_metadata = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            assert updated_metadata.get(UnifiedMetadataKey.RATING) == 85
            assert updated_metadata.get(UnifiedMetadataKey.BPM) == 120
            
            # 4. Delete all metadata
            delete_result = delete_all_metadata(test_file)
            assert delete_result is True
            
            # 5. Verify all metadata was deleted
            deleted_metadata = get_merged_unified_metadata(test_file)
            assert deleted_metadata.get(UnifiedMetadataKey.TITLE) is None or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Original Title"
            assert deleted_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None or deleted_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) != ["Original Artist"]
            assert deleted_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None or deleted_metadata.get(UnifiedMetadataKey.ALBUM_NAME) != "Original Album"
            assert deleted_metadata.get(UnifiedMetadataKey.RATING) is None
            assert deleted_metadata.get(UnifiedMetadataKey.BPM) is None

    def test_complete_metadata_deletion_workflow_flac(self):
        # Complete e2e deletion workflow for FLAC
        initial_metadata = {
            "title": "FLAC Original Title",
            "artist": "FLAC Original Artist",
            "album": "FLAC Original Album"
        }
        
        with TempFileWithMetadata(initial_metadata, "flac") as test_file:
            # 1. Verify initial metadata exists
            initial_metadata_result = get_merged_unified_metadata(test_file)
            assert initial_metadata_result.get(UnifiedMetadataKey.TITLE) == "FLAC Original Title"
            
            # 2. Add more metadata
            additional_metadata = {
                UnifiedMetadataKey.RATING: 90,
                UnifiedMetadataKey.BPM: 140,
                UnifiedMetadataKey.COMMENT: "FLAC comment"
            }
            update_file_metadata(test_file.path, additional_metadata, normalized_rating_max_value=100)
            
            # 3. Delete all metadata
            delete_result = delete_all_metadata(test_file)
            assert delete_result is True
            
            # 4. Verify all metadata was deleted
            deleted_metadata = get_merged_unified_metadata(test_file)
            assert deleted_metadata.get(UnifiedMetadataKey.TITLE) is None or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "FLAC Original Title"
            assert deleted_metadata.get(UnifiedMetadataKey.RATING) is None

    def test_complete_metadata_deletion_workflow_wav(self):
        # Complete e2e deletion workflow for WAV
        initial_metadata = {
            "title": "WAV Original Title",
            "artist": "WAV Original Artist",
            "album": "WAV Original Album"
        }
        
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # 1. Verify initial metadata exists
            initial_metadata_result = get_merged_unified_metadata(test_file)
            assert initial_metadata_result.get(UnifiedMetadataKey.TITLE) == "WAV Original Title"
            
            # 2. Add more metadata (WAV doesn't support rating/BPM)
            additional_metadata = {
                UnifiedMetadataKey.COMMENT: "WAV comment"
            }
            update_file_metadata(test_file.path, additional_metadata)
            
            # 3. Delete all metadata
            delete_result = delete_all_metadata(test_file)
            assert delete_result is True
            
            # 4. Verify all metadata was deleted
            deleted_metadata = get_merged_unified_metadata(test_file)
            assert deleted_metadata.get(UnifiedMetadataKey.TITLE) is None or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "WAV Original Title"

    def test_partial_metadata_deletion_workflow(self):
        # E2e test for deleting specific metadata fields
        initial_metadata = {
            "title": "Partial Deletion Title",
            "artist": "Partial Deletion Artist",
            "album": "Partial Deletion Album",
            "year": "2023",
            "genre": "Jazz"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # 1. Verify initial metadata
            initial_metadata_result = get_merged_unified_metadata(test_file)
            assert initial_metadata_result.get(UnifiedMetadataKey.TITLE) == "Partial Deletion Title"
            assert initial_metadata_result.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Partial Deletion Artist"]
            assert initial_metadata_result.get(UnifiedMetadataKey.ALBUM_NAME) == "Partial Deletion Album"
            
            # 2. Delete specific fields by setting them to None
            deletion_metadata = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.ARTISTS_NAMES: None
            }
            update_file_metadata(test_file.path, deletion_metadata)
            
            # 3. Verify specific fields were deleted while others remain
            updated_metadata = get_merged_unified_metadata(test_file)
            assert updated_metadata.get(UnifiedMetadataKey.TITLE) is None
            assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is None
            assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Partial Deletion Album"  # Should remain
            
            # 4. Delete remaining metadata
            remaining_deletion = {
                UnifiedMetadataKey.ALBUM_NAME: None,
                UnifiedMetadataKey.RELEASE_DATE: None,
                UnifiedMetadataKey.GENRE_NAME: None
            }
            update_file_metadata(test_file.path, remaining_deletion)
            
            # 5. Verify all metadata is now deleted
            final_metadata = get_merged_unified_metadata(test_file)
            assert final_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None
            assert final_metadata.get(UnifiedMetadataKey.RELEASE_DATE) is None
            assert final_metadata.get(UnifiedMetadataKey.GENRE_NAME) is None

    def test_cross_format_deletion_consistency(self, sample_mp3_file, sample_flac_file, sample_wav_file):
        # E2e test for deletion consistency across formats
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Cross Format Deletion Test",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Test Album"
        }
        
        sample_files = [
            (sample_mp3_file, "mp3"),
            (sample_flac_file, "flac"),
            (sample_wav_file, "wav")
        ]
        
        for file_path, format_type in sample_files:
            # Set up metadata using external script
            initial_metadata = {
                "title": "Original Title",
                "artist": "Original Artist"
            }
            with TempFileWithMetadata(initial_metadata, format_type) as test_file:
                # Add metadata using app's function
                update_file_metadata(test_file.path, test_metadata)
                
                # Verify metadata was added
                added_metadata = get_merged_unified_metadata(test_file)
                assert added_metadata.get(UnifiedMetadataKey.TITLE) == "Cross Format Deletion Test"
                
                # Delete all metadata
                delete_result = delete_all_metadata(test_file)
                assert delete_result is True
                
                # Verify metadata was deleted consistently across formats
                deleted_metadata = get_merged_unified_metadata(test_file)
                assert deleted_metadata.get(UnifiedMetadataKey.TITLE) is None or deleted_metadata.get(UnifiedMetadataKey.TITLE) != "Cross Format Deletion Test"

    def test_format_specific_deletion_workflow(self):
        # E2e test for deleting specific metadata formats
        initial_metadata = {
            "title": "Format Specific Deletion",
            "artist": "Format Specific Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # 1. Add metadata in different formats
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"]
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            id3v1_metadata = {
                UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Album"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # 2. Verify both formats have metadata
            combined_metadata = get_merged_unified_metadata(test_file)
            assert combined_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            assert combined_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v1 Album"
            
            # 3. Delete only ID3v2 metadata
            id3v2_deletion = {
                UnifiedMetadataKey.TITLE: None,
                UnifiedMetadataKey.ARTISTS_NAMES: None
            }
            update_file_metadata(test_file.path, id3v2_deletion, metadata_format=MetadataFormat.ID3V2)
            
            # 4. Verify ID3v2 metadata is deleted but ID3v1 remains
            after_id3v2_deletion = get_merged_unified_metadata(test_file)
            assert after_id3v2_deletion.get(UnifiedMetadataKey.TITLE) is None or after_id3v2_deletion.get(UnifiedMetadataKey.TITLE) != "ID3v2 Title"
            assert after_id3v2_deletion.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v1 Album"  # Should remain
            
            # 5. Delete ID3v1 metadata
            id3v1_deletion = {
                UnifiedMetadataKey.ALBUM_NAME: None
            }
            update_file_metadata(test_file.path, id3v1_deletion, metadata_format=MetadataFormat.ID3V1)
            
            # 6. Verify all metadata is now deleted
            final_metadata = get_merged_unified_metadata(test_file)
            assert final_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is None

    def test_deletion_error_handling_workflow(self, temp_audio_file: Path):
        # E2e test for deletion error scenarios
        # Create a file with unsupported extension
        test_file = temp_audio_file.with_suffix(".txt")
        test_file.write_bytes(b"fake audio content")
        
        # All deletion operations should raise appropriate errors
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            delete_all_metadata(str(test_file))
        
        with pytest.raises(Exception):  # FileTypeNotSupportedError
            update_file_metadata(str(test_file), {UnifiedMetadataKey.TITLE: None})

    def test_deletion_with_rating_normalization_workflow(self):
        # E2e test for deletion with rating normalization
        initial_metadata = {
            "title": "Rating Deletion Test",
            "artist": "Rating Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # 1. Add rating with normalization
            rating_metadata = {
                UnifiedMetadataKey.RATING: 75
            }
            update_file_metadata(test_file.path, rating_metadata, normalized_rating_max_value=100)
            
            # 2. Verify rating was added
            metadata_with_rating = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            assert metadata_with_rating.get(UnifiedMetadataKey.RATING) == 75
            
            # 3. Delete rating
            rating_deletion = {
                UnifiedMetadataKey.RATING: None
            }
            update_file_metadata(test_file.path, rating_deletion, normalized_rating_max_value=100)
            
            # 4. Verify rating was deleted
            metadata_after_deletion = get_merged_unified_metadata(test_file, normalized_rating_max_value=100)
            assert metadata_after_deletion.get(UnifiedMetadataKey.RATING) is None

    def test_batch_deletion_workflow(self, sample_mp3_file, sample_flac_file, sample_wav_file):
        # E2e test for batch deletion operations
        sample_files = [
            (sample_mp3_file, "mp3"),
            (sample_flac_file, "flac"),
            (sample_wav_file, "wav")
        ]
        
        results = []
        
        for file_path, format_type in sample_files:
            try:
                # Set up metadata using external script
                initial_metadata = {
                    "title": f"Batch Deletion Test {format_type.upper()}",
                    "artist": "Batch Artist"
                }
                with TempFileWithMetadata(initial_metadata, format_type) as test_file:
                    # Add more metadata using app's function
                    additional_metadata = {
                        UnifiedMetadataKey.ALBUM_NAME: f"Batch Album {format_type.upper()}",
                        UnifiedMetadataKey.COMMENT: f"Batch comment for {format_type}"
                    }
                    update_file_metadata(test_file.path, additional_metadata)
                    
                    # Verify metadata was added
                    added_metadata = get_merged_unified_metadata(test_file)
                    assert added_metadata.get(UnifiedMetadataKey.TITLE) == f"Batch Deletion Test {format_type.upper()}"
                    
                    # Delete all metadata
                    delete_result = delete_all_metadata(test_file)
                    assert delete_result is True
                    
                    # Verify deletion worked
                    deleted_metadata = get_merged_unified_metadata(test_file)
                    assert deleted_metadata.get(UnifiedMetadataKey.TITLE) is None or deleted_metadata.get(UnifiedMetadataKey.TITLE) != f"Batch Deletion Test {format_type.upper()}"
                    
                    results.append(("success", format_type))
                    
            except Exception as e:
                results.append(("error", format_type, str(e)))
        
        # Verify all files were processed successfully
        assert len(results) == len(sample_files)
        success_count = sum(1 for result in results if result[0] == "success")
        assert success_count == len(sample_files)  # All should succeed

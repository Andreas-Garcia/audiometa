import pytest
from pathlib import Path

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestRatingErrorHandling:

    def test_rating_unsupported_file_type(self, temp_audio_file: Path):
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_specific_metadata(str(temp_audio_file), UnifiedMetadataKey.RATING)
        
        with pytest.raises(FileTypeNotSupportedError):
            update_file_metadata(str(temp_audio_file), {UnifiedMetadataKey.RATING: 85})

    def test_rating_nonexistent_file(self):
        nonexistent_file = "nonexistent_file.mp3"
        
        with pytest.raises(FileNotFoundError):
            get_specific_metadata(nonexistent_file, UnifiedMetadataKey.RATING)
        
        with pytest.raises(FileNotFoundError):
            update_file_metadata(nonexistent_file, {UnifiedMetadataKey.RATING: 85})

    def test_rating_invalid_values(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Test with invalid rating values - should handle gracefully
        invalid_ratings = [-1, 101, "invalid", None]
        
        for invalid_rating in invalid_ratings:
            # Copy file for each test
            temp_audio_file.write_bytes(sample_mp3_file.read_bytes())
            
            # This should not raise an error, but may not set the rating
            update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: invalid_rating})
            
            # Verify the file is still readable
            metadata = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING)
            # Rating should be None or a valid value, not the invalid input
            assert metadata is None or isinstance(metadata, (int, float))

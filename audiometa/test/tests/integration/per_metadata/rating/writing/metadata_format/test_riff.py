import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestRiffRatingWriting:
    
    def test_write_0_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 0}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 0

    def test_write_1_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 20}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 20

    def test_write_2_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 40}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 40

    def test_write_3_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 60}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 60

    def test_write_4_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 80}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 80

    def test_write_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 100}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 100

    def test_write_0_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 10}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 10

    def test_write_1_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 30}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 30

    def test_write_2_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 50}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 50

    def test_write_3_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 70}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 70

    def test_write_4_5_star(self, temp_audio_file):
        basic_metadata = {"title": "Test Title", "artist": "Test Artist"}
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            test_metadata = {UnifiedMetadataKey.RATING: 90}
            update_file_metadata(test_file.path, test_metadata, normalized_rating_max_value=100, metadata_format=MetadataFormat.RIFF)
            rating = get_specific_metadata(test_file.path, UnifiedMetadataKey.RATING, normalized_rating_max_value=100)
            assert rating is not None
            assert rating == 90

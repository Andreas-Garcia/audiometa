import pytest
from pathlib import Path
import tempfile
import shutil
import time

from audiometa import update_file_metadata, get_merged_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestPerformanceLargeData:
    def test_write_large_number_of_artists(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write a large number of artists
        large_artist_list = [f"Artist {i:04d}" for i in range(100)]
        
        start_time = time.time()
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: large_artist_list
        }
        update_file_metadata(temp_audio_file, metadata)
        write_time = time.time() - start_time
        
        # Verify all artists were written
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        read_time = time.time() - start_time
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 100
        
        # Performance assertions (should complete within reasonable time)
        assert write_time < 5.0, f"Write took too long: {write_time:.2f}s"
        assert read_time < 2.0, f"Read took too long: {read_time:.2f}s"

    def test_write_large_strings(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write metadata with very large strings
        large_string = "A" * 10000  # 10KB string
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: [large_string, "Normal Artist"],
            UnifiedMetadataKey.COMMENT: large_string
        }
        
        start_time = time.time()
        update_file_metadata(temp_audio_file, metadata)
        write_time = time.time() - start_time
        
        # Verify data was written correctly
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        read_time = time.time() - start_time
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        comment = unified_metadata.get(UnifiedMetadataKey.COMMENT)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert large_string in artists
        assert "Normal Artist" in artists
        assert comment == large_string
        
        # Performance assertions
        assert write_time < 3.0, f"Write took too long: {write_time:.2f}s"
        assert read_time < 1.0, f"Read took too long: {read_time:.2f}s"

    def test_write_multiple_large_lists(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write multiple fields with large lists
        large_artist_list = [f"Artist {i:04d}" for i in range(50)]
        large_composer_list = [f"Composer {i:04d}" for i in range(50)]
        large_musician_list = [f"Musician {i:04d}: Instrument {i:04d}" for i in range(50)]
        
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: large_artist_list,
            UnifiedMetadataKey.COMPOSER: large_composer_list,
            UnifiedMetadataKey.MUSICIANS: large_musician_list
        }
        
        start_time = time.time()
        update_file_metadata(temp_audio_file, metadata)
        write_time = time.time() - start_time
        
        # Verify all data was written
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        read_time = time.time() - start_time
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
        musicians = unified_metadata.get(UnifiedMetadataKey.MUSICIANS)
        
        assert isinstance(artists, list)
        assert len(artists) == 50
        assert isinstance(composers, list)
        assert len(composers) == 50
        assert isinstance(musicians, list)
        assert len(musicians) == 50
        
        # Performance assertions
        assert write_time < 5.0, f"Write took too long: {write_time:.2f}s"
        assert read_time < 2.0, f"Read took too long: {read_time:.2f}s"

    def test_write_unicode_large_data(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write large amounts of Unicode data
        unicode_artists = [f"艺术家 {i:04d} 🎵" for i in range(100)]
        
        start_time = time.time()
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: unicode_artists
        }
        update_file_metadata(temp_audio_file, metadata)
        write_time = time.time() - start_time
        
        # Verify Unicode data was written correctly
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        read_time = time.time() - start_time
        
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        assert isinstance(artists, list)
        assert len(artists) == 100
        assert "艺术家 0000 🎵" in artists
        assert "艺术家 0099 🎵" in artists
        
        # Performance assertions
        assert write_time < 5.0, f"Write took too long: {write_time:.2f}s"
        assert read_time < 2.0, f"Read took too long: {read_time:.2f}s"

    def test_write_memory_efficiency(self, sample_flac_file: Path, temp_audio_file: Path):
        # Test memory efficiency with large data
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create large metadata
        large_metadata = {}
        for i in range(10):
            large_metadata[UnifiedMetadataKey.ARTISTS_NAMES] = [f"Artist {i:04d}" for i in range(100)]
            large_metadata[UnifiedMetadataKey.COMPOSER] = [f"Composer {i:04d}" for i in range(100)]
            large_metadata[UnifiedMetadataKey.MUSICIANS] = [f"Musician {i:04d}" for i in range(100)]
            
            update_file_metadata(temp_audio_file, large_metadata)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024, f"Memory usage increased too much: {memory_increase / 1024 / 1024:.2f}MB"

    def test_write_concurrent_access(self, sample_flac_file: Path, temp_audio_file: Path):
        # Test writing to the same file multiple times quickly
        for i in range(10):
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: [f"Artist {i:04d}", f"Artist {i+1:04d}"]
            }
            update_file_metadata(temp_audio_file, metadata)
        
        # Verify final state
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
        
        assert isinstance(artists, list)
        assert len(artists) == 2
        assert "Artist 0009" in artists
        assert "Artist 0010" in artists

    def test_write_large_metadata_dict(self, sample_flac_file: Path, temp_audio_file: Path):
        # Write a large metadata dictionary with many fields
        large_metadata = {}
        
        # Add multiple values for each supported multiple-value field
        large_metadata[UnifiedMetadataKey.ARTISTS_NAMES] = [f"Artist {i:04d}" for i in range(20)]
        large_metadata[UnifiedMetadataKey.ALBUM_ARTISTS_NAMES] = [f"Album Artist {i:04d}" for i in range(20)]
        large_metadata[UnifiedMetadataKey.COMPOSER] = [f"Composer {i:04d}" for i in range(20)]
        large_metadata[UnifiedMetadataKey.INVOLVED_PEOPLE] = [f"Person {i:04d}: Role {i:04d}" for i in range(20)]
        large_metadata[UnifiedMetadataKey.MUSICIANS] = [f"Musician {i:04d}: Instrument {i:04d}" for i in range(20)]
        large_metadata[UnifiedMetadataKey.KEYWORDS] = [f"keyword{i:04d}" for i in range(20)]
        
        # Add single values
        large_metadata[UnifiedMetadataKey.TITLE] = "Large Metadata Test"
        large_metadata[UnifiedMetadataKey.ALBUM_NAME] = "Large Album"
        large_metadata[UnifiedMetadataKey.GENRE_NAME] = "Test Genre"
        large_metadata[UnifiedMetadataKey.COMMENT] = "This is a test comment for large metadata"
        
        start_time = time.time()
        update_file_metadata(temp_audio_file, large_metadata)
        write_time = time.time() - start_time
        
        # Verify all data was written
        start_time = time.time()
        unified_metadata = get_merged_unified_metadata(temp_audio_file)
        read_time = time.time() - start_time
        
        # Check multiple value fields
        for field in [UnifiedMetadataKey.ARTISTS_NAMES, UnifiedMetadataKey.ALBUM_ARTISTS_NAMES, 
                     UnifiedMetadataKey.COMPOSER, UnifiedMetadataKey.INVOLVED_PEOPLE,
                     UnifiedMetadataKey.MUSICIANS, UnifiedMetadataKey.KEYWORDS]:
            values = unified_metadata.get(field)
            assert isinstance(values, list)
            assert len(values) == 20
        
        # Check single value fields
        assert unified_metadata.get(UnifiedMetadataKey.TITLE) == "Large Metadata Test"
        assert unified_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Large Album"
        assert unified_metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre"
        assert unified_metadata.get(UnifiedMetadataKey.COMMENT) == "This is a test comment for large metadata"
        
        # Performance assertions
        assert write_time < 5.0, f"Write took too long: {write_time:.2f}s"
        assert read_time < 2.0, f"Read took too long: {read_time:.2f}s"

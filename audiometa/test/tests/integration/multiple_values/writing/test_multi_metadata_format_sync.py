from pathlib import Path

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata,
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


class TestMultiMetadataFormatSync:
    def test_wav_sync_multiple_values_with_all_formats(self, sample_wav_file: Path, temp_audio_file: Path):
        # Create WAV file with existing ID3v2, RIFF, and ID3v1 metadata
        with TempFileWithMetadata({"title": "Initial Title"}, "wav") as test_file:
            # Set up initial metadata in all three formats using helper methods
            # ID3v2 metadata
            test_file.set_id3v2_title("Original ID3v2 Title")
            test_file.set_id3v2_artist("Original ID3v2 Artist")
            test_file.set_id3v2_album("Original ID3v2 Album")
            test_file.set_id3v2_genre("Original ID3v2 Genre")
            
            # RIFF metadata (using our library)
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "Original RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Original RIFF Album",
                UnifiedMetadataKey.GENRES_NAMES: "Original RIFF Genre"
            }
            update_file_metadata(test_file.path, riff_metadata, metadata_format=MetadataFormat.RIFF)
            
            # ID3v1 metadata (using our library)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "Original ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Original ID3v1 Album",
                UnifiedMetadataKey.GENRES_NAMES: "Original ID3v1 Genre"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Verify initial state - all formats have different metadata
            id3v2_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            riff_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            id3v1_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            assert id3v2_initial.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            assert riff_initial.get(UnifiedMetadataKey.TITLE) == "Original RIFF Title"
            assert id3v1_initial.get(UnifiedMetadataKey.TITLE) == "Original ID3v1 Title"
            
            # Now write multiple values using SYNC strategy
            # Focus only on multi-value fields
            sync_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist One", "Synced Artist Two", "Synced Artist Three"]
            }
            
            update_file_metadata(
                test_file.path, 
                sync_metadata, 
                metadata_strategy=MetadataWritingStrategy.SYNC
            )
            
            # Verify RIFF metadata (native format for WAV)
            riff_final = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            
            # RIFF should have multiple values as separate entries
            riff_artists = riff_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(riff_artists, list)
            assert len(riff_artists) == 3
            assert "Synced Artist One" in riff_artists
            assert "Synced Artist Two" in riff_artists
            assert "Synced Artist Three" in riff_artists
            
            # Verify ID3v2 metadata (should be synced)
            id3v2_final = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            
            # ID3v2 should have multiple values as separate entries
            id3v2_artists = id3v2_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(id3v2_artists, list)
            assert len(id3v2_artists) == 3
            assert "Synced Artist One" in id3v2_artists
            assert "Synced Artist Two" in id3v2_artists
            assert "Synced Artist Three" in id3v2_artists
            
            # Verify ID3v1 metadata (should be synced with limitations)
            id3v1_final = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            # ID3v1 should have concatenated values due to format limitations
            id3v1_artists = id3v1_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            # ID3v1 may return a list due to parsing, or a string due to concatenation
            if isinstance(id3v1_artists, list):
                # If it's a list, it means the parsing is working but may be truncated
                assert len(id3v1_artists) >= 1
                assert "Synced Artist One" in id3v1_artists[0] or "Synced Artist One" in str(id3v1_artists)
            else:
                # If it's a string, it should be concatenated
                assert isinstance(id3v1_artists, str)
                assert "Synced Artist One" in id3v1_artists
                # Should be concatenated with separators
                assert ", " in id3v1_artists or "," in id3v1_artists
            
            # Verify merged metadata (should prefer RIFF as native format)
            merged_final = get_merged_unified_metadata(test_file.path)
            
            merged_artists = merged_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(merged_artists, list)
            assert len(merged_artists) == 3
            assert "Synced Artist One" in merged_artists
            assert "Synced Artist Two" in merged_artists
            assert "Synced Artist Three" in merged_artists

    def test_mp3_sync_multiple_values_with_all_formats(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Create MP3 file with existing ID3v2 and ID3v1 metadata
        with TempFileWithMetadata({"title": "Initial Title"}, "mp3") as test_file:
            # Set up initial metadata in both formats
            # ID3v2 metadata
            test_file.set_id3v2_title("Original ID3v2 Title")
            test_file.set_id3v2_artist("Original ID3v2 Artist")
            test_file.set_id3v2_album("Original ID3v2 Album")
            test_file.set_id3v2_genre("Original ID3v2 Genre")
            
            # ID3v1 metadata (using our library)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "Original ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Original ID3v1 Album",
                UnifiedMetadataKey.GENRES_NAMES: "Original ID3v1 Genre"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Verify initial state - both formats have different metadata
            id3v2_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            assert id3v2_initial.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            assert id3v1_initial.get(UnifiedMetadataKey.TITLE) == "Original ID3v1 Title"
            
            # Now write multiple values using SYNC strategy
            # Focus only on multi-value fields
            sync_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist One", "Synced Artist Two", "Synced Artist Three"]
            }
            
            update_file_metadata(
                test_file.path, 
                sync_metadata, 
                metadata_strategy=MetadataWritingStrategy.SYNC
            )
            
            # Verify ID3v2 metadata (native format for MP3)
            id3v2_final = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            
            # ID3v2 should have multiple values as separate entries
            id3v2_artists = id3v2_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(id3v2_artists, list)
            assert len(id3v2_artists) == 3
            assert "Synced Artist One" in id3v2_artists
            assert "Synced Artist Two" in id3v2_artists
            assert "Synced Artist Three" in id3v2_artists
            
            # Verify ID3v1 metadata (should be synced with limitations)
            id3v1_final = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            # ID3v1 should have concatenated values due to format limitations
            id3v1_artists = id3v1_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            # ID3v1 may return a list due to parsing, or a string due to concatenation
            if isinstance(id3v1_artists, list):
                # If it's a list, it means the parsing is working but may be truncated
                assert len(id3v1_artists) >= 1
                assert "Synced Artist One" in id3v1_artists[0] or "Synced Artist One" in str(id3v1_artists)
            else:
                # If it's a string, it should be concatenated
                assert isinstance(id3v1_artists, str)
                assert "Synced Artist One" in id3v1_artists
                # Should be concatenated with separators
                assert ", " in id3v1_artists or "," in id3v1_artists
            
            # Verify merged metadata (should prefer ID3v2 as native format)
            merged_final = get_merged_unified_metadata(test_file.path)
            
            merged_artists = merged_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(merged_artists, list)
            assert len(merged_artists) == 3
            assert "Synced Artist One" in merged_artists
            assert "Synced Artist Two" in merged_artists
            assert "Synced Artist Three" in merged_artists

    def test_flac_sync_multiple_values_with_all_formats(self, sample_flac_file: Path, temp_audio_file: Path):
        # Create FLAC file with existing Vorbis, ID3v2, and ID3v1 metadata
        with TempFileWithMetadata({"title": "Initial Title"}, "flac") as test_file:
            # Set up initial metadata in all three formats
            # ID3v2 metadata
            test_file.set_id3v2_title("Original ID3v2 Title")
            test_file.set_id3v2_artist("Original ID3v2 Artist")
            test_file.set_id3v2_album("Original ID3v2 Album")
            test_file.set_id3v2_genre("Original ID3v2 Genre")
            
            # Vorbis metadata (using our library)
            vorbis_metadata = {
                UnifiedMetadataKey.TITLE: "Original Vorbis Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original Vorbis Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Original Vorbis Album",
                UnifiedMetadataKey.GENRES_NAMES: "Original Vorbis Genre"
            }
            update_file_metadata(test_file.path, vorbis_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # ID3v1 metadata (using our library)
            id3v1_metadata = {
                UnifiedMetadataKey.TITLE: "Original ID3v1 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Original ID3v1 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Original ID3v1 Album",
                UnifiedMetadataKey.GENRES_NAMES: "Original ID3v1 Genre"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Verify initial state - all formats have different metadata
            vorbis_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            id3v2_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            id3v1_initial = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            assert vorbis_initial.get(UnifiedMetadataKey.TITLE) == "Original Vorbis Title"
            assert id3v2_initial.get(UnifiedMetadataKey.TITLE) == "Original ID3v2 Title"
            assert id3v1_initial.get(UnifiedMetadataKey.TITLE) == "Original ID3v1 Title"
            
            # Now write multiple values using SYNC strategy
            # Focus only on multi-value fields
            sync_metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Synced Artist One", "Synced Artist Two", "Synced Artist Three"]
            }
            
            update_file_metadata(
                test_file.path, 
                sync_metadata, 
                metadata_strategy=MetadataWritingStrategy.SYNC
            )
            
            # Verify Vorbis metadata (native format for FLAC)
            vorbis_final = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            
            # Vorbis should have multiple values as separate entries
            vorbis_artists = vorbis_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(vorbis_artists, list)
            assert len(vorbis_artists) == 3
            assert "Synced Artist One" in vorbis_artists
            assert "Synced Artist Two" in vorbis_artists
            assert "Synced Artist Three" in vorbis_artists
            
            # Verify ID3v2 metadata (should be synced)
            id3v2_final = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            
            # ID3v2 should have multiple values as separate entries
            id3v2_artists = id3v2_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(id3v2_artists, list)
            assert len(id3v2_artists) == 3
            assert "Synced Artist One" in id3v2_artists
            assert "Synced Artist Two" in id3v2_artists
            assert "Synced Artist Three" in id3v2_artists
            
            # Verify ID3v1 metadata (should be synced with limitations)
            id3v1_final = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            
            # ID3v1 should have concatenated values due to format limitations
            id3v1_artists = id3v1_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            # ID3v1 may return a list due to parsing, or a string due to concatenation
            if isinstance(id3v1_artists, list):
                # If it's a list, it means the parsing is working but may be truncated
                assert len(id3v1_artists) >= 1
                assert "Synced Artist One" in id3v1_artists[0] or "Synced Artist One" in str(id3v1_artists)
            else:
                # If it's a string, it should be concatenated
                assert isinstance(id3v1_artists, str)
                assert "Synced Artist One" in id3v1_artists
                # Should be concatenated with separators
                assert ", " in id3v1_artists or "," in id3v1_artists
            
            # Verify merged metadata (should prefer Vorbis as native format)
            merged_final = get_merged_unified_metadata(test_file.path)
            
            merged_artists = merged_final.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(merged_artists, list)
            assert len(merged_artists) == 3
            assert "Synced Artist One" in merged_artists
            assert "Synced Artist Two" in merged_artists
            assert "Synced Artist Three" in merged_artists

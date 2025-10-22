import pytest

from audiometa import delete_all_metadata, update_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.common.comprehensive_header_verifier import ComprehensiveHeaderVerifier
from utils.MetadataFormat import MetadataFormat
from utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestAudioFormatHeaderDeletion:

    def test_header_detection_flac(self):        
        with TempFileWithMetadata({"title": "FLAC Test"}, "flac") as flac_file:

            vorbis_metadata = {UnifiedMetadataKey.TITLE: "FLAC Vorbis Title"}
            update_metadata(flac_file.path, vorbis_metadata, metadata_format=MetadataFormat.VORBIS)
            
            id3v2_metadata = {UnifiedMetadataKey.ARTISTS: ["FLAC ID3v2 Artist"]}
            update_metadata(flac_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            id3v1_metadata = {UnifiedMetadataKey.ALBUM: "FLAC ID3v1 Album"}
            update_metadata(flac_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)

            headers = ComprehensiveHeaderVerifier.get_metadata_headers_present(flac_file.path)
            assert headers['vorbis'], "FLAC should have Vorbis metadata header"
            assert headers['id3v2'], "FLAC should have ID3v2 metadata header"
            assert headers['id3v1'], "FLAC should have ID3v1 metadata header"
        
            # Test header removal
            result = delete_all_metadata(flac_file.path)
            assert result is True
            
            # After deletion, headers should be removed
            headers_after = ComprehensiveHeaderVerifier.get_metadata_headers_present(flac_file.path)
            assert not any(headers_after.values()), "All FLAC metadata headers should be deleted"
            
    def test_header_detection_wav(self):
        with TempFileWithMetadata({"title": "WAV Test"}, "wav") as wav_file:
            
            riff_metadata = {UnifiedMetadataKey.TITLE: "WAV RIFF Title"}
            update_metadata(wav_file.path, riff_metadata, metadata_format=MetadataFormat.RIFF)
            
            id3v2_metadata = {UnifiedMetadataKey.ARTISTS: ["WAV ID3v2 Artist"]}
            update_metadata(wav_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            id3v1_metadata = {UnifiedMetadataKey.ALBUM: "WAV ID3v1 Album"}
            update_metadata(wav_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)

            headers = ComprehensiveHeaderVerifier.get_metadata_headers_present(wav_file.path)
            assert headers['id3v2'], "WAV should have ID3v2 metadata header"
            assert headers['id3v1'], "WAV should have ID3v1 metadata header"
            assert headers['riff'], "WAV should have RIFF metadata header"
        
            # Test header removal
            result = delete_all_metadata(wav_file.path)
            assert result is True
            
            # After deletion, headers should be removed
            headers_after = ComprehensiveHeaderVerifier.get_metadata_headers_present(wav_file.path)
            assert not any(headers_after.values()), "All WAV metadata headers should be deleted"
            
    def test_header_detection_mp3(self):
        with TempFileWithMetadata({"title": "MP3 Test"}, "mp3") as mp3_file:
            
            id3v2_metadata = {UnifiedMetadataKey.TITLE: "MP3 ID3v2 Title"}
            update_metadata(mp3_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            id3v1_metadata = {UnifiedMetadataKey.ALBUM: "MP3 ID3v1 Album"}
            update_metadata(mp3_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)

            headers = ComprehensiveHeaderVerifier.get_metadata_headers_present(mp3_file.path)
            assert headers['id3v2'], "MP3 should have ID3v2 metadata header"
            assert headers['id3v1'], "MP3 should have ID3v1 metadata header"
        
            # Test header removal
            result = delete_all_metadata(mp3_file.path)
            assert result is True
            
            # After deletion, headers should be removed
            headers_after = ComprehensiveHeaderVerifier.get_metadata_headers_present(mp3_file.path)
            assert not any(headers_after.values()), "All MP3 metadata headers should be deleted"
            

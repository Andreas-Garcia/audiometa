from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.riff.riff_metadata_inspector import RIFFMetadataInspector
from audiometa.test.helpers.riff.riff_metadata_setter import RIFFMetadataSetter


class TestMultipleEntriesRiff:
	def test_write_multiple_artists(self):
		metadata = {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2", "Artist 3"]}
		with TempFileWithMetadata({}, "wav") as test_file:
			update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.RIFF)

			# Use helper to check the created RIFF frames directly
			verification = RIFFMetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "IART")
			# Expect three separate IART entries
			assert verification['actual_count'] == 3
   

	def test_artists_concatenation(self):
		initial_metadata = {"title": "Test Song"}
		with TempFileWithMetadata(initial_metadata, "wav") as test_file:
			metadata = {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2", "Artist 3"]}

			update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.RIFF)

			# Use helper to check the created RIFF frames directly
			verification = RIFFMetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "IART")
			# Check that all artists appear in the raw output
			raw_output = verification['raw_output']
			assert "Artist 1" in raw_output
			assert "Artist 2" in raw_output
			assert "Artist 3" in raw_output

	def test_with_existing_artists_field(self):
		# Start with an existing artist field
		initial_metadata = {"artist": "Existing Artist"}
		with TempFileWithMetadata(initial_metadata, "wav") as test_file:
			# create an existing value using setter
			RIFFMetadataSetter.set_artist(test_file.path, "Existing 1; Existing 2")
			verification = RIFFMetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "IART")
			assert "Existing 1" in verification['raw_output']
			assert "Existing 2" in verification['raw_output']

			metadata = {UnifiedMetadataKey.ARTISTS_NAMES: ["Existing 1", "New 2"]}
			update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.RIFF)

			verification = RIFFMetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "IART")
			raw_output = verification['raw_output']
			assert "Existing 1" in raw_output
			assert "New 2" in raw_output

"""
id3v2_metadata_getter.py
Helper for extracting ID3v2 metadata from audio files.
"""


from pathlib import Path
from audiometa.test.helpers.common.external_tool_runner import run_external_tool



class Id3v2MetadataGetter:
    """
    Static helper for getting ID3v2 metadata fields from an audio file using external tools.
    """
    @staticmethod
    def _get_id3v2_output(file_path):
        """
        Runs id3v2 tool and returns its output as a string.
        """
        result = run_external_tool(["id3v2", "-l", str(file_path)], "id3v2")
        return result.stdout

    @staticmethod
    def get_metadata(file_path):
        """
        Returns a dictionary of ID3v2 metadata fields using id3v2 tool output.
        """
        output = Id3v2MetadataGetter._get_id3v2_output(file_path)
        metadata = {}
        for line in output.splitlines():
            if line.startswith("TIT2 (Title):"):
                metadata["title"] = line.split(":", 1)[1].strip()
            elif line.startswith("TPE1 (Lead performer(s)/Soloist(s)):"):
                metadata["artists"] = [a.strip() for a in line.split(":", 1)[1].split("/") if a.strip()]
            elif line.startswith("TALB (Album/Movie/Show title):"):
                metadata["album"] = line.split(":", 1)[1].strip()
            elif line.startswith("TDRC (Recording time):"):
                metadata["year"] = line.split(":", 1)[1].strip()
            elif line.startswith("TCON (Content type):"):
                metadata["genre"] = line.split(":", 1)[1].strip()
            elif line.startswith("COMM (Comments):"):
                metadata["comment"] = line.split(":", 1)[1].strip()
            elif line.startswith("TRCK (Track number/Position in set):"):
                metadata["track"] = line.split(":", 1)[1].strip()
        return metadata

    @staticmethod
    def get_artists(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('artists', [])

    @staticmethod
    def get_title(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('title')

    @staticmethod
    def get_album(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('album')

    @staticmethod
    def get_year(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('year')

    @staticmethod
    def get_genre(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('genre')

    @staticmethod
    def get_comment(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('comment')

    @staticmethod
    def get_track(file_path):
        metadata = Id3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('track')

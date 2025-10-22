"""
id3v2_metadata_getter.py
Helper for extracting ID3v2 metadata from audio files.
"""

import re
from audiometa.test.helpers.common.external_tool_runner import run_external_tool

class ID3v2MetadataGetter:
    """Helper class to get ID3v2 metadata from audio files using the mid3v2 tool."""
    @staticmethod
    def get_raw_metadata(file_path):
        """Get the raw metadata from the audio file using mid3v2 tool, expanding lists to separate frames."""
        result = run_external_tool(["mid3v2", "--list-raw", str(file_path)], "mid3v2")
        stdout = result.stdout
        lines = stdout.split('\n')
        new_lines = []
        for line in lines:
            if 'text=[' in line:
                match = re.search(r"text=\[([^\]]+)\]", line)
                if match:
                    list_str = match.group(1)
                    # Split by ', ' and strip quotes
                    items = [item.strip().strip("'\"") for item in list_str.split(',')]
                    frame_id = line.split('(')[0]
                    for item in items:
                        new_lines.append(f"{frame_id}: {item}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)

    @staticmethod
    def get_artists(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('artists', [])

    @staticmethod
    def get_title(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('title')

    @staticmethod
    def get_album(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('album')

    @staticmethod
    def get_year(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('year')

    @staticmethod
    def get_genre(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('genre')

    @staticmethod
    def get_comment(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('comment')

    @staticmethod
    def get_track(file_path):
        metadata = ID3v2MetadataGetter.get_metadata(file_path)
        return metadata.get('track')

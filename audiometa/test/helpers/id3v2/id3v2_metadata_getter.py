"""
id3v2_metadata_getter.py
Helper for extracting ID3v2 metadata from audio files.
"""



from audiometa.test.helpers.common.external_tool_runner import run_external_tool



class ID3v2MetadataGetter:
    """Helper class to get ID3v2 metadata from audio files using the id3v2 tool."""
    @staticmethod
    def get_raw_metadata(file_path):
        """
        Runs id3v2 tool and returns its output as a string in the format FRAMEID=value, e.g. TPE1=Artist One;Artist Two;Artist Three
        """
        result = run_external_tool(["id3v2", "-l", str(file_path)], "id3v2")
        lines = result.stdout.splitlines()
        parsed_lines = []
        for line in lines:
            # Match lines like: FRAMEID (Description): Value
            if "(" in line and "):" in line:
                frame_id = line.split(" ", 1)[0]
                value = line.split("):", 1)[-1].strip()
                parsed_lines.append(f"{frame_id}={value}")
            else:
                parsed_lines.append(line)
        return "\n".join(parsed_lines)


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

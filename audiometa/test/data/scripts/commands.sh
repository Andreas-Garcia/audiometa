
# Metadata Command Reference
#
# PURPOSE:
#     Reference file containing command-line examples for reading and writing metadata in various audio formats.
#
# USAGE:
#     This is a reference file, not an executable script. Use it to look up commands for metadata manipulation.
#
# KEY COMMANDS:
#     - ID3v1: Read/write using id3v2 tool
#     - ID3v2: Read/write using mid3v2 tool
#     - RIFF: Read using mediainfo tool
#     - Vorbis: Read/write using metaflac tool
#     - Rating Support: Setting ratings in different formats
#
# DEPENDENCIES:
#     - id3v2 - ID3 tag manipulation
#     - mid3v2 - ID3v2 tag manipulation (from python-mutagen)
#     - metaflac - FLAC metadata manipulation
#     - mediainfo - RIFF metadata reading
#     - ffmpeg - Audio processing
#
# INSTALLATION:
#     pip install mutagen
#     brew install id3v2 flac mediainfo ffmpeg
#

# Metadata Command Reference

## ID3v1 Tags
### Read ID3v1 tags
id3v2 -l1 file.mp3                    # List ID3v1 tags only
id3v2 -l1 file.mp3 2>/dev/null || echo "No ID3v1 tags found"

### Write ID3v1 tags
id3v2 \
    --comment "COMMENT" \
    --artist "ARTIST" \
    --album "ALBUM" \
    --song "TITLE" \
    --year "YEAR" \
    --track "TRACK" \
    --genre "254" \
    --id3v1-only \
    "test.mp3"

### ID3v1 field limits
# Title: 30 chars, Artist: 30 chars, Album: 30 chars
# Year: 4 chars, Comment: 28 chars (ID3v1.1), Track: 1 byte, Genre: 1 byte

## ID3v2 Tags
### Read ID3v2 tags
mid3v2 -l "files/metadata=long a_id3v2.flac"    # List all ID3v2 tags
mid3v2 -l test.mp3 | grep "TIT2"               # Find specific frame
mutagen-inspect test.mp3                        # Detailed inspection

### Write basic ID3v2 tags
id3v2 --artist "Artist Name" test.flac
id3v2 --album "Album Name" test.flac
id3v2 --song "Song Title" test.flac

### Write multiple tags at once
id3v2 \
    --artist "Artist Name" \
    --album "Album Name" \
    --song "Song Title" \
    --year "2024" \
    --genre "Rock" \
    test.flac

### Write extended ID3v2 tags
mid3v2 \
    --TXXX "MOOD:Happy" \
    --TXXX "ISRC:USXXX9999999" \
    --TCOM "Composer Name" \
    --TPE2 "Album Artist" \
    test.mp3

### Set ratings (POPM frames)
mid3v2 --POPM "Windows Media Player 9 Series:128" test.mp3    # 50% rating
mid3v2 --POPM "kid3:128" test.mp3                             # 50% rating
mid3v2 --POPM "Traktor:153" test.mp3                          # 60% rating
mid3v2 --POPM "iTunes:255" test.mp3                           # 100% rating

### Remove ID3v2 tags
ffmpeg -i "input.flac" -map_metadata -1 -c:a copy "output.flac"    # Remove all metadata
mid3v2 --delete-all test.mp3                                        # Remove all ID3v2 tags

## RIFF/WAV Metadata
### Read RIFF metadata
mediainfo "rating_id3v2=3 star.wav"                    # Human-readable format
mediainfo --Output=JSON "test.wav"                      # JSON format
bwfmetaedit --out-core "test.wav"                      # Technical details

### Write RIFF metadata
bwfmetaedit \
    --INAM "Title" \
    --IART "Artist" \
    --IPRD "Album" \
    --IGNR "Genre" \
    --ICRD "2024" \
    test.wav

## Vorbis Comments (FLAC/OGG)
### Read Vorbis comments
metaflac --list test.flac                              # List all Vorbis comments
metaflac --list --block-type=VORBIS_COMMENT test.flac  # Vorbis comments only
metaflac --list --tag=ARTIST test.flac                 # Specific tag

### Write Vorbis comments
metaflac --set-tag="TITLE=Song Title" test.flac
metaflac --set-tag="ARTIST=Artist Name" test.flac
metaflac --set-tag="ALBUM=Album Name" test.flac

### Write multiple Vorbis comments
metaflac \
    --set-tag="TITLE=Song Title" \
    --set-tag="ARTIST=Artist Name" \
    --set-tag="ALBUM=Album Name" \
    --set-tag="DATE=2024" \
    --set-tag="GENRE=Rock" \
    test.flac

### Set ratings in Vorbis
metaflac --remove-tag=RATING --set-tag="RATING=80" test.flac    # 80% rating (0-255)
metaflac --set-tag="RATING=255" test.flac                       # 100% rating

### Remove Vorbis comments
metaflac --remove-all-tags test.flac                            # Remove all Vorbis comments
metaflac --remove-tag=ARTIST test.flac                         # Remove specific tag

## Troubleshooting
### Check if tools are installed
which id3v2 mid3v2 metaflac bwfmetaedit mediainfo

### Install missing tools
# macOS with Homebrew
brew install id3v2 flac bwfmetaedit mediainfo

# Install mutagen (provides mid3v2, mutagen-inspect)
pip install mutagen

### Common issues
# Permission denied
chmod +x script.sh

# File not found
ls -la test.mp3

# No metadata found
file test.mp3  # Check file type


#!/usr/bin/env python3
"""One-off script to set full metadata on recording=queen_wearethechampions.mp3 using the library."""

from pathlib import Path

from audiometa import update_metadata
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey

ASSETS = Path(__file__).resolve().parent.parent / "audiometa" / "test" / "assets"
FILE = ASSETS / "recording=queen_wearethechampions.mp3"

LYRICS = """
I've paid my dues
Time after time
I've done my sentence
But committed no crime
And bad mistakes
I've made a few
I've had my share of sand
Kicked in my face
But I've come through

And we mean to go on and on and on

We are the champions, my friends
And we'll keep on fighting till the end
We are the champions
We are the champions
No time for losers
'Cause we are the champions of the world
""".strip()

QUEEN_METADATA = {
    UnifiedMetadataKey.TITLE: "We Are the Champions",
    UnifiedMetadataKey.ARTISTS: ["Queen"],
    UnifiedMetadataKey.ALBUM: "News of the World",
    UnifiedMetadataKey.ALBUM_ARTISTS: ["Queen"],
    UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Arena Rock"],
    UnifiedMetadataKey.RELEASE_DATE: "1977-10-28",
    UnifiedMetadataKey.TRACK_NUMBER: "4/11",
    UnifiedMetadataKey.DISC_NUMBER: 1,
    UnifiedMetadataKey.DISC_TOTAL: 1,
    UnifiedMetadataKey.BPM: 72,
    UnifiedMetadataKey.COMPOSERS: ["Freddie Mercury"],
    UnifiedMetadataKey.PUBLISHER: "Queen Music Ltd",
    UnifiedMetadataKey.COPYRIGHT: "© 1977 Queen Productions Ltd",
    UnifiedMetadataKey.COMMENT: "From the album News of the World. Single released 1977.",
    UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: LYRICS,
    UnifiedMetadataKey.RATING: 85,
    UnifiedMetadataKey.LANGUAGE: "eng",
    UnifiedMetadataKey.ISRC: "GBUM71029604",
    UnifiedMetadataKey.MUSICBRAINZ_TRACKID: "f3922a36-1c2e-4b2d-9b3e-8a1d4c5e6f7b",
    UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: ["a3cb23fc-acd3-4ce0-8f36-1e4aa6e2b1bc"],
}

if __name__ == "__main__":
    if not FILE.exists():
        msg = f"File not found: {FILE}"
        raise SystemExit(msg)
    update_metadata(
        FILE,
        QUEEN_METADATA,
        normalized_rating_max_value=100,
        warn_on_unsupported_field=True,
    )

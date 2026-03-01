Hi there

I'm glad to share that AudioMeta Python 1.0.0 is out 🎵 It's an open-source library that reads and writes metadata across MP3, FLAC, and WAV — one API for ID3v1, ID3v2, Vorbis, and RIFF. I've been building it on my own, and it's already passed 12,000 downloads.

📦 Install:

pip install audiometa-python

⌨️ From the CLI:

audiometa read song.mp3

audiometa write song.mp3 --title "New Title" --artist "Artist Name"

audiometa unified song.flac --format table

🐍 From Python:

from audiometa import get_unified_metadata, update_metadata, UnifiedMetadataKey

metadata = get_unified_metadata("song.mp3")

update_metadata("track.flac", {

    UnifiedMetadataKey.TITLE: "New Title",

    UnifiedMetadataKey.ARTISTS: ["Artist Name"],

})

Use it for library management, metadata cleanup, format migration, or batch updates. Python 3.12+, cross‑platform, Apache 2.0. Contributions welcome.

⭐ Repo: https://lnkd.in/dhdmD6Kp

💜 Sponsor: https://lnkd.in/d2fAUrYs

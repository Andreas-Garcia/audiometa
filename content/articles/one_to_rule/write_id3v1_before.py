#!/usr/bin/env python3
"""Write ID3v1 tags to demo_id3v1_before.mp3 for the before_only_id3v1.tape demo."""
from pathlib import Path

from mutagen.id3 import ID3, TIT2, TPE1, ID3v1SaveOptions

path = Path(__file__).resolve().parent / "demo_id3v1_before.mp3"
tags = ID3(path)
tags.add(TIT2(encoding=0, text=["Demo Title"]))
tags.add(TPE1(encoding=0, text=["Demo Artist"]))
tags.save(v1=ID3v1SaveOptions.CREATE)

#!/usr/bin/env python3
"""Interactive REPL-style demo for get_full_metadata()."""

import sys
import time


def slow_print(text: str, delay: float = 0.015) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def demo() -> None:
    slow_print(">>> from audiometa import get_full_metadata", delay=0.02)
    time.sleep(0.3)

    slow_print('>>> metadata = get_full_metadata("sample.mp3")', delay=0.02)
    time.sleep(0.5)

    from audiometa import get_full_metadata

    metadata = get_full_metadata("audiometa/test/assets/sample.mp3")

    slow_print(">>> metadata['unified_metadata']", delay=0.015)
    time.sleep(0.2)
    unified = metadata["unified_metadata"]
    print("{")
    print(f"  'title': {unified.get('title')},")
    print(f"  'artists': {unified.get('artists')},")
    print(f"  'album': {unified.get('album')}")
    print("}")
    time.sleep(1.5)

    slow_print(">>> metadata['technical_info']", delay=0.015)
    time.sleep(0.2)
    tech = metadata["technical_info"]
    print("{")
    print(f"  'duration': {tech['duration_seconds']:.1f}s,")
    print(f"  'bitrate': {tech['bitrate_bps']//1000}kbps,")
    print(f"  'sample_rate': {tech['sample_rate_hz']}Hz,")
    print(f"  'channels': {tech['channels']}")
    print("}")
    time.sleep(1.5)

    slow_print(">>> list(metadata['raw_metadata'].keys())", delay=0.015)
    time.sleep(0.2)
    print(list(metadata["raw_metadata"].keys()))
    time.sleep(1.5)

    slow_print(">>> # Complete metadata in one function!", delay=0.02)
    time.sleep(0.5)
    print(">>> ")


if __name__ == "__main__":
    demo()

#!/usr/bin/env python3
"""Interactive REPL-style demo for get_full_metadata() - FIXED VERSION"""

import time
import sys

def slow_print(text, delay=0.015):
    """Print text with typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def demo():
    # Import statement - immediate start
    slow_print(">>> from audiometa import get_full_metadata", delay=0.02)
    time.sleep(0.3)

    # Call the function
    slow_print('>>> metadata = get_full_metadata("sample.mp3")', delay=0.02)
    time.sleep(0.5)

    # Now execute and show results
    from audiometa import get_full_metadata
    metadata = get_full_metadata("audiometa/test/assets/sample.mp3")

    # Show unified metadata
    slow_print(">>> metadata['unified_metadata']", delay=0.015)
    time.sleep(0.2)
    unified = metadata['unified_metadata']
    # Show only key fields
    print(f"{{")
    print(f"  'title': {unified.get('title')},")
    print(f"  'artists': {unified.get('artists')},")
    print(f"  'album': {unified.get('album')}")
    print(f"}}")
    time.sleep(1.5)

    # Show technical info
    slow_print(">>> metadata['technical_info']", delay=0.015)
    time.sleep(0.2)
    tech = metadata['technical_info']
    print(f"{{")
    print(f"  'duration': {tech['duration_seconds']:.1f}s,")
    print(f"  'bitrate': {tech['bitrate_bps']//1000}kbps,")
    print(f"  'sample_rate': {tech['sample_rate_hz']}Hz,")
    print(f"  'channels': {tech['channels']}")
    print(f"}}")
    time.sleep(1.5)

    # Show raw metadata available
    slow_print(">>> list(metadata['raw_metadata'].keys())", delay=0.015)
    time.sleep(0.2)
    print(list(metadata['raw_metadata'].keys()))
    time.sleep(1.5)

    # Final message
    slow_print(">>> # Complete metadata in one function!", delay=0.02)
    time.sleep(0.5)
    print(">>> ")

if __name__ == "__main__":
    demo()

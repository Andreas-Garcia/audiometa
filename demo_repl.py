#!/usr/bin/env python3
"""Interactive REPL-style demo for get_full_metadata()"""

import time
import sys

def slow_print(text, delay=0.03):
    """Print text with typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def demo():
    print("Python 3.12.0")
    print('Type "help", "copyright", "credits" or "license" for more information.')

    # Import statement
    slow_print(">>> from audiometa import get_full_metadata")
    time.sleep(0.5)

    # Call the function
    slow_print('>>> metadata = get_full_metadata("sample.mp3")')
    time.sleep(0.5)

    # Now execute and show results
    from audiometa import get_full_metadata
    metadata = get_full_metadata("audiometa/test/assets/sample.mp3")

    # Show unified metadata
    slow_print(">>> metadata['unified_metadata']", delay=0.02)
    time.sleep(0.3)
    print(metadata['unified_metadata'])
    time.sleep(1)

    # Show technical info
    slow_print(">>> metadata['technical_info']", delay=0.02)
    time.sleep(0.3)
    tech = metadata['technical_info']
    print(f"{{'duration_seconds': {tech['duration_seconds']:.2f}, 'bitrate_bps': {tech['bitrate_bps']}, 'sample_rate_hz': {tech['sample_rate_hz']}, 'channels': {tech['channels']}, 'format': '{tech['audio_format_name']}'}}")
    time.sleep(1)

    # Show raw metadata formats available
    slow_print(">>> list(metadata['raw_metadata'].keys())", delay=0.02)
    time.sleep(0.3)
    print(list(metadata['raw_metadata'].keys()))
    time.sleep(1)

    # Show format priorities
    slow_print(">>> metadata['format_priorities']", delay=0.02)
    time.sleep(0.3)
    print(metadata['format_priorities'])
    time.sleep(1.5)

    # Final message
    slow_print(">>> # One function - Complete metadata access!", delay=0.02)
    time.sleep(0.5)
    print(">>> ")

if __name__ == "__main__":
    demo()

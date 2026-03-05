#!/usr/bin/env python3
"""AudioMeta - Quick Demo for Twitter"""
from audiometa import get_full_metadata

print("🎵 AudioMeta - Get Full Metadata Demo\n")

# Analyze audio file
metadata = get_full_metadata("audiometa/test/assets/sample.mp3")

# Show unified metadata
print("📊 UNIFIED METADATA:")
for key, value in list(metadata['unified_metadata'].items())[:4]:
    print(f"  • {key}: {value}")

# Show technical info
tech = metadata['technical_info']
print(f"\n🔧 TECHNICAL INFO:")
print(f"  • Duration: {tech['duration_seconds']:.2f}s")
print(f"  • Bitrate: {tech['bitrate_bps']//1000} kbps")
print(f"  • Format: {tech['audio_format_name']}")

# Show raw metadata
print(f"\n📝 RAW METADATA:")
for fmt in ['id3v2', 'id3v1']:
    if metadata['raw_metadata'][fmt]:
        print(f"  • {fmt.upper()}: Available")

print("\n✅ One function - Complete metadata access!")
print("   pip install audiometa-python")

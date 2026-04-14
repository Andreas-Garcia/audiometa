# Read Vorbis comments (FLAC) with metaflac. Uses output/work/demo_read_vorbis.flac (copy of samples/sample.flac from video script).
Output output/work/read_vorbis_metaflac.gif


Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms
Env HOME "@@ONE_TO_RULE_ABS@@"


Sleep 300ms

Type "echo '=== Vorbis (FLAC): metaflac'"
Enter
Sleep 1s

Type "(metaflac --list --block-type=VORBIS_COMMENT output/work/demo_read_vorbis.flac 2>/dev/null | head -14; echo '...')"
Enter
Sleep 5s

# Before only (Vorbis): read → update → read (metaflac); for side-by-side with after_only_vorbis.tape
# Half width (600). Run from repo root with venv. Requires metaflac on PATH.
# Use run_demo_side_by_side_vorbis.sh (in article dir) to copy sample.flac to article dir before recording.
Output content/articles/one_to_rule/output/before_only_vorbis.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== Read (metaflac)'"
Enter
Sleep 1s

Type "(metaflac --list --block-type=VORBIS_COMMENT content/articles/one_to_rule/demo_vorbis_before.flac 2>/dev/null | head -12; echo '...')"
Enter
Sleep 3s

Type "echo '=== Update (metaflac)'"
Enter
Sleep 1s

Type "metaflac --set-tag=TITLE='Demo Title' --set-tag=ARTIST='Demo Artist' content/articles/one_to_rule/demo_vorbis_before.flac"
Enter
Sleep 2s

Type "echo '=== Read (metaflac)'"
Enter
Sleep 1s

Type "(metaflac --list --block-type=VORBIS_COMMENT content/articles/one_to_rule/demo_vorbis_before.flac 2>/dev/null | head -12; echo '...')"
Enter
Sleep 3s

# After only (Vorbis): read → update → read (audiometa); for side-by-side with after_only_vorbis.tape
# Half width (600). Run from repo root with venv.
# Use run_demo_side_by_side_vorbis.sh (in article dir) to copy sample.flac to article dir before recording.
Output content/articles/one_to_rule/output/after_only_vorbis.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== Read (audiometa)'"
Enter
Sleep 1s

Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/demo_vorbis_after.flac --color | head -18; echo '...')"
Enter
Sleep 3s

Type "echo '=== Update (audiometa)'"
Enter
Sleep 1s

Type "audiometa write content/articles/one_to_rule/demo_vorbis_after.flac --title 'Demo Title' --artist 'Demo Artist'"
Enter
Sleep 2s

Type "echo '=== Read (audiometa)'"
Enter
Sleep 1s

Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/demo_vorbis_after.flac --color | head -18; echo '...')"
Enter
Sleep 3s

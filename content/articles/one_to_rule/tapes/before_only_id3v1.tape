# Before only (ID3v1): write with mutagen (legacy); for video panel.
# Half width (600). Run from repo root with venv. Copies sample.mp3 to demo_id3v1_before.mp3.
Output content/articles/one_to_rule/output/before_only_id3v1.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 600
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

Type "echo '=== Before: write ID3v1 (mutagen)'"
Enter
Sleep 1s

Type "cp content/articles/one_to_rule/sample.mp3 content/articles/one_to_rule/demo_id3v1_before.mp3"
Enter
Sleep 1s

Type "python3 content/articles/one_to_rule/write_id3v1_before.py"
Enter
Sleep 2s

Type "echo '=== Read back'"
Enter
Sleep 1s

Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/demo_id3v1_before.mp3 --format table --color | head -18; echo '...')"
Enter
Sleep 4s

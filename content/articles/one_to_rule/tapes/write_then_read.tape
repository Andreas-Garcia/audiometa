# Write then read demo – AudioMeta CLI (social / docs)
# Run from repo root with venv: vhs content/articles/one_to_rule/tapes/write_then_read.tape
# Uses a copy of content/articles/one_to_rule/sample.mp3 so the tracked file is not modified.
Output content/articles/one_to_rule/output/write_then_read.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 1200
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

# Intro
Type "echo '=== AudioMeta – Write metadata, then read it back'"
Enter
Sleep 2s

# Copy sample so we don't modify the tracked file
Type "cp content/articles/one_to_rule/sample.mp3 content/articles/one_to_rule/demo_write.mp3"
Enter
Sleep 1s

# Write title and artist
Type "audiometa write content/articles/one_to_rule/demo_write.mp3 --title 'Demo Title' --artist 'Demo Artist'"
Enter
Sleep 2s

# Read back (table, truncated)
Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/demo_write.mp3 --format table --color | head -26; echo '...')"
Enter
Sleep 6s

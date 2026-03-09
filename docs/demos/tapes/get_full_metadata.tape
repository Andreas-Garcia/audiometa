# Get full metadata demo – AudioMeta CLI (social / docs)
# Run from repo root with venv: vhs docs/demos/tapes/get_full_metadata.tape
# Audio: docs/demos/sample.mp3 (tracked). Output: docs/demos/output/<name>.gif
Output docs/demos/output/get_full_metadata.gif

Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 1200
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms

# Intro
Type "echo '=== AudioMeta – Get full metadata (JSON, YAML, table)'"
Enter
Sleep 1s

# Table view
Type "audiometa read docs/demos/sample.mp3 --format table"
Enter
Sleep 7s

# Full metadata – JSON
Type "audiometa read docs/demos/sample.mp3 --format json"
Enter
Sleep 6s

# Same track – YAML
Type "audiometa read docs/demos/sample.mp3 --format yaml"
Enter
Sleep 4s

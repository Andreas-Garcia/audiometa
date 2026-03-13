# Get full metadata demo – AudioMeta CLI (social / docs)
# Run from repo root with venv: vhs content/articles/one_to_rule/tapes/get_full_metadata.tape
# Audio: content/articles/one_to_rule/sample.mp3 (tracked). Output: content/articles/one_to_rule/output/<name>.gif
# env -u NO_COLOR ensures color is shown when the environment has NO_COLOR set (CLI honors NO_COLOR over --color).
Output content/articles/one_to_rule/output/get_full_metadata.gif

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
Sleep 2s

# Table view (truncated; "..." indicates more output)
Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/sample.mp3 --format table --color | head -26; echo '...')"
Enter
Sleep 8s

# Full metadata – JSON (truncated so output fits viewport)
Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/sample.mp3 --format json --color | head -26; echo '...')"
Enter
Sleep 8s

# Same track – YAML (truncated)
Type "(env -u NO_COLOR audiometa read content/articles/one_to_rule/sample.mp3 --format yaml --color | head -26; echo '...')"
Enter
Sleep 8s

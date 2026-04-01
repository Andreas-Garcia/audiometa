# Before/after demo – format-specific tool vs one AudioMeta command (social / docs)
# Run with repo runner: bash content/articles/one_to_rule/run_vhs_tape.sh before_after_one_command.tape
# Requires: audiometa (Require) and mid3v2 on PATH (for "before" step; from mutagen).
# Audio: sample.mp3 in article dir (tracked). Output: output/<name>.gif (no cd is typed in the tape).
Output output/before_after_one_command.gif


Require audiometa

Set Shell "bash"
Set FontSize 16
Set Width 1200
Set Height 700
Set Padding 20
Set Theme "Dracula"
Set TypingSpeed 50ms
Env HOME "@@ONE_TO_RULE_ABS@@"


Sleep 300ms

# Intro: before = format-specific tool
Type "echo '=== Before: format-specific tool (mid3v2 for MP3)'"
Enter
Sleep 2s

# Before: mid3v2 list (truncated)
Type "(mid3v2 -l sample.mp3 2>/dev/null | head -26; echo '...')"
Enter
Sleep 5s

# Transition: after = one command for any format
Type "echo '=== After: one command for any format (MP3, FLAC, WAV)'"
Enter
Sleep 2s

# After: audiometa unified (truncated)
Type "(env -u NO_COLOR audiometa unified sample.mp3 --format table --color | head -26; echo '...')"
Enter
Sleep 6s

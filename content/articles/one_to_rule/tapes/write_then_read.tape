# Write then read demo – AudioMeta CLI (social / docs)
# Run with repo runner: bash content/articles/one_to_rule/run_vhs_tape.sh write_then_read.tape
# Uses a copy of samples/sample.mp3 so the tracked file is not modified.
Output output/write_then_read.gif


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

# Intro
Type "echo '=== AudioMeta – Write metadata, then read it back'"
Enter
Sleep 2s

# Copy sample so we don't modify the tracked file
Type "cp samples/sample.mp3 demo_write.mp3"
Enter
Sleep 1s

# Write title and artist
Type "audiometa write demo_write.mp3 --title 'We Are the Champions' --artist 'Queen'"
Enter
Sleep 2s

# Read back (table, truncated)
Type "(env -u NO_COLOR audiometa unified demo_write.mp3 --format table --color | head -26; echo '...')"
Enter
Sleep 6s

import re

import pytest

from audiometa.cli import _colorize_json, _colorize_table, _colorize_yaml


def _strip_ansi(text: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", text)


@pytest.mark.unit
class TestColorizeJson:
    def test_keys_green(self):
        raw = '"title": "Hello"'
        out = _colorize_json(raw)
        assert "\033[32m" in out
        assert "title" in out
        assert _strip_ansi(out) == raw

    def test_string_values_yellow(self):
        raw = '"title": "Hello"'
        out = _colorize_json(raw)
        assert "\033[33m" in out
        assert "Hello" in out

    def test_numbers_cyan(self):
        raw = '"duration": 180'
        out = _colorize_json(raw)
        assert "\033[36m" in out
        assert "180" in out

    def test_literals_dim(self):
        raw = '"enabled": true'
        out = _colorize_json(raw)
        assert "\033[2m" in out
        assert "true" in out

    def test_reset_present(self):
        raw = '{"key": "val"}'
        out = _colorize_json(raw)
        assert "\033[0m" in out


@pytest.mark.unit
class TestColorizeTable:
    def test_section_headers_bold_cyan(self):
        raw = "=== UNIFIED METADATA ==="
        out = _colorize_table(raw)
        assert "\033[1;36m" in out
        assert "UNIFIED METADATA" in out

    def test_key_value_line(self):
        raw = "title               : My Song"
        out = _colorize_table(raw)
        assert "\033[32m" in out
        assert "\033[33m" in out
        assert "title" in out
        assert "My Song" in out

    def test_continuation_line_colored_as_value(self):
        raw = "title               : Line one\nLine two"
        out = _colorize_table(raw)
        assert "\033[33m" in out
        assert "Line one" in out
        assert "Line two" in out


@pytest.mark.unit
class TestColorizeYaml:
    def test_key_green_value_yellow(self):
        raw = "title: My Album"
        out = _colorize_yaml(raw)
        assert "\033[32m" in out
        assert "\033[33m" in out
        assert "title" in out
        assert "My Album" in out

    def test_continuation_line_colored(self):
        raw = "lyrics: First line\nSecond line"
        out = _colorize_yaml(raw)
        assert "\033[33m" in out
        assert "First line" in out
        assert "Second line" in out

    def test_empty_value_key_only_colored(self):
        raw = "empty:"
        out = _colorize_yaml(raw)
        assert "\033[32m" in out
        assert "empty" in out

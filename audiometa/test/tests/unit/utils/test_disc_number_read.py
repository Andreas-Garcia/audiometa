import pytest

from audiometa.utils.disc_number_read import (
    parse_disc_number_from_combined_str,
    parse_disc_total_from_combined_str,
    parse_explicit_non_negative_disctotal,
)


@pytest.mark.unit
class TestDiscNumberReadParsing:
    @pytest.mark.parametrize(
        ("s", "expected"),
        [
            ("1", 1),
            ("01", 1),
            ("1/2", 1),
            ("1-2", 1),
            ("99/100", 99),
        ],
    )
    def test_parse_disc_number_ok(self, s, expected):
        assert parse_disc_number_from_combined_str(s) == expected

    @pytest.mark.parametrize(
        "s",
        ["", "1/2/3", "x", "1-", "-1", "1/"],
    )
    def test_parse_disc_number_none(self, s):
        assert parse_disc_number_from_combined_str(s) is None

    @pytest.mark.parametrize(
        ("s", "expected"),
        [
            ("1/2", 2),
            ("1-2", 2),
            ("0/5", 5),
        ],
    )
    def test_parse_disc_total_from_combined_ok(self, s, expected):
        assert parse_disc_total_from_combined_str(s) == expected

    @pytest.mark.parametrize(
        "s",
        ["1", "1/2/3", "", "x"],
    )
    def test_parse_disc_total_from_combined_none(self, s):
        assert parse_disc_total_from_combined_str(s) is None

    @pytest.mark.parametrize(
        ("s", "expected"),
        [
            ("0", 0),
            ("2", 2),
            ("42", 42),
        ],
    )
    def test_parse_explicit_disctotal_ok(self, s, expected):
        assert parse_explicit_non_negative_disctotal(s) == expected

    @pytest.mark.parametrize(
        "s",
        ["", "bogus", "-1", "1.5"],
    )
    def test_parse_explicit_disctotal_none(self, s):
        assert parse_explicit_non_negative_disctotal(s) is None

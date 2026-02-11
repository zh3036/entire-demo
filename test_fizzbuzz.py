"""Tests for the configurable FizzBuzz module."""

from fizzbuzz import fizzbuzz, run, parse_rule, stats, main
import pytest


class TestFizzbuzz:
    def test_plain_number(self):
        assert fizzbuzz(1) == "1"
        assert fizzbuzz(7) == "7"

    def test_fizz(self):
        assert fizzbuzz(3) == "Fizz"
        assert fizzbuzz(9) == "Fizz"

    def test_buzz(self):
        assert fizzbuzz(5) == "Buzz"
        assert fizzbuzz(10) == "Buzz"

    def test_fizzbuzz(self):
        assert fizzbuzz(15) == "FizzBuzz"
        assert fizzbuzz(30) == "FizzBuzz"

    def test_custom_rules(self):
        rules = [(2, "Even"), (7, "Lucky")]
        assert fizzbuzz(2, rules) == "Even"
        assert fizzbuzz(7, rules) == "Lucky"
        assert fizzbuzz(14, rules) == "EvenLucky"
        assert fizzbuzz(3, rules) == "3"


class TestRun:
    def test_classic_range(self):
        result = run(1, 5)
        assert result == ["1", "2", "Fizz", "4", "Buzz"]

    def test_custom_start(self):
        result = run(14, 16)
        assert result == ["14", "FizzBuzz", "16"]


class TestParseRule:
    def test_valid_rule(self):
        assert parse_rule("7:Woof") == (7, "Woof")

    def test_invalid_format(self):
        with pytest.raises(Exception):
            parse_rule("bad")

    def test_non_integer_divisor(self):
        with pytest.raises(Exception):
            parse_rule("abc:Foo")

    def test_zero_divisor(self):
        with pytest.raises(Exception):
            parse_rule("0:Zero")


class TestStats:
    def test_classic_stats(self):
        s = stats(1, 15)
        assert s["total"] == 15
        assert s["replaced"] == 7  # 3,5,6,9,10,12,15
        assert s["numeric"] == 8

    def test_replacement_rate(self):
        s = stats(1, 15)
        assert s["replacement_rate"] == pytest.approx(46.7, abs=0.1)


class TestCLI:
    def test_json_output(self, capsys):
        main(["5", "--json"])
        captured = capsys.readouterr()
        import json
        result = json.loads(captured.out)
        assert result == ["1", "2", "Fizz", "4", "Buzz"]

    def test_stats_output(self, capsys):
        main(["15", "--stats"])
        captured = capsys.readouterr()
        assert "46.7%" in captured.out

import pytest
from findlike.format import BaseFormatter, JsonFormatter
from pathlib import Path
import json

# Sample test data
targets = [Path("file1.txt"), Path("file2.txt"), Path("file3.txt")]
scores = [0.8, 0.6, 0.9]


class TestBaseFormatter:
    @pytest.mark.parametrize("max_results, expected_length", [(2, 2), (5, 3)])
    def test_max_results(self, max_results, expected_length):
        formatter = BaseFormatter(targets, scores, max_results=max_results)
        output = formatter.format()
        assert len(output.split("\n")) == expected_length

    def test_show_scores(self):
        formatter = BaseFormatter(targets, scores, show_scores=True)
        output = formatter.format()
        assert all(
            any(char.isdigit() for char in line) for line in output.split("\n")
        )

    def test_hide_reference(self):
        formatter = BaseFormatter(targets, scores, hide_reference=True)
        output = formatter.format()
        assert len(output.split("\n")) == 2

    def test_prefix(self):
        formatter = BaseFormatter(targets, scores, prefix="PREFIX_")
        output = formatter.format()
        assert all(line.startswith("PREFIX_") for line in output.split("\n"))

    def test_heading(self):
        heading = "Sample Heading"
        formatter = BaseFormatter(targets, scores, heading=heading)
        output = formatter.format()
        assert output.split("\n")[0] == heading

    def test_threshold(self):
        formatter = BaseFormatter(targets, scores, threshold=0.7)
        output = formatter.format()
        assert len(output.split("\n")) == 2

    def test_absolute_paths(self):
        formatter = BaseFormatter(targets, scores, absolute_paths=True)
        output = formatter.format()
        assert all(Path(line).is_absolute() for line in output.split("\n"))


class TestJsonFormatter:
    def test_valid_json(self):
        formatter = JsonFormatter(targets, scores)
        output = formatter.format()
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            pytest.fail("Output is not valid JSON")

    @pytest.mark.parametrize(
        "show_scores, expected_keys",
        [(True, ["score", "target"]), (False, ["target"])],
    )
    def test_keys_in_json(self, show_scores, expected_keys):
        formatter = JsonFormatter(targets, scores, show_scores=show_scores)
        output = formatter.format()
        data = json.loads(output)
        for entry in data:
            assert set(entry.keys()) == set(expected_keys)

    def test_hide_reference(self):
        formatter = JsonFormatter(targets, scores, hide_reference=True)
        output = formatter.format()
        data = json.loads(output)
        assert len(data) == 2

    def test_threshold(self):
        formatter = JsonFormatter(targets, scores, threshold=0.7)
        output = formatter.format()
        data = json.loads(output)
        assert len(data) == 2

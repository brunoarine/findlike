from __future__ import annotations

import json
from pathlib import Path


class BaseFormatter:
    """Base class for formatting similarity search results.

    This class provides the foundation for formatting the results of a similarity search.
    It processes a list of target files and their corresponding similarity scores, then
    formats the output according to the specified options.

    Args:
        targets (list[Path]): List of paths to the target files.
        scores (list[float]): List of similarity scores corresponding to the targets.
        max_results (int, optional): Maximum number of results to display. Defaults to 10.
        show_scores (bool, optional): Whether to show the similarity scores. Defaults to False.
        hide_reference (bool, optional): Whether to hide the reference file (if present). Defaults to False.
        prefix (str, optional): Prefix to prepend to each line of the result. Defaults to "".
        heading (str, optional): Heading to be displayed at the top of the result. Defaults to "".
        threshold (float, optional): Minimum similarity score to include a result. Defaults to 0.0.
        absolute_paths (bool, optional): Whether to show absolute paths. Defaults to False.
        is_query (bool, optional): Indicates if the search was by a query string (as opposed to a reference file). Defaults to False.
        precision (int, optional): Number of decimal places to round the scores to. Defaults to 2.

    The `format` method returns the formatted output string.
    """

    def __init__(
        self,
        targets: list[Path],
        scores: list[float],
        max_results: int = 10,
        show_scores: bool = False,
        hide_reference: bool = False,
        prefix: str = "",
        heading: str = "",
        threshold: float = 0.0,
        absolute_paths: bool = False,
        is_query: bool = False,
        precision: int = 2,
    ):
        self.targets = targets
        self.scores = scores
        self.max_results = max_results
        self.show_scores = show_scores
        self.hide_reference = hide_reference
        self.prefix = prefix
        self.heading = heading
        self.threshold = threshold
        self.absolute_paths = absolute_paths
        self.is_query = is_query
        self.precision = precision

        self._scores_targets: list[tuple[float, Path]]
        self._format_targets()._zip_pairs()._filter_pairs()

    def _zip_pairs(self):
        self._scores_targets = list(zip(self.scores, self.targets))
        return self

    def _filter_pairs(self):
        """Remove reference doc if needed and limit list to max number of results."""

        # Sort pairs according to distance (descending).
        self._scores_targets = sorted(
            self._scores_targets, key=lambda x: x[0], reverse=True
        )

        # Remove entries whose score are below the threshold.
        self._scores_targets = [
            x for x in self._scores_targets if x[0] >= self.threshold
        ]

        # Apply precision
        self._scores_targets = [
            (round(score, self.precision), target)
            for (score, target) in self._scores_targets
        ]

        # Limit number of results, disregarding the first entry if `remove_reference`
        # flag was passed.
        start_pos = int(self.hide_reference and not self.is_query)
        range = slice(start_pos, start_pos + self.max_results)
        self._scores_targets = self._scores_targets[range]

        return self

    def _format_targets(self):
        if self.absolute_paths:
            self.targets = [x.resolve() for x in self.targets]
        return self

    def _format_score(self, score):
        return f"{score}" + " " if self.show_scores else ""

    def format(self):
        entries = []
        if self.heading:
            entries.append(self.heading)
        entries += [
            f"{self.prefix}{self._format_score(score)}{target}"
            for score, target in self._scores_targets
        ]
        output = "\n".join(entries)
        return output


class JsonFormatter(BaseFormatter):
    def format(self):
        if self.heading:
            print(self.heading)
        if self.show_scores:
            entries = [
                {"score": score, "target": str(target)}
                for score, target in self._scores_targets
            ]
        else:
            entries = [{"target": str(target)} for _, target in self._scores_targets]
        json_data = json.dumps(entries)
        return json_data

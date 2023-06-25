import json
from pathlib import Path


class BaseFormatter:
    """Format results in an org-compatible format with links.

    Args:
        input_filename (Path): path to the filename that will be used as
            reference.
        target_filenames (Path): Glob containing the path to the documents
            whose similarity with the input filename will be estimated.
        scores (array-like): List of similarity scores with the same number of
            documents in target_filenames plus one (accounting for the
            input_filename).
        num_results (int): How many similar entries to list at the end of the buffer.
        id_links (bool): Whether the resulting list of similar documents will
            point to ID property or filename. Recommend setting it to True
            if you use `org-roam' v2.
        show_scores (bool): Whether to prepend the results with the similarity score.
        remove_first (bool): Remove first result from the scores list. Useful if
            the source document is inside the same directory as the target documents,
            and you don't want to see it included in the list for obvious reasons.
            Default is False.
        prefix (str): Prefix to add to each item in the printed list.
        heading (str): List heading (title).

    Returns:
        List of org formatted links to the most similar documents, sorted in descending
        order of similarity.
    """

    def __init__(
        self,
        targets: list[Path],
        scores: list[float],
        max_results: int,
        show_scores: bool,
        remove_reference: bool,
        prefix: str,
        heading: str,
        threshold: float,
        absolute_paths: bool,
        is_query: bool
    ):
        self.targets = targets
        self.scores = scores
        self.max_results = max_results
        self.show_scores = show_scores
        self.remove_reference = remove_reference
        self.prefix = prefix
        self.heading = heading
        self.threshold = threshold
        self.absolute_paths = absolute_paths
        self.is_query = is_query

        self._format_targets()
        self._zip_pairs()
        self._filter_pairs()
    
    def _zip_pairs(self):
        self._scores_targets  = zip(self.scores, self.targets)
    
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

        # Limit number of results, disregarding the first entry if `remove_reference`
        # flag was passed.
        start_pos = int(self.remove_reference and not self.is_query)
        range = slice(start_pos, start_pos + self.max_results)
        self._scores_targets = self._scores_targets[range]
        
    
    def _format_targets(self):
        if self.absolute_paths:
            self.targets = [str(x.resolve()) for x in self.targets]
        else:
            self.targets = [str(x) for x in self.targets]

    def _format_score(self, score):
        return f"{score:.2f}" + " " if self.show_scores else ""
    
    def format(self):
        if self.heading:
            print(self.heading)
        entries = [
            f"{self.prefix}{self._format_score(score)}{target}"
            for score, target in self._scores_targets
        ]
        output = "\n".join(entries)
        return output


class JsonFormatter(BaseFormatter):
    def format(self):
        if self.heading:
            print(self.heading)
        entries = [
            {"score": score, "target": str(target)}
            for score, target in self._scores_targets
        ]
        json_data = json.dumps(entries)
        return json_data

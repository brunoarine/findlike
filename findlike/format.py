from typing import Callable
from rank_bm25 import BM25Okapi
import argparse
import functools
import os
import re
import sys
from itertools import compress
from pathlib import Path
from typing import Callable, List
import click
import orgparse

import numpy as np
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ioutils import get_relative_path

def format_orgmode(
    input_path: Path,
    targets: List[Path],
    scores: List[float],
    num_results: int,
    id_links: bool,
    show_scores: bool,
    remove_first: bool,
    prefix: str = "",
    heading: str = "",
) -> List[str]:
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
    results = zip(scores, targets)
    sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
    valid_results = sorted_results[int(remove_first) : num_results + int(remove_first)]
    formatted_results = []
    print(heading)
    print()
    for score, target in valid_results:
        org_content = orgparse.load(target)
        title = org_content.get_file_property("title")
        score_output = f"{score:.2f} " if show_scores else ""
        if id_links:
            target_id = org_content.get_property("ID")
            link_ref = f"id:{target_id}"
        else:
            # org-mode links use relative rather than absolute paths
            target_rel_path = get_relative_path(
                source=input_path, target=target
            )
            link_ref = f"file:{target_rel_path}"
        entry = f"{prefix}{score_output}[[{link_ref}][{title}]]"
        formatted_results.append(entry)
    return formatted_results


def format_json(
    input_path: Path,
    targets: List[Path],
    scores: List[float],
    num_results: int,
    id_links: bool,
    show_scores: bool,
    remove_first: bool,
    prefix: str = "",
    heading: str = "",
) -> list[str]:
    # TODO
    return [""]
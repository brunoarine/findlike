from .format import BaseFormatter, JsonFormatter
from rank_bm25 import BM25Okapi
import functools
import os
import re
import sys
from itertools import compress
from pathlib import Path
from typing import Callable, List
import click

import numpy as np
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import (
    Corpus,
    get_junkchars,
    get_stopwords,
    read_file,
    Processor,
)
from .wrappers import BM25, Tfidf

FILES_EXT = "*.org"

FORMATTER_CLASSES = {"plain": BaseFormatter, "json": JsonFormatter}

WORD_RE = re.compile(r"(?u)\b[a-z]{2,}\b")
URL_RE = re.compile(r"\S*https?:\S*")


@click.command()
@click.argument(
    "reference",
    type=click.Path(),
    nargs=1
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(),
    default=Path("."),
    help="directory to scan for similar documents",
    required=False,
)
@click.option(
    "--algorithm",
    "-a",
    type=str,
    default="tfidf",
    help="algorithm for creating the bag of words",
    required=False,
)
@click.option(
    "--number",
    "-n",
    type=int,
    default=10,
    help="number of similar documents",
    required=False,
)
@click.option(
    "--language",
    "-l",
    type=str,
    default="english",
    help="nltk's SnowBallStemmer language",
    required=False,
)
@click.option(
    "--min-words",
    "-m",
    type=int,
    default=0,
    help="minimum document size (in number of words) to be included in the corpus",
    required=False,
)
@click.option(
    "--prefix", "-p", type=str, default="", help="item prefix", required=False
)
@click.option(
    "--heading",
    "-H",
    type=str,
    default="",
    help="list heading",
    required=False,
)
@click.option(
    "--show-scores",
    "-s",
    is_flag=True,
    help="show cosine similarity scores (default: False)",
    required=False,
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="search for org files recursively (default: False)",
    required=False,
)
@click.option(
    "--id-links",
    "-I",
    is_flag=True,
    help="create ID links instead of FILE links (default: False)",
    required=False,
)
@click.option(
    "--remove-first",
    "-F",
    is_flag=True,
    help="remove first row from results (default: False)",
    required=False,
)
@click.option("--format", "-f", type=str, default="plain", required=False)
def cli(
    reference,
    directory,
    algorithm,
    number,
    language,
    min_words,
    prefix,
    heading,
    show_scores,
    recursive,
    id_links,
    remove_first,
    format,
):
    """Execute main function."""
    target = Path(reference)
    directory = Path(directory)
    documents_glob = (
        directory.rglob(FILES_EXT) if recursive else directory.glob(FILES_EXT)
    )

    documents_paths = [f for f in documents_glob]
    corpus = Corpus(paths=documents_paths, min_words=min_words)
    source_content = read_file(target)

    stemmer = SnowballStemmer(language).stem
    junkchars = get_junkchars()
    stopwords = get_stopwords()
    processor = Processor(
        junkchars=junkchars,
        stopwords=stopwords,
        stemmer=stemmer,
        lemmatize=False,
    )

    if algorithm == "bm25":
        model = BM25(processor=processor)
    else:
        model = Tfidf(processor=processor)

    # Add source content to list of possible words to avoid zero divisions.
    model.fit(corpus.documents_ + [source_content])
    scores = model.get_scores(source=source_content)

    config = dict(
        targets=corpus.paths_,
        scores=scores,
        num_results=number,
        show_scores=show_scores,
        id_links=id_links,
        remove_first=remove_first,
        prefix=prefix,
        heading=heading,
    )
    selected_class = FORMATTER_CLASSES.get(format)
    if selected_class:
        formatter = selected_class(**config)
    else:
        raise ValueError("Invalid format type")
    formatted_results = formatter.format()
    print(formatted_results)

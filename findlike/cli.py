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

import numpy as np
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import Corpus, get_junkchars, get_stopwords, read_file, Processor
from .wrappers import BM25, Tfidf
from .format import format_orgmode

FILES_EXT = "*.org"

WORD_RE = re.compile(r"(?u)\b[a-z]{2,}\b")
URL_RE = re.compile(r"\S*https?:\S*")

def parse_args():
    """Parse command line arguments."""
    p = argparse.ArgumentParser()
    p.add_argument(
        "--target",
        "-t",
        type=str,
        help="target (reference) document",
        required=True,
    )
    p.add_argument(
        "--directory",
        "-d",
        type=str,
        help="directory of files to search",
        required=True,
    )
    p.add_argument(
        "--algorithm",
        "-a",
        type=str,
        default="tfidf",
        help="algorithm for creating the embeddings",
        required=False,
    )
    p.add_argument(
        "--number",
        "-n",
        type=int,
        default=10,
        help="number of similar documents (default: 10)",
        required=False,
    )
    p.add_argument(
        "--language",
        "-l",
        type=str,
        default="english",
        help="nltk's SnowballStemmer language (default: english)",
        required=False,
    )
    p.add_argument(
        "--min-words",
        "-m",
        type=int,
        default=0,
        help="minimum document size (in number of words) to be included in the corpus",
        required=False,
    )
    p.add_argument(
        "--prefix",
        "-p",
        type=str,
        default="",
        help="item prefix",
        required=False,
    )
    p.add_argument(
        "--heading",
        type=str,
        default="",
        help="list heading",
        required=False,
    )
    p.add_argument(
        "--scores",
        "-s",
        action="store_true",
        help="show cosine similarity scores (default: False)",
        required=False,
    )
    p.add_argument(
        "--recursive",
        "-r",
        help="search for org files recursively (default: False)",
        action="store_true",
        required=False,
    ),
    p.add_argument(
        "--id-links",
        "-I",
        action="store_true",
        help="create ID links instead of FILE links (default: False)",
        required=False,
    )
    p.add_argument(
        "--remove-first",
        "-f",
        action="store_true",
        help="remove first row from results (default: False)",
        required=False,
    )
    return p.parse_args()


def cli():
    """Execute main function."""
    args = parse_args()
    target_path = Path(args.target)
    directory = Path(args.directory)
    num_results = args.number
    language = args.language
    show_scores = args.scores
    recursive = args.recursive
    id_links = args.id_links
    remove_first = args.remove_first
    min_words = args.min_words
    prefix = args.prefix
    heading = args.heading

    documents_glob = (
        directory.rglob(FILES_EXT) if recursive else directory.glob(FILES_EXT)
    )
    documents_paths = [f for f in documents_glob]
    corpus = Corpus(paths=documents_paths, min_words=min_words)
    source_content = read_file(target_path)

    stemmer = SnowballStemmer(language).stem
    junkchars = get_junkchars()
    stopwords = get_stopwords()
    processor = Processor(
        junkchars=junkchars,
        stopwords=stopwords,
        stemmer=stemmer,
        lemmatize=False,
    )

    if args.algorithm == "bm25":
        model = BM25(processor=processor)
    else:
        model = Tfidf(processor=processor)

    # Add source content to list of possible words to avoid zero divisions.
    model.fit(corpus.documents_ + [source_content])
    scores = model.get_scores(source=source_content)

    formatted_results = format_orgmode(
        input_path=target_path,
        targets=corpus.paths_,
        scores=scores,
        num_results=num_results,
        show_scores=show_scores,
        id_links=id_links,
        remove_first=remove_first,
        prefix=prefix,
        heading=heading,
    )

    for entry in formatted_results:
        print(entry)

   
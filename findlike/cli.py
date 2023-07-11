from __future__ import annotations

from pathlib import Path

import click
from nltk.stem import SnowballStemmer
from stop_words import get_stop_words

from .constants import ALGORITHM_CLASSES, FORMATTER_CLASSES, TEXT_FILE_EXT
from .preprocessing import (
    Corpus,
    Processor,
)
from .utils import collect_paths


@click.command()
@click.version_option()
@click.argument("reference-file", type=click.Path(), nargs=1, required=False)
@click.option(
    "-q",
    "--query",
    default=None,
    show_default=True,
    help="query option if no reference file is provided",
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(),
    default=Path("./"),
    show_default="current directory",
    help="directory to scan for similar files",
    required=False,
)
@click.option(
    "--filename-pattern",
    "-f",
    type=str,
    default=None,
    help="filename pattern matching",
    show_default="plain-text file extensions",
    required=False,
)
@click.option(
    "--recursive",
    "-R",
    is_flag=True,
    help="recursive search",
    required=False,
)
@click.option(
    "--algorithm",
    "-a",
    type=click.Choice(list(ALGORITHM_CLASSES.keys())),
    default="tfidf",
    show_default=True,
    help="text similarity algorithm",
    required=False,
)
@click.option(
    "--language",
    "-l",
    type=str,
    default="english",
    show_default=True,
    help="stemmer and stopwords language",
    required=False,
)
@click.option(
    "--min-chars",
    "-c",
    type=int,
    default=1,
    show_default=True,
    help="minimum document size (in number of characters) to be considered",
    required=False,
)
@click.option(
    "--absolute-paths",
    "-A",
    is_flag=True,
    help="show absolute rather than relative paths",
    required=False,
)
@click.option(
    "--max-results",
    "-m",
    type=int,
    default=10,
    show_default=True,
    help="maximum number of results",
    required=False,
)
@click.option(
    "--prefix",
    "-p",
    type=str,
    default="",
    show_default=True,
    help="result lines prefix",
    required=False,
)
@click.option(
    "--show-scores",
    "-s",
    is_flag=True,
    help="show similarity scores",
    required=False,
)
@click.option(
    "--hide-reference",
    "-h",
    is_flag=True,
    help="remove REFERENCE_FILE from results",
    required=False,
)
@click.option(
    "--ignore-front-matter",
    "-i",
    is_flag=True,
    help="ignore front-matter from supported markup languages",
    required=False,
)
@click.option(
    "--heading",
    "-H",
    type=str,
    default="",
    show_default=True,
    help="results list heading",
    required=False,
)
@click.option(
    "--format",
    "-F",
    type=click.Choice(list(FORMATTER_CLASSES.keys())),
    default="plain",
    show_default=True,
    show_choices=True,
    help="output format",
    required=False,
)
@click.option(
    "--threshold",
    "-t",
    type=float,
    default=0.0,
    show_default=True,
    help="minimum score for a result to be shown",
)
def cli(
    reference_file,
    directory,
    filename_pattern,
    algorithm,
    max_results,
    language,
    min_chars,
    prefix,
    heading,
    show_scores,
    recursive,
    hide_reference,
    query,
    format,
    threshold,
    absolute_paths,
    ignore_front_matter,
):
    """'findlike' is a program that scans a given directory and returns the most
    similar documents in relation to REFERENCE_FILE or --query QUERY.

    Example using a reference file:

    $ findlike -d /path/to/my/notes my_recipe.md

    Example using a query:

    $ findlike -q "There is only one good, knowledge, and one evil, ignorance"
    """

    # Put together the list of documents to be analyzed.
    directory_path = Path(directory)
    extensions: list[str] = (
        [filename_pattern] if filename_pattern else TEXT_FILE_EXT
    )
    document_paths = collect_paths(
        directory=directory_path, extensions=extensions, recursive=recursive
    )

    # Create a corpus with the collected documents.
    corpus = Corpus(
        paths=document_paths,
        min_chars=min_chars,
        ignore_front_matter=ignore_front_matter,
    )
    if reference_file:
        corpus.add_from_file(path=Path(reference_file), is_reference=True)
    elif query:
        corpus.add_from_query(query=query)
    else:
        raise click.UsageError(
            "Neither REFERENCE_FILE nor --query QUERY was provided."
        )

    # Set up the documents pre-processor.
    stemmer = SnowballStemmer(language).stem
    processor = Processor(
        stopwords=get_stop_words(language=language),
        stemmer=stemmer,
    )

    # Set up the similarity model.
    model = ALGORITHM_CLASSES[algorithm](processor=processor)
    model.fit(corpus.documents_)  # Add reference to avoid zero division
    scores = model.get_scores(source=corpus.reference_)

    # Format and print results.
    formatter = FORMATTER_CLASSES[format](
        targets=corpus.paths_,
        scores=scores,
        max_results=max_results,
        show_scores=show_scores,
        hide_reference=hide_reference,
        prefix=prefix,
        heading=heading,
        threshold=threshold,
        absolute_paths=absolute_paths,
        is_query=bool(query),
    )
    formatted_results = formatter.format()
    print(formatted_results)

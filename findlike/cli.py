from pathlib import Path

import click
from nltk.stem import SnowballStemmer

from .format import BaseFormatter, JsonFormatter
from .preprocessing import (
    Corpus,
    Processor,
    get_junkchars,
    get_stopwords,
    read_file,
)
from .wrappers import BM25, Tfidf

FILE_EXTENSIONS = ["*.org", "*.md", "*.txt", ".rst"]
FORMATTER_CLASSES = {"plain": BaseFormatter, "json": JsonFormatter}
ALGORITHM_CLASSES = {"bm25": BM25, "tfidf": Tfidf}


@click.command()
@click.version_option()
@click.argument("reference-file", type=click.Path(), nargs=1, required=False)
@click.option(
    "--directory",
    "-d",
    type=click.Path(),
    default=Path("."),
    help="directory to scan for similar documents (default: current)",
    required=False,
)
@click.option(
    "--algorithm",
    "-a",
    type=click.Choice(list(ALGORITHM_CLASSES.keys())),
    default="tfidf",
    help="algorithm for creating the bag of words (default: tfidf)",
    required=False,
)
@click.option(
    "--max-results",
    "-m",
    type=int,
    default=10,
    help="maximum number of results (default: 10)",
    required=False,
)
@click.option(
    "--language",
    "-l",
    type=str,
    default="english",
    help="stemmer and stopwords language (default: english)",
    required=False,
)
@click.option(
    "--min-words",
    "-n",
    type=int,
    default=0,
    help="minimum document size (in number of words) to be included in the corpus (default: 0)",
    required=False,
)
@click.option(
    "--prefix",
    "-p",
    type=str,
    default="",
    help="result lines prefix (default: None)",
    required=False,
)
@click.option(
    "--heading",
    "-H",
    type=str,
    default="",
    help="results list heading (default: None)",
    required=False,
)
@click.option(
    "--show-scores",
    "-s",
    is_flag=True,
    help="show similarity scores (default: False)",
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
    "--remove-first",
    "-F",
    is_flag=True,
    help="remove first row from results",
    required=False,
)
@click.option(
    "-q",
    "--query",
    default=None,
    help="query option if no reference file is provided",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(list(FORMATTER_CLASSES.keys())),
    default="plain",
    help="output format (default: plain)",
    required=False,
)
@click.option(
    "--threshold",
    "-t",
    type=float,
    default=0.05,
    help="minimum score for a result to be shown (default: 0.0)",
)
def cli(
    reference_file,
    directory,
    algorithm,
    max_results,
    language,
    min_words,
    prefix,
    heading,
    show_scores,
    recursive,
    remove_first,
    query,
    format,
    threshold
):
    """'findlike' is a program that scans a given directory and returns the most
    similar documents in relation to REFERENCE_FILE or --query QUERY."""

    # Set up the reference text.
    if reference_file:
        reference_content = read_file(Path(reference_file))
    elif query:
        reference_content = query
    else:
        raise click.UsageError(
            "Neither REFERENCE_FILE nor --query QUERY was provided."
        )

    # Put together the list of documents to be analyzed.
    directory_path = Path(directory)
    glob_func = directory_path.rglob if recursive else directory_path.glob
    documents_glob = [
        file for extension in FILE_EXTENSIONS for file in glob_func(extension)
    ]
    documents_paths = [f for f in documents_glob]

    # Create a corpus with the collected documents.
    corpus = Corpus(paths=documents_paths, min_words=min_words)

    # Set up the documents pre-processor.
    stemmer = SnowballStemmer(language).stem
    junkchars = get_junkchars()
    stopwords = get_stopwords()
    processor = Processor(
        junkchars=junkchars,
        stopwords=stopwords,
        stemmer=stemmer,
        lemmatize=False,
    )

    # Set up the similarity model.
    model = ALGORITHM_CLASSES[algorithm](processor=processor)
    model.fit(
        corpus.documents_ + [reference_content]
    )  # Add reference to avoid zero division
    scores = model.get_scores(source=reference_content)

    # Format and print results.
    format_config = dict(
        targets=corpus.paths_,
        scores=scores,
        num_results=max_results,
        show_scores=show_scores,
        remove_first=remove_first,
        prefix=prefix,
        heading=heading,
        threshold=threshold
    )
    formatter = FORMATTER_CLASSES[format](**format_config)
    formatted_results = formatter.format()
    print(formatted_results)

# findlike

`findlike` is a command-line tool to help discover similar or related files.
Under the hood, it uses Python and
[scikit-learn](https://github.com/scikit-learn/scikit-learn) for text feature
extraction, and [nltk](https://github.com/nltk/nltk) for text pre-processing.
More specifically, this tool recursively scans a given directory for the
specified files,tokenize them, replace each token with its respective
linguistic stem, generate a TF-IDF sparse matrix, and calculate the cosine
similarity between these documents and the buffer you are currently working on.

## Installation

TODO

## Usage

TODO

## Configuration

TODO

## Benchmarking

TODO

## Changelog

### 2023-??-?? - v0.1

- First version.
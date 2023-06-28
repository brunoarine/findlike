# findlike

[![PyPI](https://img.shields.io/pypi/v/findlike.svg)](https://pypi.org/project/findlike/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/brunoarine/findlike/blob/master/LICENSE)
[![Tests](https://github.com/brunoarine/findlike/workflows/Test/badge.svg)](https://github.com/brunoarine/findlike/actions?query=workflow%3ATest)

`findlike` is a command-line tool written in Python that retrieves a list of similar files in relation to a reference file or an ad-hoc query. The tool is highly configurable and can be used as backend for other programs (e.g. personal knowledge manage systems, Emacs, etc.) 

Features: 

- Choose between BM25 and TF-IDF + cosine distance for similarity calculation
- Recursive search option
- Control over output format, document size to consider, maximum results to show, etc.
- Multilingual support

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Example](#examples)
- [License](#license)

## Prerequisites

- Python 3.8 or higher
- Additional dependencies as listed in the `requirements.txt` file

## Installation

### Using `pip` (single user)

To install `findlike` for your user only, run the following command in your terminal:

```bash
pip install --user findlike
```

### Using `pip` and virtual environments

Or, if you wish to install `findlike` in a new virtual environment, first create and activate the environment:

```bash
python -m venv <virtual environment directory>
source <virtual environment directory>/bin/activate
```

Then run `pip install findlike` (without the `--user` flag).

### Manual installation from source
Lastly, if you prefer to install `findlike` from this repository instead of fetching the package from PyPI: 

```bash
# Clone this repository
git clone https://github.com/brunoarine/findlike.git

# Navigate into the findlike directory
cd findlike

# Install the required dependencies
pip install -r requirements.txt
```

Then you have two options, either you can install it as a Python package using `pip`:

```bash
pip install -e .
```

Or you can an alias for the `findlike` command:

```bash
# Replace .bashrc with .zshrc depending on your shell environment.
echo "alias findlike='python /path/to/findlike/findlike/cli.py'" >> ~/.bashrc
source ~/.bashrc
```

## Usage

Here is the basic usage of findlike:

```bash
findlike [OPTIONS] [REFERENCE_FILE]
```

`findlike` works with either a reference file or a `--query` option. Once the reference text is set, `findlike` will scan a given directory (default is the current working dir), and return the most similar documents against the reference.

## Options

Here's the breakdown of the available options in Findlike:

```
  --version                     Show the version and exit.
  -q, --query TEXT              query option if no reference file is provided
  -d, --directory PATH          directory to scan for similar files  [default:
                                (current directory)]
  -f, --filename-pattern TEXT   filename pattern matching  [default: *.*]
  -R, --recursive               recursive search
  -a, --algorithm [bm25|tfidf]  text similarity algorithm  [default: tfidf]
  -l, --language TEXT           stemmer and stopwords language  [default:
                                english]
  -c, --min-chars INTEGER       minimum document size (in number of
                                characters) to be considered  [default: 1]
  -A, --absolute-paths          show absolute rather than relative paths
  -m, --max-results INTEGER     maximum number of results  [default: 10]
  -p, --prefix TEXT             result lines prefix
  -s, --show-scores             show similarity scores
  -h, --hide-reference          remove REFERENCE_FILE from results
  -H, --heading TEXT            results list heading
  -F, --format [plain|json]     output format  [default: plain]
  -t, --threshold FLOAT         minimum score for a result to be shown
                                [default: 0.0]
  --help                        Show this message and exit.
```

## Examples

To find similar documents in a directory (recursively):

```sh
findlike -R -d /path/to/directory reference_file.md 
```

To search files using a query instead of a reference file while filtering by extension:

```sh
findlike -q "black holes" -d /path/to/ayreon/lyrics -f "*.txt"
```

To show similarity scores and filenames in JSON format:

```sh
findlike -s -F json reference_file.md
```

To print the results table as a Markdown list:

```sh
findlike -H "# List of similar documents" -p "- " reference_file.txt
```

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.
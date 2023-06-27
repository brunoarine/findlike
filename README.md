# findlike

[![PyPI](https://img.shields.io/pypi/v/findlike.svg)](https://pypi.org/project/findlike/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/brunoarine/findlike/blob/master/LICENSE)

`findlike` is a command-line tool that enables users to find similar documents in relation to a reference file or an ad-hoc query. This project is written in Python and utilizes well-known libraries that are optimized for performance.

Features: 

- Choose between BM25 and TF-IDF + cosine distance for similarity calculation
- Recursive search option
- Control over output format, document size to consider, maximum results to show, etc.
- Multilingual support

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Example](#examples)
- [License](#license)

## Getting Started

These instructions will guide you through the process of installing and using `findlike` on your local machine.

### Prerequisites

- Python 3.7 or higher
- Additional dependencies as listed in the `requirements.txt` file

### Installation

To install `findlike`, follow the steps below:

```bash
pip install --user findlike
```

If you prefer to download the repository instead:

```bash
# Clone this repository
git clone https://github.com/brunoarine/findlike.git

# Navigate into the findlike directory
cd findlike

# Install the required dependencies
pip install -r requirements.txt

# Add an alias for the findlike command (Optional)
echo "alias findlike='python /path/to/findlike/main.py'" >> ~/.bashrc
source ~/.bashrc
```

## Usage

Here is the basic usage of findlike:

```bash
findlike [OPTIONS] [REFERENCE_FILE]
```

findlike will scan a given directory and return the most similar documents in relation to either a reference file or a query passed to with by the `--query` option.

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
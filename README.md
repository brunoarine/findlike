# findlike

[![PyPI](https://img.shields.io/pypi/v/findlike.svg)](https://pypi.org/project/findlike/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/brunoarine/findlike/blob/master/LICENSE)
[![Tests](https://github.com/brunoarine/findlike/workflows/Test/badge.svg)](https://github.com/brunoarine/findlike/actions?query=workflow%3ATest)

`findlike` is a command-line tool written in Python that retrieves a list of similar files in relation to a reference file or an ad-hoc query. The tool is highly configurable and can be used as backend for other programs (e.g. personal knowledge management systems, Emacs, etc.) 

Features: 

- Choose between BM25 and TF-IDF + cosine distance for similarity calculation
- Recursive search option
- Control over parameters like maximum number of results, whether to display similarity scores etc.
- Optionally return results in JSON format
- Multilingual support

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Example](#examples)
- [Development](#development)
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

# Install it as a Python package using `pip`:

pip install -e .
```

Optionally, you can create an alias for the `findlike` command to be accessible without activating its virtual environment:

```bash
# Replace .bashrc with .zshrc depending on your shell environment.
echo "alias findlike='/path/to/findlike/venv/bin/findlike'" >> ~/.bashrc
source ~/.bashrc
```

## Usage

Here is the basic usage of findlike:

```bash
findlike [OPTIONS] [REFERENCE_FILE]
```

`findlike` works with either a reference file or a `--query` option. Once the reference text is set, `findlike` will scan a given directory (default is the current working dir), and return the most similar documents against the reference.

## Options

Here's the breakdown of the available options in findlike:

#### `--help`

Displays a short summary of the available options.

#### `-d, --directory PATH`

Specify the directory that is going to be scanned. Default is current working directory. Example:

```sh
findlike -d /path/to/another/directory
```

#### `-q, --query TEXT`

Passes an ad-hoc query to the program, so that no reference file is required. Useful when you want to quickly find documents by an overall theme. Example:

```sh
findlike -q "earthquakes"
```

#### `-f, --file-pattern`

Specifies the file pattern to use when scanning the directories for similar files. The pattern uses [glob](https://en.wikipedia.org/wiki/Glob_(programming)) convention, and should be passed with single or double quotes, otherwise your shell environment will likely try to expand it. Default is common plain-text file extensions (the full list can be seen [here](./findlike/constants.py)).

```sh
findlike -f "*.md" reference_file.txt
```

#### `-R, --recursive`

If used, this option makes `findlike` scans directories and their sub-directories as well. Example:

```sh
findlike reference_file.txt -R
```

#### `-a, --algorithm [tfidf|bm25]`

Algorithm to use when generating the scores list. The possible choices are `tfidf` or `bm25'. Default is `tfidf`, and it works great in most cases. However, `bm25' may be a bit more robust in depending on the size of your documents. Example:

```sh
findlike reference_file -a bm25
```

#### `-l, --language TEXT`

Changing this value will impact stopwords filtering and word stemmer. The following languages are supported: Arabic, Danish, Dutch, English, Finnish, French, German, Hungarian, Italian, Norwegian, Portuguese, Romanian, Russian, Spanish and Swedish. Default is English.

```sh
findlike reference_file.txt -l "portuguese"
```

#### `-c, --min-chars INTEGER`

Minimum document size (in number of characters) to be included in the corpus. Default is 1. Example:

```sh
findlike reference_file.txt -c 50
```

#### `-A, --absolute-paths`

Show the absolute path of each result instead of relative paths. Example:

```sh
findlike reference_file.txt -A
```

#### `-m, --max-results INTEGER`

Number of items to show in the final results. Default is 10.

```sh
findlike reference_file.txt -m 5
```

#### `-p, --prefix TEXT`

String to prepend each entry in the final results. You can set it to "* " or "- " to turn them into a Markdown or Org-mode list. Default is "", so that no prefix is shown. Example: 

```sh
findlike reference_file.txt -p "- "
```

#### `-h, --hide-reference`

Remove the first result from the scores list. Useful if the reference file is in the scanned directory, and you don't want to see it included in the top of the results. This option has no effect if the `--query` option is used.

```sh
findlike reference_file.txt -h
```

#### `-H, --heading TEXT`

Text to show as the list heading. Default is "", so no heading title is shown. Example:

```sh
findlike reference_file.txt -H "## Similar files"
```

#### `-F, --format [plain|json]`

This option sets the output format. `plain` will print the results as a simple list, one entry per line. `json` will print the results as a valid JSON list with `score` and `target` as keys for each entry. Default is "plain". Example:

```sh
findlike reference_file.txt -F json
```

#### `-t, --threshold FLOAT`

Similarity score threshold. All results whose score are below the determined threshold will be omitted. Default is 0.05. Set it to 0 if you wish to show all results. Example:

```sh
findlike reference_file.txt -t 0
```

## More Examples

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

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd findlike
python -m venv venv
source venv/bin/activate
```

Now install the development dependencies:

```sh
pip install -e '.[dev]'
```

To run the tests:

```sh
pytest
```

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

## Acknowledgements

- [Simon Willison](https://simonwillison.net/) for being an inspiration on releasing small but useful tools more often.
- [Sindre Sorhus](https://raw.githubusercontent.com/sindresorhus/text-extensions) for the comprehensive list of plain-text file extensions.
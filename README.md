# findlike

[![PyPI](https://img.shields.io/pypi/v/findlike.svg)](https://pypi.org/project/findlike/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/brunoarine/findlike/blob/master/LICENSE)
[![Tests](https://github.com/brunoarine/findlike/workflows/Test/badge.svg)](https://github.com/brunoarine/findlike/actions?query=workflow%3ATest)

`findlike` is a command-line tool written in Python that retrieves a list of similar files in relation to a reference text or ad-hoc query.

Imagine you have a document, and you want to find other documents on your computer that talk about similar things. You can use `findlike` to do that. It looks at the words and phrases used in your reference document or a specific question you have, and then finds other files that use similar language. It's a bit like doing a Google search across your own files.

![](example.gif)

Features: 

- Choose between [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) and [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithms for the lexical similarity calculation between file contents
- Recursive search option
- Control over parameters like maximum number of results, whether to display similarity scores etc.
- Optionally return results in JSON format
- Multilingual support
- Highly configurable and can be used as backend for other programs (e.g. personal knowledge management systems, Emacs, etc.)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using pip (single user)](#using-pip-single-user)
  - [Using pip and virtual environments](#using-pip-and-virtual-environments)
  - [Manual installation from source](#manual-installation-from-source)
- [Usage](#usage)
- [Options](#options)
- [Examples](#examples)
- [Development](#development)
- [Projects using findlike](#projects-using-findlike)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Prerequisites

- Python 3.8 or higher
- Additional dependencies as listed in the `requirements.txt` file

## Installation

### Using pip (single user)

To install `findlike` for your user only, run the following command in your terminal:

```bash
pip install --user findlike
```

### Using pip and virtual environments

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

Here's the breakdown of the available options:


| <div style="width:220px">Option</div>                     | Detailed Description                                                                                                                                                                                                                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--help`                    | Displays a short summary of the available options.                                                                                                                                                                                                                                                                                    |
| `-d, --directory PATH`      | Specify the directory that is going to be scanned. Default is current working directory. Example: `findlike -d /path/to/another/directory`                                                                                                                                                                                            |
| `-q, --query TEXT`          | Passes an ad-hoc query to the program, so that no reference file is required. Useful when you want to quickly find documents by an overall theme. Example: `findlike -q "earthquakes"`                                                                                                                                                |
| `-f, --file-pattern`        | Specifies the file pattern to use when scanning the directories for similar files. The pattern uses glob convention, and should be passed with single or double quotes, otherwise your shell environment will likely try to expand it. Default is common plain-text file extensions. Example: `findlike -f "*.md" reference_file.txt` |
| `-R, --recursive`           | If used, this option makes `findlike` scan directories and their sub-directories as well. Example: `findlike reference_file.txt -R`                                                                                                                                                                                                   |
| `-a, --algorithm [tfidf, bm25]`| Algorithm to use when generating the scores list. The possible choices are `tfidf` or `bm25`. Default is `tfidf`. Example: `findlike reference_file -a bm25` |
| `-l, --language TEXT`       | Changing this value will impact stopwords filtering and word stemmer. Default is English. Example: `findlike reference_file.txt -l "portuguese"`                                                                                                                                                                                      |
| `-c, --min-chars INTEGER`   | Minimum document size (in number of characters) to be included in the corpus. Default is 1. Example: `findlike reference_file.txt -c 50`                                                                                                                                                                                              |
| `-A, --absolute-paths`      | Show the absolute path of each result instead of relative paths. Example: `findlike reference_file.txt -A`                                                                                                                                                                                                                            |
| `-m, --max-results INTEGER` | Number of items to show in the final results. Default is 10. Example: `findlike reference_file.txt -m 5`                                                                                                                                                                                                                              |
| `-p, --prefix TEXT`         | String to prepend each entry in the final results. Default is "". Example: `findlike reference_file.txt -p "- "`                                                                                                                                                                                                                      |
| `-h, --hide-reference`      | Remove the first result from the scores list. This option has no effect if the `--query` option is used. Example: `findlike reference_file.txt -h`                                                                                                                                                                                    |
| `-H, --heading TEXT`        | Text to show as the list heading. Default is "". Example: `findlike reference_file.txt -H "## Similar files"`                                                                                                                                                                                                                         |
| `-F, --format [plain, json]` | This option sets the output format. Default is "plain". Example: `findlike reference_file.txt -F json`                                                       |
| `-t, --threshold FLOAT`     | Similarity score threshold. All results whose score are below the determined threshold will be omitted. Default is 0.05. Example: `findlike reference_file.txt -t 0`                                                                                                                                                                  |
| `-i, --ignore-front-matter` | Tries to strip the front-matter from markup files like Markdown and Org-mode. |

## Examples

To find similar documents in a directory (recursively) against a reference text file:

```sh
findlike -R -d /path/to/directory reference_file.md 
```

To search files using a query instead of a reference file while filtering by extension:

```sh
findlike -q "black holes" -d /path/to/ayreon/lyrics -f "*.txt"
```

To find similar files and show their similarity scores and filenames in JSON format:

```sh
findlike -s -F json reference_file.md
```

To print the similarity results as a Markdown list:

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

## Projects using findlike

- [org-similarity](https://github.com/brunoarine/org-similarity) - Emacs package to search for similar org files in relation to the current buffer.

## Acknowledgements

- [Simon Willison](https://simonwillison.net/) for being an inspiration on releasing small but useful tools more often.
- [Sindre Sorhus](https://raw.githubusercontent.com/sindresorhus/text-extensions) for the comprehensive list of plain-text file extensions.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.


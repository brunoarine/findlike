from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

from .markup import Markup
from .utils import try_read_file

WORD_RE = re.compile(r"(?u)\b\w{2,}\b")
URL_RE = re.compile(r"\S*https?:\S*")

SCRIPT_PATH = Path(__file__).parent


class Processor:
    """Class containing preprocessing and tokenization rules.

    Args:
        junkchars (list): List of junk characters to be stripped from the text.
        stopwords (list): List of stopwords to be removed from the text.
        stemmer (nltk's stemmer): Stemmer provided by the nltk API.
    """

    def __init__(
        self,
        stopwords: list[str],
        stemmer: Callable,
    ):
        self.stopwords = stopwords
        self.stemmer = stemmer
        self._stopwords_re = re.compile(
            r"\b(" + r"|".join(stopwords) + r")\b\s*"
        )

    def preprocessor(self, text: str) -> str:
        """Remove fancy symbols and stopwords."""
        text = text.lower()
        text = text.translate({ord("’"): ord("'")})
        text = self._stopwords_re.sub("", text)
        text = URL_RE.sub("", text)
        return text

    def tokenizer(self, text: str) -> list[str]:
        """Run the tokenization and post-processing.
        This method should be called by the similarity algorithms.
        """
        tokens = self._tokenize(text)
        stemmized_tokens = self._stemmize(tokens)
        return stemmized_tokens

    def _tokenize(self, text: str) -> list[str]:
        """Preprocess a text and returns a list of tokens.
        This method should be called by the similarity algorithms.
        """
        words = WORD_RE.findall(text)
        return words

    def _stemmize(self, tokens: list[str]) -> list[str]:
        """Get only the stems from a list of words."""
        return [self.stemmer(w) for w in tokens]


class Corpus:
    """This wrapper provides easy access to a filtered corpus.

    Args:
        paths (list of Path): Document paths.
        min_chars (int): Minimum document size (in number of chars) to include
            in the corpus.
    Properties:
        documents_ (list of str): List of filtered document contents.
        paths_ (list of Path): List of filtered document paths.

    """

    def __init__(
        self,
        paths: list[Path],
        min_chars: int,
        ignore_front_matter: bool = False,
    ):
        self.paths = paths
        self.min_chars = min_chars
        self.ignore_front_matter = ignore_front_matter

        self.documents_: list[str] = []
        self.paths_: list[Path] = []
        self.reference_: str | None = None

        self.add_from_paths()

    def add_from_file(self, path: Path, is_reference: bool = False):
        """Adds the contents of a file to the corpus.

        Args:
            path (Path): The path to the file.
            is_reference (bool, optional): Indicates if the file is a reference file.
                Defaults to False.

        Notes:
            - The file content is added to the corpus if it meets the minimum character
              length requirement.
            - If front matter stripping is enabled, the file content is stripped of its
              front matter before being added to the corpus.
        """
        loaded_doc = try_read_file(path)
        if loaded_doc and len(loaded_doc) >= self.min_chars:
            if self.ignore_front_matter:
                loaded_doc = self.strip_front_matter(
                    loaded_doc, extension=path.suffix
                )
            if is_reference:
                self.reference_ = loaded_doc
                if self.reference_ not in self.documents_:
                    self.documents_.append(self.reference_)
            else:
                self.documents_.append(loaded_doc)
                self.paths_.append(path)

    def add_from_query(self, query: str):
        self.documents_.append(query)
        self.reference_ = query

    def add_from_paths(self) -> list[str | None]:
        """Load document contents from the specified paths."""
        return [self.add_from_file(p) for p in self.paths]

    def strip_front_matter(self, document: str, extension: str) -> str:
        """Strip front-matter from the loaded documents."""
        markup = Markup(extension=extension)
        return markup.strip_frontmatter(document)

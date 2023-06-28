from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

from .utils import try_read_file, compress

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
        tokens = self._stemmize(tokens)
        return tokens

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
    ):
        self.paths = paths
        self.min_chars = min_chars

        self._loaded_documents: list[str | None]

        self.documents_: list[str]
        self.paths_: list[Path]

        self._load_documents()
        if min_chars:
            self._apply_min_chars_filter()
        self._prune_documents()
        self._prune_paths()

    def _load_documents(self):
        self._loaded_documents = [try_read_file(p) for p in self.paths]

    def _prune_paths(self):
        self.paths_ = compress(self.paths, self.documents_)

    def _prune_documents(self):
        self.documents_ = [x for x in self._loaded_documents if x]

    def _apply_min_chars_filter(self):
        """Apply min chars filter in both documents and documents paths"""
        self._loaded_documents = [
            doc if doc and len(doc) >= self.min_chars else None
            for doc in self._loaded_documents
        ]
        return self

import re
from itertools import compress
from pathlib import Path
from typing import Callable, List
from nltk.stem import WordNetLemmatizer

WORD_RE = re.compile(r"(?u)\b[a-z]{2,}\b")
URL_RE = re.compile(r"\S*https?:\S*")

SCRIPT_PATH = Path(__file__).parent


class Processor:
    """Class containing preprocessing and tokenization rules.

    Args:
        junkchars (list): List of junk characters to be stripped from the text.
        stopwords (list): List of stopwords to be removed from the text.
        stemmer (nltk's stemmer): Stemmer provided by the nltk API.
        lemmatize (bool): Whether to lemmatize tokens.
    """

    def __init__(
        self,
        stopwords: list[str],
        stemmer: Callable,
        lemmatize=False,
    ):
        self.stopwords = stopwords
        self.stemmer = stemmer
        self.lemmatize = lemmatize
        self._lemmatizer = WordNetLemmatizer() if self.lemmatize else None
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

    def _tokenize(self, text: str) -> List[str]:
        """Preprocess a text and returns a list of tokens."""
        words = WORD_RE.findall(text)
        return words

    def _lemmatize(self, tokens: List[str]) -> List[str]:
        return [self._lemmatizer.lemmatize(w) for w in tokens]

    def _stemmize(self, tokens: List[str]) -> List[str]:
        """Get only the stems from a list of words."""
        return [self.stemmer(w) for w in tokens]

    def tokenizer(self, text: str) -> List[str]:
        """Run the preprocessor."""

        tokens = self._tokenize(text)
        tokens = self._lemmatize(tokens) if self.lemmatize else tokens
        tokens = self._stemmize(tokens)
        return tokens


class Corpus:
    """This wrapper provides easy access to a filtered corpus.

    Args:
        paths (list of Path): Documents paths.
        min_words (int): Minimum document size (in number of words) to include
            in the corpus. This number takes into account the number of words
            in the document bodies only, and doesn't include any kind of file
            properties (not even #+TITLE).

    Properties:
        documents_ (list of str): List of (un)filtered documents contents.
        paths_ (list of Path): List of (un)filtered document paths.

    """

    def __init__(
        self,
        paths: List[Path],
        min_chars: int,
    ):
        self.min_chars = min_chars

        valid_documents: list[str|None] = [read_file(p) for p in paths]
        self.documents_: list[str] = [x for x in valid_documents if x]
        self.paths_: list[Path] = list(compress(paths, valid_documents))

        if min_chars:
            self._apply_filter()

    def _apply_filter(self):
        """Apply min chars filter in both documents and documents paths"""
        mask = [len(doc) >= self.min_chars for doc in self.documents_]
        self.documents_ = list(compress(self.documents_, mask))
        self.paths_ = list(compress(self.paths_, mask))
        return self


def read_file(filename: Path) -> str|None:
    with filename.open() as f:
        try:
            document = f.read()
        except UnicodeDecodeError:
            document = None
    return document

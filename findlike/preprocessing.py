from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

from .markup import Markup
from .utils import compress, try_read_file

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
        
        self.documents_ = self._notnull_documents

    def add_document(self, document: str, extension: str | None = None):
        """Add a document to the current corpus.

        Args:
            document (str): Document to be added.
            filetype (str|None): Type or file extension from where the document came.
                This is necessary in case we try to filter out the document's
                front-matter.

        Returns:
            list[str]: The new corpus after the document has been added.
        """
        if extension and self.ignore_front_matter:
            markup = Markup(extension=extension)
            self.documents_.append(markup.strip_frontmatter(document))
        else:
            self.documents_.append(document)

    @property
    def _loaded_documents(self) -> list[str | None]:
        return [try_read_file(p) for p in self.paths]

    @property
    def _frontmatter_stripped_documents(self) -> list[str | None]:
        """Reads _loaded_documents and returns frontmatter-stripped documents"""
        if self.ignore_front_matter:
            stripped_documents: list[str | None] = []
            for document, path in zip(self._loaded_documents, self.paths):
                if document:
                    markup = Markup(extension=path.suffix)
                    stripped_documents.append(
                        markup.strip_frontmatter(document)
                    )
                else:
                    stripped_documents.append(None)
            return stripped_documents
        else:
            return self._loaded_documents

    @property
    def _min_filtered_documents(self) -> list[str | None]:
        """Apply min chars filter in both documents and documents paths.

        All documents that don't meet the criteria will be turned into None."""
        if self.min_chars:
            return [
                doc if doc and len(doc) >= self.min_chars else None
                for doc in self._frontmatter_stripped_documents
            ]
        else:
            return self._frontmatter_stripped_documents

    @property
    def paths_(self) -> list[Path]:
        """List of paths whose documents are valid

        (i.e. non-null and above max char if set)"""
        return compress(self.paths, self._min_filtered_documents)

    @property
    def _notnull_documents(self) -> list[str]:
        """List of non-null documents"""
        return [x for x in self._min_filtered_documents if x]

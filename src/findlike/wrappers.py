from __future__ import annotations

import concurrent.futures
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import Processor
from functools import partial

def _process_doc(doc: str, processor: Processor) -> list[str]:
    """Apply preprocessing and tokenization to a document.

    This helper function is used in parallel processing to clean and tokenize
    a document using the provided Processor instance.

    Args:
        doc: The document text to process.
        processor: The Processor instance containing preprocessing rules.

    Returns:
        The tokenized document as a list of strings.
    """
    cleaned = processor.preprocessor(doc)
    return processor.tokenizer(cleaned)

class Tfidf:
    """Scikit-learn's TF-IDF wrapper.

    Args:
        processor (Processor): Processor object.

    Attributes:
        source_embeddings_: Reference content embeddings.
        target_embeddings_: Scanned files embeddings.
    """

    def __init__(self, processor, **kwargs):
        self.processor = processor

        self._vectorizer = TfidfVectorizer(
            tokenizer=self.processor.tokenizer,
            preprocessor=self.processor.preprocessor,
            token_pattern=None,
            **kwargs,
        )

    def fit(self, documents: list[str]):
        self.target_embeddings_ = self._vectorizer.fit_transform(documents)

    def get_scores(self, source: str):
        self.reference_embeddings_ = self._vectorizer.transform([source])
        scores = cosine_similarity(
            self.reference_embeddings_, self.target_embeddings_
        ).flatten()
        return scores


class BM25:
    """Okapi BM25 wrapper.

    Args:
        processor (Processor): Processor object.

    Attributes:
        tokenized_documents_ (list[str]): List of tokens.
    """

    def __init__(self, processor):
        self.processor = processor

    def fit(self, documents: list[str]):
        """Fit IDF to documents X"""
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            self.tokenized_documents_ = list(executor.map(_process_doc, documents))

        self._model = BM25Okapi(self.tokenized_documents_)

    def get_scores(self, source: str):
        clean_source = self.processor.preprocessor(source)
        tokenized_source = self.processor.tokenizer(clean_source)
        scores = self._model.get_scores(tokenized_source)
        return scores

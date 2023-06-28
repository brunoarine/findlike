from __future__ import annotations

from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Tfidf:
    """Scikit-learn's TF-IDF wrapper.

    Args:
        processor (Processor): Processor object.
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
        self._vectorizer.fit(documents)
        self.documents_embeddings_ = self._vectorizer.transform(documents)

    def get_scores(self, source: str):
        self.source_embeddings_ = self._vectorizer.transform([source])
        scores = cosine_similarity(
            self.source_embeddings_, self.documents_embeddings_
        ).flatten()
        return scores


class BM25:
    """Okapi BM25 wrapper.

    Args:
        processor (Processor): Processor object.
    """

    def __init__(self, processor):
        self.processor = processor

    def fit(self, documents: list[str]):
        """Fit IDF to documents X"""
        clean_docs = [self.processor.preprocessor(d) for d in documents]
        tokenized_docs = [self.processor.tokenizer(d) for d in clean_docs]
        self._model = BM25Okapi(tokenized_docs)

    def get_scores(self, source: str):
        clean_source = self.processor.preprocessor(source)
        tokenized_source = self.processor.tokenizer(clean_source)
        scores = self._model.get_scores(tokenized_source)
        return scores

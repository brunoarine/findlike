from __future__ import annotations

from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wrappers import BertModel

N_THREADS = 6
LIBBERT_PATH = "/home/soldeace/apps/src/bert.cpp/build/libbert.so"
MODEL_PATH = "/home/soldeace/apps/src/bert.cpp/models/all-MiniLM-L6-v2/ggml-model-q4_0.bin"

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
        # Since the reference has been appended to the corpus, the last
        # item in the embeddings list will be the reference's.
        self.reference_embeddings_ = self.target_embeddings_[-1]
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
        clean_docs = [self.processor.preprocessor(d) for d in documents]
        self.tokenized_documents_ = [
            self.processor.tokenizer(d) for d in clean_docs
        ]
        self._model = BM25Okapi(self.tokenized_documents_)

    def get_scores(self, source: str):
        # Since the reference has been appended to the corpus, the last
        # item in the embeddings list will be the reference's.
        tokenized_source = self.tokenized_documents_[-1]
        scores = self._model.get_scores(tokenized_source)
        return scores

class SBERT:
    def __init__(self, processor):
        self.processor = processor()
        self.model = BertModel(fname=MODEL_PATH)
    def fit(self, documents: list[str]):
        self.embeddings = [self.get_embeddings(doc) for doc in documents]
        pass
    def get_scores(self, source: str):
        pass
    def get_embeddings(self, document: str) -> list[float]:
        sentences = self.processor.tokenizer(document)
        embeddings = [self.model.encode(sentence) for sentence in sentences]
        
        pass
import pytest
from pathlib import Path
from findlike.preprocessing import Corpus
from findlike.utils import try_read_file


@pytest.fixture
def sample_paths(tmp_path):
    content1 = "This is a sample document with enough characters."
    content2 = "Too short."
    content3 = "This one has just enough characters to pass the filter."

    path1 = tmp_path / "doc1.txt"
    path2 = tmp_path / "doc2.txt"
    path3 = tmp_path / "doc3.txt"

    with open(path1, "w") as f:
        f.write(content1)

    with open(path2, "w") as f:
        f.write(content2)

    with open(path3, "w") as f:
        f.write(content3)

    return [path1, path2, path3]


def test_loading_documents(sample_paths):
    corpus = Corpus(sample_paths, min_chars=0)
    assert len(corpus._loaded_documents) == 3


def test_min_chars_filter(sample_paths):
    corpus = Corpus(sample_paths, min_chars=30)
    filtered_docs = corpus.documents_
    filtered_paths = corpus.paths_

    assert len(filtered_docs) == 2
    assert len(filtered_paths) == 2


def test_pruning_documents(sample_paths):
    corpus = Corpus(sample_paths, min_chars=30)
    assert all(doc is not None for doc in corpus.documents_)


def test_pruning_paths(sample_paths):
    corpus = Corpus(sample_paths, min_chars=30)
    filtered_paths = corpus.paths_

    assert isinstance(filtered_paths[0], Path)
    assert any("doc2.txt" not in str(path) for path in filtered_paths)


def test_try_read_file(sample_paths):
    valid_path = sample_paths[0]
    invalid_path = Path("nonexistent.txt")

    # Test reading a valid file
    document = try_read_file(valid_path)
    assert document is not None

    # Test reading an invalid file
    with pytest.raises(FileNotFoundError):
        try_read_file(invalid_path)


def test_empty_paths_list():
    corpus = Corpus([], min_chars=0)
    assert len(corpus.documents_) == 0
    assert len(corpus.paths_) == 0


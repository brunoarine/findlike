import tempfile
from pathlib import Path
from textwrap import dedent

import pytest

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


class TestCorpus:
    # Fixture for creating temporary files with random content
    @pytest.fixture
    def temp_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            file1 = tmp_path / "file1.txt"
            file2 = tmp_path / "file2.txt"
            file1.write_text("This is file 1.")
            file2.write_text("This is file 2.")
            yield [file1, file2]

    # Fixture for creating a Corpus instance
    @pytest.fixture
    def corpus(self):
        min_chars = 10
        return Corpus([], min_chars)

    # Test add_from_file method
    def test_files_were_added(self, corpus, temp_files):
        # Add files to the corpus
        corpus.add_from_file(temp_files[0])
        corpus.add_from_file(temp_files[1])

        # Check if documents and paths are updated correctly
        assert len(corpus.documents_) == 2
        assert len(corpus.paths_) == 2
        assert corpus.documents_[0] == "This is file 1."
        assert corpus.documents_[1] == "This is file 2."
        assert corpus.paths_[0] == temp_files[0]
        assert corpus.paths_[1] == temp_files[1]

    # Test add_from_query method
    def test_add_from_query(self, corpus):
        # Add query to the corpus
        corpus.add_from_query("This is a query.")

        # Check if the query is added to the documents
        assert len(corpus.documents_) == 1
        assert len(corpus.paths_) == 0
        assert corpus.documents_[0] == "This is a query."

    # Test _strip_front_matter method
    def test_strip_front_matter(self, corpus):
        # Test with front matter stripping disabled
        document = "This is a document."
        stripped_document = corpus.strip_front_matter(document, extension=".txt")
        assert stripped_document == document
        
        # Test with front matter stripping enabled
        document = """
        :PROPERTIES:
        :ID: 123
        :END:
        #+TITLE: Example
        This is some text.
        ** A heading
        Some more text.
        """
        extension = ".org"
        expected = "This is some text.\n** A heading\nSome more text."
        assert corpus.strip_front_matter(dedent(document), extension) == expected
    
    def test_reference_duplicity(self, corpus, temp_files):
        corpus.add_from_file(temp_files[0])
        corpus.add_from_file(temp_files[1])
        corpus.add_from_file(temp_files[0], is_reference=True)
        duplicates = set([x for x in corpus.documents_ if corpus.documents_.count(x) > 1])
        assert len(duplicates) == 0

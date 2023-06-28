import pytest
from nltk.stem import SnowballStemmer
from findlike.preprocessing import Processor
from stop_words import get_stop_words


@pytest.fixture
def processor():
    stemmer = SnowballStemmer("english").stem
    return Processor(
        stopwords=get_stop_words("english"), stemmer=stemmer
    )


def test_preprocessor(processor):
    text = "There’s a URL https://example.com in this text."
    processed_text = processor.preprocessor(text)
    assert processed_text == "'s url  text."


def test_tokenize(processor):
    text = "This is a test."
    tokens = processor._tokenize(text)
    assert tokens == ["This", "is", "test"]


def test_stemmize(processor):
    tokens = ["running", "cats", "quickly"]
    stemmed_tokens = processor._stemmize(tokens)
    assert stemmed_tokens == ["run", "cat", "quick"]


def test_tokenizer(processor):
    text = "There’s a word in this text. Running cats quickly!"
    tokens = processor.tokenizer(text)
    assert tokens == [
        "there",
        "word",
        "in",
        "this",
        "text",
        "run",
        "cat",
        "quick",
    ]


def test_empty_text(processor):
    text = ""
    tokens = processor.tokenizer(text)
    assert tokens == []


def test_text_with_only_stopwords(processor):
    text = "This is a the an"
    tokens = processor.preprocessor(text)
    assert tokens == ""


def test_text_with_special_characters(processor):
    text = "#This is a test! @user #hashtag"
    tokens = processor.tokenizer(processor.preprocessor(text))
    assert tokens == ["test", "user", "hashtag"]


def test_text_with_numbers(processor):
    text = "There are 100 cats"
    tokens = processor.tokenizer(processor.preprocessor(text))
    assert tokens == ["100", "cat"]


def test_text_with_unicode_characters(processor):
    text = "café naïve"
    processed_text = processor.preprocessor(text)
    tokens = processor.tokenizer(processed_text)
    assert tokens == ["café", "naïv"]

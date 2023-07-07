from findlike.preprocessing import SentenceProcessor

processor = SentenceProcessor()

def test_tokenizer():
    text = "This is a sentence. This is another sentence."
    expected_sentences = ["This is a sentence.", "This is another sentence."]
    assert processor.tokenizer(text) == expected_sentences

def test_preprocessor():
    text = "This is some text."
    expected_text = "This is some text."
    assert processor.preprocessor(text) == expected_text

import ctypes
from typing import Union, List
import numpy as np
import os
import sys

N_THREADS = 6
LIBBERT_PATH = "/home/soldeace/apps/src/bert.cpp/build/libbert.so"
MODEL_PATH = "/home/soldeace/apps/src/bert.cpp/models/all-MiniLM-L6-v2/ggml-model-q4_0.bin"

class BertModel:
    def __init__(self, fname):
        self.lib = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), LIBBERT_PATH))

        self.lib.bert_load_from_file.restype = ctypes.c_void_p
        self.lib.bert_load_from_file.argtypes = [ctypes.c_char_p]

        self.lib.bert_n_embd.restype = ctypes.c_int32
        self.lib.bert_n_embd.argtypes = [ctypes.c_void_p]
        
        self.lib.bert_free.argtypes = [ctypes.c_void_p]

        self.lib.bert_encode_batch.argtypes = [
            ctypes.c_void_p,    # struct bert_ctx * ctx,
            ctypes.c_int32,     # int32_t n_threads,  
            ctypes.c_int32,     # int32_t n_batch_size
            ctypes.c_int32,     # int32_t n_inputs
            ctypes.POINTER(ctypes.c_char_p),                # const char ** texts
            ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), # float ** embeddings
        ]

        self.ctx = self.lib.bert_load_from_file(fname.encode("utf-8"))
        self.n_embd = self.lib.bert_n_embd(self.ctx)

    def __del__(self):
        self.lib.bert_free(self.ctx)

    def encode(self, sentences: Union[str, List[str]], batch_size: int = 16) -> np.ndarray:
        input_is_string = False
        if isinstance(sentences, str):
            sentences = [sentences]
            input_is_string = True

        n = len(sentences)

        embeddings = np.zeros((n, self.n_embd), dtype=np.float32)
        embeddings_pointers = (ctypes.POINTER(ctypes.c_float) * len(embeddings))(*[e.ctypes.data_as(ctypes.POINTER(ctypes.c_float)) for e in embeddings])

        texts = (ctypes.c_char_p * n)()
        for j, sentence in enumerate(sentences):
            texts[j] = sentence.encode("utf-8")

        self.lib.bert_encode_batch(
            self.ctx, N_THREADS, batch_size, len(sentences), texts, embeddings_pointers
        )
        if input_is_string:
            return embeddings[0]
        return embeddings

def main():    
    model = BertModel(MODEL_PATH)
    texts = [
    'Writing down what matters is an art, as it takes us a lot of effort to summarize and process all that information',
    'He notes that in matter of fitness, most art students make a lot of effort to keep in shape',
    'I do not see the point in harvesting so much information, something which many call the Collector\'s Fallacy'
    ]

    embedded_texts = model.encode(texts)
    
    def print_results(res):
        (closest_texts, closest_similarities) = res
        # Print the closest texts and their similarity scores
        print("Closest texts:")
        for i, text in enumerate(closest_texts):
            print(f"{i+1}. {text} (similarity score: {closest_similarities[i]:.4f})")

    # Define the function to query the k closest texts
    def query(text, k=3):
        # Embed the input text
        embedded_text = model.encode(text)
        # Compute the cosine similarity between the input text and all the embedded texts
        similarities = [np.dot(embedded_text, embedded_text_i) / (np.linalg.norm(embedded_text) * np.linalg.norm(embedded_text_i)) for embedded_text_i in embedded_texts]
        # Sort the similarities in descending order
        sorted_indices = np.argsort(similarities)[::-1]
        # Return the k closest texts and their similarities
        closest_texts = [texts[i] for i in sorted_indices[:k]]
        closest_similarities = [similarities[i] for i in sorted_indices[:k]]
        return closest_texts, closest_similarities

    test_query = "The Zettelkasten method is one of the favorite personal knowledge management systems for avid note takers nowadays"
    print_results(query(test_query))

if __name__ == '__main__':
    main()
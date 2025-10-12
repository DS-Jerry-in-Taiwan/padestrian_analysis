import unittest
import numpy as np
from preprocess.transformer_text_prerpocessor import TransformerTextPreprocessor

class TestTransformerTextPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = TransformerTextPreprocessor(max_length=10)

    def test_single_sentence(self):
        text = "hello world"
        result = self.preprocessor(text, return_tensors=None, max_length=10)
        self.assertIn("input_ids", result)
        self.assertIn("attention_mask", result)
        self.assertEqual(len(result["input_ids"][0]), 10)
        self.assertEqual(len(result["attention_mask"][0]), 10)

    def test_batch_sentences(self):
        texts = ["hello world", "openai is great"]
        result = self.preprocessor(texts, return_tensors=None, max_length=10)
        self.assertEqual(len(result["input_ids"]), 2)
        self.assertEqual(len(result["attention_mask"]), 2)
        for ids, mask in zip(result["input_ids"], result["attention_mask"]):
            self.assertEqual(len(ids), 10)
            self.assertEqual(len(mask), 10)

    def test_truncation(self):
        text = " ".join(["test"] * 20)
        result = self.preprocessor(text, truncation=True, max_length=5, return_tensors=None)
        self.assertEqual(len(result["input_ids"][0]), 5)
        self.assertEqual(len(result["attention_mask"][0]), 5)

    def test_return_tensors_np(self):
        text = "tensor test"
        result = self.preprocessor(text, return_tensors="np", max_length=10)
        self.assertIsInstance(result["input_ids"], np.ndarray)
        self.assertIsInstance(result["attention_mask"], np.ndarray)

if __name__ == "__main__":
    unittest.main()
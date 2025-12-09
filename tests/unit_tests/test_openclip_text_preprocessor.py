import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import unittest
from preprocess.openclip_text_tokenizer import OpenCLIPTEXTTokenizer

class TestOpenCLIPTextTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = OpenCLIPTEXTTokenizer(max_length=10)

    def test_single_sentence(self):
        text = "hello world"
        result = self.tokenizer(text)
        self.assertIn("input_ids", result)
        self.assertIn("attention_mask", result)
        self.assertEqual(len(result["input_ids"][0]), 10)
        self.assertEqual(len(result["attention_mask"][0]), 10)

    def test_batch_sentences(self):
        texts = ["hello world", "openai is great"]
        result = self.tokenizer(texts)
        self.assertEqual(len(result["input_ids"]), 2)
        self.assertEqual(len(result["attention_mask"]), 2)
        for ids, mask in zip(result["input_ids"], result["attention_mask"]):
            self.assertEqual(len(ids), 10)
            self.assertEqual(len(mask), 10)

    def test_truncation(self):
        text = " ".join(["test"] * 20)  # 長度超過 max_length
        result = self.tokenizer(text, truncation=True, max_length=5)
        self.assertEqual(len(result["input_ids"][0]), 5)
        self.assertEqual(len(result["attention_mask"][0]), 5)

    def test_no_padding(self):
        text = "short"
        result = self.tokenizer(text, padding=False, max_length=10)
        self.assertLessEqual(len(result["input_ids"][0]), 10)

    def test_return_tensors(self):
        text = "tensor test"
        result = self.tokenizer(text, return_tensors="np")
        import numpy as np
        self.assertIsInstance(result["input_ids"], np.ndarray)
        self.assertIsInstance(result["attention_mask"], np.ndarray)

if __name__ == "__main__":
    unittest.main()
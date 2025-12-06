import unittest
import numpy as np
from PIL import Image
from preprocess.vit_image_preprocessor import ViTImagePreprocessor
from preprocess.clip_image_preprocessor import CLIPImagePreprocessor
from preprocess.clip_text_preprocessor import CLIPTextTokenizer
from preprocess.bert_text_prerpocessor import TransformerTextPreprocessor
from preprocess.openclip_text_tokenizer import OpenCLIPTEXTTokenizer

class TestImagePreprocessors(unittest.TestCase):
    def setUp(self):
        self.vit = ViTImagePreprocessor()
        self.clip = CLIPImagePreprocessor()

    def test_vit_single_image(self):
        img = Image.new("RGB", (256, 256), color=(128, 128, 128))
        arr = self.vit(img)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (3, 224, 224))

    def test_clip_single_image(self):
        img = np.ones((256, 256, 3), dtype=np.uint8) * 128
        arr = self.clip(img)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (3, 224, 224))

    def test_vit_invalid_input(self):
        with self.assertRaises(ValueError):
            self.vit("not an image")

    def test_clip_gray_image(self):
        img = Image.new("L", (256, 256), color=128)
        arr = self.clip(img)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (3, 224, 224))

    def test_vit_batch(self):
        imgs = [Image.new("RGB", (256, 256)), Image.new("RGB", (256, 256))]
        arr = self.vit.batch_preprocess(imgs)
        self.assertEqual(arr.shape, (2, 3, 224, 224))

class TestTextTokenizers(unittest.TestCase):
    def setUp(self):
        self.clip = CLIPTextTokenizer()
        self.bert = TransformerTextPreprocessor()
        self.openclip = OpenCLIPTEXTTokenizer()

    def test_clip_tokenizer_single(self):
        out = self.clip("hello world", return_tensors="np")
        self.assertIn("input_ids", out)
        self.assertIn("attention_mask", out)
        self.assertEqual(out["input_ids"].shape[1], 77)

    def test_bert_tokenizer_batch(self):
        out = self.bert(["hello", "world"], return_tensors="np", max_length=10)
        self.assertIn("input_ids", out)
        self.assertEqual(out["input_ids"].shape[0], 2)

    def test_openclip_tokenizer_invalid(self):
        with self.assertRaises(ValueError):
            self.openclip(12345)

    def test_clip_tokenizer_invalid_list(self):
        with self.assertRaises(ValueError):
            self.clip([123, "valid"])

    def test_bert_tokenizer_invalid(self):
        with self.assertRaises(ValueError):
            self.bert({"not": "a string"})

if __name__ == "__main__":
    unittest.main()
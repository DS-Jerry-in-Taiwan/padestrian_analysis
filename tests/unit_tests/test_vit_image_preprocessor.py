import unittest
import numpy as np
from PIL import Image
from preprocess.vit_image_preprocessor import ViTImagePreprocessor

class TestViTImagePreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = ViTImagePreprocessor(
            size=(224, 224),
            mean=(0.5, 0.5, 0.5),
            std=(0.5, 0.5, 0.5)
        )

    def test_single_image_pil(self):
        img = Image.new("RGB", (256, 256), color=(128, 128, 128))
        result = self.preprocessor(img)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (3, 224, 224))

    def test_single_image_numpy(self):
        img = np.ones((256, 256, 3), dtype=np.uint8) * 128
        result = self.preprocessor(img)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (3, 224, 224))

    def test_batch_preprocess(self):
        imgs = [
            Image.new("RGB", (256, 256), color=(128, 128, 128)),
            np.ones((256, 256, 3), dtype=np.uint8) * 128
        ]
        batch = self.preprocessor.batch_preprocess(imgs)
        self.assertIsInstance(batch, np.ndarray)
        self.assertEqual(batch.shape, (2, 3, 224, 224))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.preprocessor("not an image")

    def test_gray_image(self):
        img = Image.new("L", (256, 256), color=128)
        result = self.preprocessor(img)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (3, 224, 224))

if __name__ == "__main__":
    unittest.main()
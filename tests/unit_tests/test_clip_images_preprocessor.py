import unittest
import numpy as np
from PIL import Image
from preprocess.clip_image_preprocessor import CLIPImagePreprocessor

class TestCLIPImagePreprocessor(unittest.TestCase):
    def setUp(self):
        # 初始化 CLIPImagePreprocessor
        self.preprocessor = CLIPImagePreprocessor()

    def test_single_image_pil(self):
        # 測試單張 PIL.Image 輸入
        img = Image.new("RGB", (256, 256), color="red")
        result = self.preprocessor(img)
        self.assertEqual(result.shape, (3, 224, 224))
        self.assertFalse(np.isnan(result).any())
        self.assertFalse(np.isinf(result).any())

    def test_single_image_numpy(self):
        # 測試單張 numpy.ndarray 輸入
        img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        result = self.preprocessor(img)
        self.assertEqual(result.shape, (3, 224, 224))
        self.assertFalse(np.isnan(result).any())
        self.assertFalse(np.isinf(result).any())

    def test_batch_images(self):
        # 測試批次影像處理
        img1 = Image.new("RGB", (256, 256), color="red")
        img2 = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        batch = [img1, img2]
        results = self.preprocessor.batch_preprocess(batch)
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result.shape, (3, 224, 224))
            self.assertFalse(np.isnan(result).any())
            self.assertFalse(np.isinf(result).any())

    def test_invalid_input_type(self):
        # 測試無效輸入類型
        with self.assertRaises(ValueError):
            self.preprocessor("not an image")

    def test_invalid_numpy_shape(self):
        # 測試無效的 numpy.ndarray 輸入
        invalid_img = np.random.randint(0, 255, (256, 256), dtype=np.uint8)  # 缺少通道維度
        with self.assertRaises(ValueError):
            self.preprocessor(invalid_img)

    def test_invalid_numpy_channels(self):
        # 測試通道數不為 3 的 numpy.ndarray
        invalid_img = np.random.randint(0, 255, (256, 256, 4), dtype=np.uint8)  # 通道數為 4
        with self.assertRaises(ValueError):
            self.preprocessor(invalid_img)

if __name__ == "__main__":
    unittest.main()
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import unittest
import numpy as np
from PIL import Image
from preprocess.PreprocessManager import PreprocessManager
from preprocess.registry import register_preprocessor, PREPROCESSOR_REGISTRY


class DummyImagePreprocessor:
    def __call__(self, data, **kwargs):
        return f"image:{data}"


class DummyTextPreprocessor:
    def __call__(self, data, **kwargs):
        return f"text:{data}"


class DummyAudioPreprocessor:
    def __call__(self, data, **kwargs):
        return f"audio:{data}"


class TestPreprocessManager(unittest.TestCase):

    def setUp(self):
        PREPROCESSOR_REGISTRY.clear()
        register_preprocessor('image', DummyImagePreprocessor())
        register_preprocessor('text', DummyTextPreprocessor())
        register_preprocessor('audio', DummyAudioPreprocessor())
        self.manager = PreprocessManager()

    def test_is_image(self):
        # 測試影像型態判斷
        np_image = np.zeros((224, 224, 3))  # numpy array
        pil_image = Image.new('RGB', (224, 224))  # PIL Image

        self.assertTrue(self.manager.is_image(np_image))
        self.assertTrue(self.manager.is_image(pil_image))
        self.assertFalse(self.manager.is_image("not an image"))

    def test_is_text(self):
        # 測試文字型態判斷
        text = "This is a test string"
        text_list = ["This is a test string", "Another string"]

        self.assertTrue(self.manager.is_text(text))
        self.assertTrue(self.manager.is_text(text_list))
        self.assertFalse(self.manager.is_text(123))  # 非文字型態

    def test_preprocess_image(self):
        # 測試影像分流邏輯
        np_image = np.zeros((224, 224, 3))  # numpy array
        result = self.manager.preprocess(np_image, mode='image')

        # 確認結果
        self.assertTrue(result.startswith("image:"))

    def test_preprocess_text(self):
        # 測試文字分流邏輯
        text = "This is a test string"
        result = self.manager.preprocess(text, mode='text')

        # 確認結果
        self.assertEqual(result, "text:This is a test string")

    def test_preprocess_auto_image(self):
        # 測試自動分流邏輯（影像）
        np_image = np.zeros((224, 224, 3))  # numpy array
        result = self.manager.preprocess(np_image, mode='auto')

        # 確認結果
        self.assertTrue(result.startswith("image:"))

    def test_preprocess_auto_text(self):
        # 測試自動分流邏輯（文字）
        text = "This is a test string"
        result = self.manager.preprocess(text, mode='auto')

        # 確認結果
        self.assertEqual(result, "text:This is a test string")

    def test_preprocess_audio(self):
        # 測試音訊分流邏輯
        data = b"audio_bytes"
        result = self.manager.preprocess(data, mode='audio')

        # 確認結果
        self.assertEqual(result, "audio:" + str(data))

    def test_preprocess_invalid_mode(self):
        # 測試無效的 mode
        with self.assertRaises(ValueError):
            self.manager.preprocess("Invalid data", mode='invalid')

    def test_preprocess_not_registered(self):
        # 測試未註冊的前處理器類型
        with self.assertRaises(ValueError):
            self.manager.preprocess("data", mode='video')

    def test_preprocess_kwargs(self):
        # 測試帶有額外參數的前處理
        class KwPreprocessor:
            def __call__(self, data, **kwargs):
                return kwargs.get('flag', False)

        register_preprocessor('kw', KwPreprocessor())
        result = self.manager.preprocess("data", mode='kw', flag=True)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
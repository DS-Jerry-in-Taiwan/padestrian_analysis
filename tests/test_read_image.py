import os
import numpy as np
import torch
import pytest
import sys
from PIL import Image
import tempfile
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from preprocess.read_image import read_image, read_images, Preprocessor

class TestReadImage:
    @pytest.fixture(scope="class")
    def setup_test_images(self):
        test_dir = tempfile.mkdtemp()
        valid_img_path = os.path.join(test_dir, "valid.jpg")
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        pil_img = Image.fromarray(test_image)
        pil_img.save(valid_img_path)
        invalid_img_path = os.path.join(test_dir, "invalid.txt")
        with open(invalid_img_path, 'w') as f:
            f.write("This is not an image file")
        nonexistent_path = os.path.join(test_dir, "nonexistent.jpg")
        yield {
            "test_dir": test_dir,
            "valid_img_path": valid_img_path,
            "invalid_img_path": invalid_img_path,
            "nonexistent_path": nonexistent_path
        }
        shutil.rmtree(test_dir)

    def test_read_image_success(self, setup_test_images):
        img = read_image(setup_test_images["valid_img_path"])
        assert isinstance(img, np.ndarray)
        assert len(img.shape) == 3
        assert img.shape[2] == 3

    def test_read_image_file_not_found(self, setup_test_images):
        with pytest.raises(FileNotFoundError):
            read_image(setup_test_images["nonexistent_path"])

    def test_read_image_invalid_file(self, setup_test_images):
        with pytest.raises(IOError):
            read_image(setup_test_images["invalid_img_path"])

class TestReadImages:
    @pytest.fixture(scope="class")
    def setup_test_directory(self):
        test_dir = tempfile.mkdtemp()
        for i in range(3):
            img_path = os.path.join(test_dir, f"test_{i}.jpg")
            test_image = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
            pil_img = Image.fromarray(test_image)
            pil_img.save(img_path)
        invalid_path = os.path.join(test_dir, "invalid.txt")
        with open(invalid_path, 'w') as f:
            f.write("Not an image")
        empty_dir = os.path.join(test_dir, "empty")
        os.makedirs(empty_dir)
        yield {
            "test_dir": test_dir,
            "empty_dir": empty_dir
        }
        shutil.rmtree(test_dir)

    def test_read_images_success(self, setup_test_directory):
        images = read_images(setup_test_directory["test_dir"])
        assert isinstance(images, list)
        assert len(images) >= 3
        assert all(isinstance(img, np.ndarray) for img in images)

    def test_read_images_empty_directory(self, setup_test_directory):
        images = read_images(setup_test_directory["empty_dir"])
        assert isinstance(images, list)
        assert len(images) == 0

    def test_read_images_directory_not_found(self):
        with pytest.raises(FileNotFoundError):
            read_images("/nonexistent/directory")

    def test_read_images_max_limit(self, setup_test_directory):
        images = read_images(setup_test_directory["test_dir"])
        assert len(images) <= 20

class TestPreprocessor:
    @pytest.fixture
    def sample_image(self):
        return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    @pytest.fixture
    def sample_pil_image(self):
        img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        return Image.fromarray(img_array)

    def test_preprocessor_default_init(self):
        preprocessor = Preprocessor()
        assert preprocessor.model_type == 'default'
        assert preprocessor.size == (224, 224)
        assert len(preprocessor.mean) == 3
        assert len(preprocessor.std) == 3

    @pytest.mark.parametrize("model_type", ['default', 'clip', 'openclip', 'vit'])
    def test_preprocessor_model_types(self, model_type, sample_image):
        preprocessor = Preprocessor(model_type=model_type)
        result = preprocessor(sample_image)
        assert isinstance(result, torch.Tensor)
        assert result.shape == torch.Size([3, 224, 224])
        assert result.dtype == torch.float32

    def test_preprocessor_custom_params(self, sample_image):
        custom_mean = [0.5, 0.5, 0.5]
        custom_std = [0.2, 0.2, 0.2]
        custom_size = (256, 256)
        preprocessor = Preprocessor(
            size=custom_size,
            mean=custom_mean,
            std=custom_std,
            model_type='clip'
        )
        result = preprocessor(sample_image)
        assert result.shape == torch.Size([3, 256, 256])
        assert preprocessor.mean == custom_mean
        assert preprocessor.std == custom_std
        assert preprocessor.size == custom_size

    def test_preprocessor_with_kwargs(self, sample_image):
        preprocessor = Preprocessor(
            model_type='clip',
            use_center_crop=False
        )
        assert preprocessor.use_center_crop is False
        result = preprocessor(sample_image)
        assert isinstance(result, torch.Tensor)

    def test_preprocessor_numpy_input(self, sample_image):
        preprocessor = Preprocessor()
        result = preprocessor(sample_image)
        assert isinstance(result, torch.Tensor)
        assert result.shape == torch.Size([3, 224, 224])

    def test_preprocessor_pil_input(self, sample_pil_image):
        preprocessor = Preprocessor()
        result = preprocessor(sample_pil_image)
        assert isinstance(result, torch.Tensor)
        assert result.shape == torch.Size([3, 224, 224])

    def test_preprocessor_invalid_input(self):
        preprocessor = Preprocessor()
        with pytest.raises(ValueError):
            preprocessor("invalid input")
        with pytest.raises(ValueError):
            preprocessor(123)

    def test_preprocessor_batch_processing(self, sample_image):
        preprocessor = Preprocessor()
        batch_images = [sample_image, sample_image, sample_image]
        batch_result = preprocessor.batch(batch_images)
        assert isinstance(batch_result, list)
        assert len(batch_result) == 3
        assert all(isinstance(tensor, torch.Tensor) for tensor in batch_result)
        stacked_result = preprocessor.batch_stack(batch_images)
        assert isinstance(stacked_result, torch.Tensor)
        assert stacked_result.shape == torch.Size([3, 3, 224, 224])

    def test_preprocessor_update_config(self, sample_image):
        preprocessor = Preprocessor(model_type='default')
        preprocessor.update_config(
            size=(512, 512),
            mean=[0.5, 0.5, 0.5],
            std=[0.2, 0.2, 0.2]
        )
        result = preprocessor(sample_image)
        assert result.shape == torch.Size([3, 512, 512])
        assert preprocessor.size == (512, 512)
        assert preprocessor.mean == [0.5, 0.5, 0.5]
        assert preprocessor.std == [0.2, 0.2, 0.2]

    def test_preprocessor_mixed_input_types(self, sample_image, sample_pil_image):
        preprocessor = Preprocessor()
        mixed_batch = [sample_image, sample_pil_image]
        result = preprocessor.batch_stack(mixed_batch)
        assert isinstance(result, torch.Tensor)
        assert result.shape == torch.Size([2, 3, 224, 224])

class TestIntegration:
    @pytest.fixture(scope="class")
    def setup_integration_test(self):
        test_dir = tempfile.mkdtemp()
        for i in range(5):
            img_path = os.path.join(test_dir, f"img_{i}.jpg")
            test_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
            pil_img = Image.fromarray(test_image)
            pil_img.save(img_path)
        yield {"test_dir": test_dir}
        shutil.rmtree(test_dir)

    def test_full_pipeline(self, setup_integration_test):
        images = read_images(setup_integration_test["test_dir"])
        assert len(images) == 5
        for model_type in ['default', 'clip', 'openclip', 'vit']:
            preprocessor = Preprocessor(model_type=model_type)
            single_result = preprocessor(images[0])
            assert isinstance(single_result, torch.Tensor)
            batch_result = preprocessor.batch_stack(images[:3])
            assert batch_result.shape == torch.Size([3, 3, 224, 224])

    def test_error_handling_integration(self, setup_integration_test):
        invalid_file = os.path.join(setup_integration_test["test_dir"], "invalid.txt")
        with open(invalid_file, 'w') as f:
            f.write("invalid")
        images = read_images(setup_integration_test["test_dir"])
        assert len(images) == 5
        preprocessor = Preprocessor()
        result = preprocessor.batch_stack(images)
        assert result.shape[0] == 5

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

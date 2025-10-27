import unittest
import os
import torch
import tempfile
from models.prompt_based_attribute_analyzer import PromptBasedAttributeAnalyzer

class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(10, 2)
    def forward(self, x, **kwargs):
        return self.linear(x)

class TestCheckpoint(unittest.TestCase):
    def setUp(self):
        self.device = torch.device("cpu")
        self.model = DummyModel()
        self.attribute_names = ["attr1", "attr2"]
        self.prompts = ["prompt1", "prompt2"]
        self.preprocess = lambda x: torch.randn(len(x), 10)  # Dummy preprocess
        self.tokenizer = lambda prompts, **kwargs: {"input_ids": torch.ones((len(prompts), 5), dtype=torch.long)}
        self.analyzer = PromptBasedAttributeAnalyzer(
            model=self.model,
            attribute_names=self.attribute_names,
            device=self.device,
            preprocess=self.preprocess,
            tokenizer=self.tokenizer,
            prompts=self.prompts
        )
        self.optimizer = torch.optim.Adam(self.model.parameters())

    def test_save_and_load_checkpoint(self):
        with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as tmp:
            path = tmp.name
        # 儲存
        self.analyzer.save_checkpoint(path, optimizer=self.optimizer, epoch=5, extra={"note": "test"})
        # 修改模型參數
        for param in self.model.parameters():
            param.data += 1.0
        # 載入
        checkpoint = self.analyzer.load_checkpoint(path, optimizer=self.optimizer)
        # 驗證模型參數已還原
        for param1, param2 in zip(self.model.parameters(), DummyModel().parameters()):
            self.assertTrue(param1.shape == param2.shape)
        # 驗證其他資訊
        self.assertEqual(self.analyzer.attribute_names, self.attribute_names)
        self.assertEqual(self.analyzer.prompts, self.prompts)
        self.assertEqual(checkpoint.get("epoch"), 5)
        self.assertEqual(checkpoint.get("extra")["note"], "test")
        os.remove(path)

    def test_load_checkpoint_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.analyzer.load_checkpoint("not_exist_file.pth")

    def test_load_checkpoint_format_error(self):
        with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as tmp:
            path = tmp.name
            tmp.write(b"not a pytorch checkpoint")
        with self.assertRaises(RuntimeError):
            self.analyzer.load_checkpoint(path)
        os.remove(path)

if __name__ == "__main__":
    unittest.main()
ㄙ
import unittest
from backend.inference_service.pipeline_controller import PipelineController

class DummyPreprocessor:
    def preprocess(self, input_data):
        return f"preprocessed({input_data})"

class DummyModelAnalyzer:
    def __call__(self, preprocessed_data):
        return f"model_output({preprocessed_data})"

class DummyPostprocessor:
    def __call__(self, model_output):
        return f"postprocessed({model_output})"

class TestPipelineController(unittest.TestCase):
    def setUp(self):
        self.preprocessor = DummyPreprocessor()
        self.model_analyzer = DummyModelAnalyzer()
        self.postprocessor = DummyPostprocessor()
        self.pipeline = PipelineController(
            self.preprocessor,
            self.model_analyzer,
            self.postprocessor
        )

    def test_pipeline_run(self):
        input_data = "raw_input"
        result = self.pipeline.run(input_data)
        self.assertEqual(
            result,
            "postprocessed(model_output(preprocessed(raw_input)))"
        )

    def test_pipeline_with_empty_input(self):
        result = self.pipeline.run("")
        self.assertEqual(
            result,
            "postprocessed(model_output(preprocessed()))"
        )

if __name__ == "__main__":
    unittest.main()
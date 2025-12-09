import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
import unittest
from postprocess.PostprocessManager import PostprocessManager

class TestPostprocessManager(unittest.TestCase):
    def setUp(self):
        self.postprocessor = PostprocessManager()
        self.sample_output = [
            {"attribute_type": "gender", "name": "male", "score": 0.95},
            {"attribute_type": "clothes", "name": "coat", "score": 0.95},
            {"attribute_type": "gender", "name": "female", "score": 0.45},
            {"attribute_type": "clothes", "name": "tshirt", "score": 0.60},
            {"attribute_type": "action", "name": "walking", "confidence": 0.92},
            {"attribute_type": "action", "name": "running", "confidence": 0.30}
        ]

    def test_grouping_and_sorting(self):
        result = self.postprocessor(
            self.sample_output,
            output_format="dict",
            sort_by=None,
            score_fields=["score", "confidence"],
            descending=True
        )
        self.assertIn("gender", result)
        self.assertEqual(result["gender"][0]["score"], 0.95)
        self.assertEqual(result["clothes"][0]["score"], 0.95)
        self.assertEqual(result["action"][0]["confidence"], 0.92)

    def test_score_threshold(self):
        result = self.postprocessor(
            self.sample_output,
            output_format="dict",
            score_threshold=0.9
        )
        self.assertEqual(len(result["gender"]), 1)
        self.assertEqual(result["gender"][0]["name"], "male")
        self.assertEqual(len(result["clothes"]), 1)
        self.assertEqual(result["clothes"][0]["name"], "coat")
        self.assertEqual(len(result["action"]), 1)
        self.assertEqual(result["action"][0]["name"], "walking")

    def test_json_output(self):
        result_json = self.postprocessor(
            self.sample_output,
            output_format="json"
        )
        self.assertIsInstance(result_json, str)
        self.assertIn('"gender"', result_json)

    def test_dataframe_output(self):
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not installed")
        df = self.postprocessor(
            self.sample_output,
            output_format="dataframe"
        )
        self.assertTrue("attribute_type" in df.columns)
        self.assertTrue("name" in df.columns)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            self.postprocessor(12345, output_format="dict")

    def test_no_score_field(self):
        data = [
            {"attribute_type": "other", "name": "unknown"}
        ]
        result = self.postprocessor(data, output_format="dict")
        self.assertIn("other", result)
        self.assertEqual(len(result["other"]), 1)

if __name__ == "__main__":
    unittest.main()
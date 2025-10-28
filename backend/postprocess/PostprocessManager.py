import json
from typing import Any, Dict, List, Union
import logging

try:
    import pandas as pd
except ImportError:
    pd = None

class PostprocessManager:
    """
    Convert raw model outputs into structured formats.
    """
    def __call__(self, model_output: Any, output_format: str = "dict") -> Union[Dict, str]:
        """
        Args:
            model_output (Any): The raw output from the model.
        Returns:
            Union[Dict, List]: The structured output after postprocessing.
        """
        result = self._to_dict(model_output)
        # TODO: Implement additional postprocessing logic if needed
        if output_format == "dict":
            return result
        elif output_format == "json":
            return json.dumps(result)
        elif output_format == "dataframe":
            if pd is None:
                logging.error("pandas is not installed but 'dataframe' output was requested.")
                raise ImportError("pandas is required for 'dataframe' output_format.")
            try:
                return pd.DataFrame(result["results"]) if "results" in result else pd.DataFrame([result])
            except Exception as e:
                logging.error(f"Failed to convert result to DataFrame: {e}")
                raise
        else:
            logging.error(f"Unsupported output format: {output_format}")
            raise ValueError(f"Unsupported output format: {output_format}")
        
    def _to_dict(self, model_output: Any) -> Dict:
        # TODO: Implement conversion logic based on model output structure
        if isinstance(model_output, dict):
            return model_output
        elif isinstance(model_output, list):
            return {"results": model_output}
        else:
            logging.error(f"Unsupported model_output type: {type(model_output)}")
            raise TypeError("Unsupported model_output type for postprocessing")
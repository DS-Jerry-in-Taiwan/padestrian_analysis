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
    def __call__(self, 
                 model_output: Any, 
                 output_format: str = "dict",
                 sort_by = None,
                 score_fields: List[str] = ["score", "confidence", "probability"],
                 descending: bool = True,
                 score_threshold: float = None
    ) -> Union[Dict, str]:
        """
        Args:
            model_output (Any): The raw output from the model.
        Returns:
            Union[Dict, List]: The structured output after postprocessing.
        """
        result = self._to_dict(model_output,            
                               sort_by=sort_by,
                               score_fields=score_fields,
                               descending=descending,
                               score_threshold=score_threshold,
                               )
        if output_format == "dict":
            return result
        elif output_format == "json":
            return json.dumps(result, ensure_ascii=False)
        elif output_format == "dataframe":
            if pd is None:
                logging.error("pandas is not installed but 'dataframe' output was requested.")
                raise ImportError("pandas is required for 'dataframe' output_format.")
            try:
                flat = []
                for v in result.values():
                    flat.extend(v)
                df = pd.DataFrame(flat)
                return df
            except Exception as e:
                logging.error(f"Failed to convert result to DataFrame: {e}")
                raise
        else:
            logging.error(f"Unsupported output format: {output_format}")
            raise ValueError(f"Unsupported output format: {output_format}")
        
    def _to_dict(self, 
                 model_output: Any,
                 sort_by: str = None,
                 score_fields: List[str] = ["score", "confidence", "probability"],
                 descending: bool = True,
                 score_threshold: float = None
    ) -> Dict:
        if isinstance(model_output, dict):
            return model_output
        elif isinstance(model_output, list):
            grouped = {}
            for item in model_output:
                attr_type = item.get("attribute_type", "unknown")
                grouped.setdefault(attr_type, []).append(item)
            for k, v in grouped.items():
                filtered = v
                if score_threshold is not None:
                    # 找到第一個存在的分數欄位
                    score_key = sort_by
                    if not score_key and v:
                        for field in score_fields:
                            if field in v[0]:
                                score_key = field
                                break
                    if score_key:
                        filtered = [item for item in v if item.get(score_key, 0) >= score_threshold]
                    else:
                        logging.info(f"No score field found for filtering in group '{k}', skipping threshold filter.")
                # 排序
                sorted_key = sort_by
                if not sorted_key and filtered:
                    for field in score_fields:
                        if field in filtered[0]:
                            sorted_key = field
                            break
                if sorted_key:
                    grouped[k] = sorted(
                        filtered,
                        key=lambda x: x.get(sorted_key, 0),
                        reverse=descending
                    )
                else:
                    grouped[k] = filtered
            return grouped
        else:
            logging.error(f"Unsupported model_output type: {type(model_output)}")
            raise TypeError("Unsupported model_output type for postprocessing")
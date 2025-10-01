from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AttributeAnalyzerBase(ABC):
    """
    屬性分析器基底類別，所有屬性分析器需繼承並實作 analyze 方法。
    """

    @abstractmethod
    def analyze(self, image: Any, boxes: List[List[float]]) -> List[Dict]:
        """
        針對每個 bounding box 分析屬性。

        Args:
            image: 單張影像（如 numpy array 或 tensor）。
            boxes: List of bounding boxes，每個 box 為 [x1, y1, x2, y2]。

        Returns:
            List[Dict]：每個 box 的屬性分析結果（dict 格式）。
        """
        pass
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

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
    
    @abstractmethod
    def save_checkpoint(self,
                        filepath: str,
                        optimizer: Optional[Any]= None,
                        epoch: Optional[int] = None,
                        extra: Optional[Dict[str, Any]] = None
                        ) -> None:
        """
        model checkpoint
        Args:
            filepath (str): 儲存路徑
            optimizer (可為 PyTorch、TensorFlow 等）: 優化器
            epoch (int, optional): 訓練輪數
            extra (Dict[str, Any], optional): 額外資訊
        """
        pass
    
    @abstractmethod
    def load_checkpoint(
        self,
        filepath: str,
        optimizer: Optional[Any] = None
        ) -> Dict[str, Any]:
        """
        Load model checkpoint
        Args:
            filepath (str): 儲存路徑
            optimizer (可為 PyTorch、TensorFlow 等）: 優化器
        """
        pass    
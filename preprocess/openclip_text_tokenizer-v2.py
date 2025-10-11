import time
import numpy as np
from typing import List, Union, Dict, Any
from open_clip.tokenizer import SimpleTokenizer
from transformers import CLIPTokenizerFast
from preprocess.base_preprocessor import BaseTextTokenizer
from transformers import CLIPTokenizerFast

class OpenCLIPTEXTTokenizer(BaseTextTokenizer):
    def __init__(self, vocab_path: str = None, max_length: int = 77):
        """
        Tokenizer for OpenCLIP text models.
        Args:
            vocab_path (str, optional): Path to the vocabulary file. If None, uses the
            default CLIP tokenizer from Hugging Face.
        """
        self.tokenizer = SimpleTokenizer(vocab_path) if vocab_path else SimpleTokenizer()
        self.max_length = max_length

        
    def __call__(
        self, 
        texts: Union[str, List[str]], 
        padding: bool = True,
        truncation: bool = True,
        max_length: int = 77,
        return_attention_mask: bool = True,
        return_tensors: str = None,
        **kwargs
        ) -> Dict[str, Any]:
        if isinstance(texts, str):
            texts = [texts]
        max_len = max_length if max_length is not None else self.max_length
        
        time_start = time.time()
        # 1. 逐句 encode
        ids_list = []
        for text in texts:
            ids = self.tokenizer.encode(text)
            if truncation and len(ids) > max_len:
                ids = ids[:max_len]
            ids_list.append(ids)

        # 2. 用 numpy 批次 padding
        batch_size = len(ids_list)
        input_ids = np.full((batch_size, max_len), 0, dtype=np.int32)
        attention_mask = np.zeros((batch_size, max_len), dtype=np.int32)

        for i, ids in enumerate(ids_list):
            length = min(len(ids), max_len)
            input_ids[i, :length] = ids[:length]
            attention_mask[i, :length] = 1
            
        result = {"input_ids": input_ids.tolist()}
        if return_attention_mask:
            result["attention_mask"] = attention_mask.tolist()
        if return_tensors == "np":
            result = {"input_ids": input_ids, "attention_mask": attention_mask}
        elif return_tensors == "pt":
            import torch
            result = {k: torch.tensor(v) for k, v in result.items()}
        end_time = time.time()
        print(f"Tokenization time: {end_time - time_start:.4f} seconds for {len(texts)} texts.")
        return result
    
    def process_batch(self, texts: List[str], **kwargs) -> List[List[int]]:
        return self.__call__(texts, **kwargs)
    
if __name__ == "__main__":
    tokenizer = OpenCLIPTEXTTokenizer()
    texts = ['Hello, world!', 'This is a test.'] 
    tokens = tokenizer(texts)
    print("Texts:", texts,";", "Tokens:", tokens)
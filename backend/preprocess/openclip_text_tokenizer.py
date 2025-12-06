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
        max_length: int = None,
        return_attention_mask: bool = True,
        return_tensors: str = None,
        **kwargs
        ) -> Dict[str, Any]:
        if not isinstance(texts, (str, list)):
            raise ValueError("Input texts must be a string or a list of strings.")
        if isinstance(texts, list):
            if not all(isinstance(t, str) for t in texts):
                raise ValueError("All elements in the input list must be strings.")
        if isinstance(texts, str):
            texts = [texts]
            
        max_len = max_length if max_length is not None else self.max_length
        
        input_ids = []
        attention_masks = []
        for idx, text in enumerate(texts):
            try:
                ids = self.tokenizer.encode(text)
            except Exception as e:
                raise RuntimeError(f"Tokenization failed for text at index {idx}: {e}")
            if truncation and len(ids) > max_len:
                ids = ids[:max_len]
            if padding and  len(ids) < max_len:
                pad_len = max_len - len(ids)
                ids = ids + [0] * pad_len  # Assuming 0 is the padding token ID
            mask = [1 if id != 0 else 0 for id in ids]
            if padding and len(mask) < max_len:
                mask += [0] * (max_len - len(mask))
            input_ids.append(ids)
            attention_masks.append(mask)
            
        result = {"input_ids": input_ids}
        
        if return_attention_mask:
            result['attention_mask'] = attention_masks
        try:
            if return_tensors == 'pt':
                import torch
                result = {k: torch.tensor(v) for k, v in result.items()}
            elif return_tensors == 'np':
                import numpy as np
                result = {k: np.array(v) for k, v in result.items()}
        except Exception as e:
            raise RuntimeError(f"Failed to convert result to tensor: {e}")
        return result
    
    def process_batch(self, texts: List[str], **kwargs) -> List[List[int]]:
        return self.__call__(texts, **kwargs)
    
if __name__ == "__main__":
    tokenizer = OpenCLIPTEXTTokenizer()
    texts = ['Hello, world!', 'This is a test.'] 
    tokens = tokenizer(texts)
    print("Texts:", texts,";", "Tokens:", tokens)
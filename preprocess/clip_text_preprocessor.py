from typing import List, Union, Dict, Any
from transformers import CLIPTokenizerFast
from preprocess.base_preprocessor import BaseTextTokenizer

class CLIPTextTokenizer(BaseTextTokenizer):
    def __init__(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
        max_length: int = 77,
    ):
        """
        CLIP text tokenizer implementation
        """
        self.tokenizer = CLIPTokenizerFast.from_pretrained(model_name)
        self.max_length = max_length
    
    def __call__(
        self,
        texts: Union[str,List[str]],
        padding: bool = True,
        truncation: bool =True,
        max_length: int = None,
        return_tensors: str = None,
        return_attention_mask: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        if isinstance(texts, str):
            texts = [texts]

        max_length = max_length if max_length is not None else self.max_length

        result = self.tokenizer(
            texts,
            padding="max_length" if padding else False,
            truncation=truncation,
            max_length=max_length,
            return_tensors=return_tensors,
            return_attention_mask=return_attention_mask,
            **kwargs
        )
        
        # convert BatchEncoding to dict
        if return_tensors is None:
            result = {k: v for k, v in result.items()}
        else:
            return dict(result)
        
    def process_batch(self, texts: List[str], **kwargs) -> Dict[str, Any]:
        """
        Process a batch of texts
        """
        return self.__call__(texts, **kwargs)
        
if __name__ == "__main__":
    tokenizer = CLIPTextTokenizer()
    texts = ["A photo of a cat", "A photo of a dog"]
    outputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=77,
        return_attention_mask=True,
        return_tensors="np"
    )
    print(outputs)
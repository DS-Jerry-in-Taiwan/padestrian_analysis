from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ImageRequest(BaseModel):
    image_url: str = Field(..., description="Image URL")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image string")
    attributes: Optional[List[str]] = Field(None, description="List of attributes to analyze")
    
class BatchImageRequest(BaseModel):
    images: List[ImageRequest] # 可為 base64 或 image_url
    attributes: Optional[List[str]] = None   
    
class Attribute(BaseModel):
    attribute_type: str
    name: str
    score: Optional[float]
    
class PipelineResponse(BaseModel):
    results: Dict[str, List[Attribute]]
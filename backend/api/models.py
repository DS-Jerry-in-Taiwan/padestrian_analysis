from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ImageRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image string")
    
class Attribute(BaseModel):
    attribute_type: str
    name: str
    score: Optional[float]
    
class PipelineResponse(BaseModel):
    results: Dict[str, List[Attribute]]
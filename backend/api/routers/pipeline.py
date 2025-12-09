from fastapi import APIRouter, HTTPException
from ..models import ImageRequest, PipelineResponse, Attribute

router = APIRouter(
    prefix="/api/pipeline",
    tags=["Pipeline"]
)

@router.post("", response_model=PipelineResponse)
async def pipeline_endpoint(request: ImageRequest):
    if not request.image_url or request.image_url.strip() == "":
        raise HTTPException(status_code=422, detail="image_url is required and cannot be empty")
    return PipelineResponse(
        results={
            "gender": [Attribute(attribute_type="gender", name="male", score=0.95)],
            "clothes": [Attribute(attribute_type="clothes", name="coat", score=0.88)]
        }
    )
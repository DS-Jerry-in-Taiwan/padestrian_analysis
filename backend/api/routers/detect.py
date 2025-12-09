from fastapi import APIRouter, HTTPException
from ..models import ImageRequest, Attribute

router = APIRouter(
    prefix="/api/detect",
    tags=["Detection"]
)

@router.post("")
async def detect(request: ImageRequest):
    if not request.image_url or request.image_url.strip() == "":
        raise HTTPException(status_code=422, detail="image_url is required and cannot be empty")
    return {
        "results": [
            {"attribute_type": "gender", "name": "male", "score": 0.95},
            {"attribute_type": "clothes", "name": "coat", "score": 0.88}
        ]
    }
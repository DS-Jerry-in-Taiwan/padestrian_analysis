from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ImageRequest, PipelineResponse
# create FastAPI app instance
app = FastAPI(
    title="PAG API",
    description="API for Pedestrian Attribute Recognition System",
    version="1.0.0",
    )

# settings for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#TODO : Add your API routes and logic here

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/detect")
async def detecct(request: ImageRequest):
    #TODO : image detection logic here
    return {
        "attributes": [
            {"attribute_type": "gender", "name": "male", "score": 0.0},
            {"attribute_type": "clothes", "name": "coat", "score": 0.88}
        ]
    }

@app.post("/pipeline", response_model=PipelineResponse)
async def pipeline_endpoint(request: ImageRequest):
    #TODO: Implement the pipeline processing logic here
        return PipelineResponse(results={
        "gender": [Attribute(attribute_type="gender", name="male", score=0.95)],
        "clothes": [Attribute(attribute_type="clothes", name="coat", score=0.88)]
    })

@app.post("/analyze", response_model=PipelineResponse)
async def analyze_endpoint(request: ImageRequest):
    #TODO: Implement the analysis logic here
    return PipelineResponse(results={
        "gender": [Attribute(attribute_type="gender", name="male", score=0.95)],
        "clothes": [Attribute(attribute_type="clothes", name="coat", score=0.88)]
    })

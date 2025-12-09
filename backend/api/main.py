from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, detect, pipeline, analyze

app = FastAPI(
    title = "PAG API",
    description = "API for Pedestrian Attribute Recognition System",
    version = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(health.router)
app.include_router(detect.router)
app.include_router(pipeline.router)
app.include_router(analyze.router)
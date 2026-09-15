from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="DataForge AI",
    description=(
        "AI-powered data intelligence "
        "and natural language database system."
    ),
    version="1.0.0",
)


app.include_router(router, prefix="/api/v1")
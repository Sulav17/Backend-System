from fastapi import FastAPI
from app.api import upload, rag

app = FastAPI()

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(rag.router, prefix="/api", tags=["RAG + Interview"])

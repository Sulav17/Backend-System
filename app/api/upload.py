from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.embeddings.chunking import recursive_chunk, semantic_chunk, custom_chunk
from app.embeddings.embedder import generate_embeddings
from app.db.vector_store import init_qdrant_collection, add_chunks_to_qdrant
from app.models.schemas import UploadMetadata

import os
import fitz  # pymupdf
import shutil

router = APIRouter()


def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format")


@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    chunking_method: str = Form("recursive"),
    embedding_model: str = Form("all-MiniLM-L6-v2")
):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only .pdf or .txt allowed.")

    # Save file
    file_path = f"data/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    try:
        text = extract_text_from_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Chunk text
    if chunking_method == "recursive":
        chunks = recursive_chunk(text)
    elif chunking_method == "semantic":
        chunks = semantic_chunk(text)
    elif chunking_method == "custom":
        chunks = custom_chunk(text)
    else:
        raise HTTPException(status_code=400, detail="Invalid chunking method.")

    # Embed chunks
    embeddings = generate_embeddings(chunks, embedding_model)

    # Save to Qdrant
    init_qdrant_collection("documents")
    metadata = UploadMetadata(
        file_name=file.filename,
        chunking_method=chunking_method,
        embedding_model=embedding_model
    )
    add_chunks_to_qdrant("documents", chunks, embeddings, metadata)

    return {"status": "success", "chunks_uploaded": len(chunks)}

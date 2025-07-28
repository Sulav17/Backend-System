from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, CollectionStatus
from uuid import uuid4
import os

client = QdrantClient(url=os.getenv("VECTOR_DB_HOST", "http://localhost:6333"))


def init_qdrant_collection(collection_name="documents"):
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # For MiniLM
        )


def add_chunks_to_qdrant(collection_name, chunks, embeddings, metadata):
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "file_name": metadata.file_name,
                "chunking_method": metadata.chunking_method,
                "embedding_model": metadata.embedding_model
            }
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=collection_name, points=points)

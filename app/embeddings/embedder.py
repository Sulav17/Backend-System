from sentence_transformers import SentenceTransformer
from typing import List


def generate_embeddings(chunks: List[str], model_name="all-MiniLM-L6-v2") -> List[List[float]]:
    model = SentenceTransformer(model_name)
    return model.encode(chunks).tolist()

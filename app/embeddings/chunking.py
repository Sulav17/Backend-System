from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


def recursive_chunk(text: str, chunk_size=500, chunk_overlap=100) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)


def semantic_chunk(text: str, model_name="all-MiniLM-L6-v2", max_tokens=100) -> List[str]:
    model = SentenceTransformer(model_name)
    sentences = text.split('.')
    embeddings = model.encode(sentences)
    
    clusters, current, current_embeds = [], [], []
    for sent, emb in zip(sentences, embeddings):
        current.append(sent)
        current_embeds.append(emb)
        if len(current_embeds) >= max_tokens:
            clusters.append(". ".join(current))
            current, current_embeds = [], []
    if current:
        clusters.append(". ".join(current))
    return clusters


def custom_chunk(text: str) -> List[str]:
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

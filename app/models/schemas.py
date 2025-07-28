from pydantic import BaseModel, Field
from typing import Literal


class UploadMetadata(BaseModel):
    file_name: str
    chunking_method: Literal["recursive", "semantic", "custom"]
    embedding_model: str

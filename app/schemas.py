from typing import List
from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    document_id: str = Field(..., description="Logical ID for the document")
    text: str = Field(..., description="Raw document text")


class IngestResponse(BaseModel):
    document_id: str
    chunks_created: int


class ContextChunk(BaseModel):
    document_id: str
    chunk_id: str
    score: float
    text_preview: str


class AskRequest(BaseModel):
    question: str
    top_k: int = Field(3, ge=1, le=10)


class AskResponse(BaseModel):
    question: str
    answer: str
    context_chunks: List[ContextChunk]


class HealthResponse(BaseModel):
    status: str
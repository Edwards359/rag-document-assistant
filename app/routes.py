from fastapi import APIRouter

from . import schemas
from .config import settings
from .services.llm_client import get_llm_client
from .services.rag_service import InMemoryChunkStore, RAGService


router = APIRouter()

_chunk_store = InMemoryChunkStore()
_llm_client = get_llm_client(settings.llm_provider)
_rag_service = RAGService(_chunk_store, _llm_client)


@router.get("/health", response_model=schemas.HealthResponse)
async def health() -> schemas.HealthResponse:
    return schemas.HealthResponse(status="ok")


@router.post("/ingest", response_model=schemas.IngestResponse)
async def ingest(request: schemas.IngestRequest) -> schemas.IngestResponse:
    chunks_created = _rag_service.ingest_document(
        document_id=request.document_id,
        text=request.text,
    )
    return schemas.IngestResponse(document_id=request.document_id, chunks_created=chunks_created)


@router.post("/ask", response_model=schemas.AskResponse)
async def ask(request: schemas.AskRequest) -> schemas.AskResponse:
    answer, chunks = await _rag_service.ask(request.question, top_k=request.top_k)
    ctx = [
        schemas.ContextChunk(
            document_id=c.document_id,
            chunk_id=c.chunk_id,
            score=0.0,
            text_preview=c.text[:200],
        )
        for c in chunks
    ]
    return schemas.AskResponse(question=request.question, answer=answer, context_chunks=ctx)
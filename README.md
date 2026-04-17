## 🇷🇺 Обзор для заказчика

**RAG Document Assistant** — AI‑ассистент, который отвечает на вопросы по вашим документам.

- **Для чего:** сократить ручной поиск по PDF, регламентам и инструкциям.
- **Что делает:** принимает текст документов, разбивает их на фрагменты, находит релевантные части и формирует контекстный ответ.
- **Где полезен:** внутренние базы знаний, HR/IT‑политики, product‑документация, инструкции для сотрудников.
- **Пример кейса:** сотрудник задаёт вопрос по отпускной политике → ассистент возвращает ответ + выдержки из актуального документа.

Дальше в README показано:
- как устроена архитектура RAG‑решения (ingestion → retrieval → answer),
- какие эндпоинты есть в API,
- как это может быть расширено до продакшн‑уровня (векторное хранилище, реальный LLM).

---
# RAG Document Assistant
_Practical RAG-style document question answering API_

## Overview
RAG Document Assistant is a small, focused backend that demonstrates how to answer questions based on your own documents.  
It provides a simple API to ingest documents, split them into chunks, store them in memory, retrieve relevant chunks, and generate a contextual answer.

## Business problem
Teams lose time searching through PDFs, policies, and scattered documents.  
Employees either read long files manually or ping “the expert” for every question.

## Solution
This project shows a clean, extensible RAG-style backend where:
- documents are ingested and chunked,
- relevant chunks are retrieved for each question,
- a prompt layer combines question + context into a model-ready input,
- the model generates a contextual answer.

You can plug in a real vector DB and LLM later — the architecture is already prepared for that.

## Key features
- **Document ingestion** via `/ingest`
- **In-memory chunk store** (replaceable with any vector DB)
- **Simple retrieval logic** based on keyword / scoring
- **Context-aware answer generation** with a clear prompt layer
- **FastAPI API** ready for integration into products or tools

## Architecture

```text
User
  ↓
FastAPI (POST /ask)
  ↓
Retriever
  ↓
Document Chunks (in-memory store)
  ↓
Prompt Builder → LLM Client (mock or real)
  ↓
Contextual Answer
```

## Tech stack
- Python 3.12+
- FastAPI
- Pydantic
- python-dotenv

## API endpoints

- `POST /ingest` — ingest a document as text
- `POST /ask` — ask a question about ingested documents
- `GET /health` — health check

## Example request / response

### POST /ingest

```json
{
  "document_id": "employee_handbook_v1",
  "text": "Long text of your document goes here..."
}
```

### POST /ask

**Request:**

```json
{
  "question": "What is the vacation policy?",
  "top_k": 3
}
```

**Response (example):**

```json
{
  "question": "What is the vacation policy?",
  "answer": "The handbook states that employees are entitled to 20 days of paid vacation per year...",
  "context_chunks": [
    {
      "document_id": "employee_handbook_v1",
      "chunk_id": "employee_handbook_v1-0",
      "score": 0.82,
      "text_preview": "Employees are entitled to 20 days of paid vacation per year..."
    }
  ]
}
```

## Example workflow
1. Client ingests one or more documents via `/ingest`.
2. The API splits them into chunks and stores them in an in-memory index.
3. The user (or another service) calls `/ask` with a natural-language question.
4. The retriever finds the most relevant chunks.
5. The prompt layer builds an input for the LLM client.
6. The LLM client (mock or real) returns a contextual answer.

## RAG in this project
RAG (Retrieval-Augmented Generation) here means:
- **Retrieve**: select relevant document chunks for a question.
- **Augment**: build a prompt that includes those chunks as context.
- **Generate**: let the model answer using that context.

The retrieval is intentionally simple (in-memory, keyword-based) but the code is structured so that any vector database can be plugged in later.

## Prompt engineering relevance
The answer quality heavily depends on how we:
- frame the question + context,
- instruct the model to ground its answer in the provided chunks,
- ask it to point out when there is not enough information.

The `llm_client.py` and service layer make it easy to tweak prompts in one place.

## Possible integrations
- internal knowledge portals
- admin panels (document management + Q&A)
- chatbots (Telegram, web widget) that call the `/ask` endpoint
- workflow tools (e.g. n8n) that send documents and questions to this API

## Project structure

```text
rag-document-assistant/
  app/
    __init__.py
    main.py
    config.py
    schemas.py
    routes.py
    services/
      __init__.py
      rag_service.py
      llm_client.py
  data/
    README.md
  .env.example
  .gitignore
  requirements.txt
  README.md
```

## Future improvements
- Replace in-memory store with a real vector database (e.g. Chroma, FAISS, Pinecone).
- Add support for multiple document formats (PDF, DOCX, HTML).
- Add embeddings and similarity search.
- Add authentication and per-tenant isolation.
- Provide a small web UI or chat interface on top of the API.
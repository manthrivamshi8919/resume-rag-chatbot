# Resume RAG Chatbot

A FastAPI + Streamlit RAG chatbot that answers questions about your resume/portfolio using Pinecone for vector search and OpenRouter for LLM responses.

## Features

- **RAG-powered answers** grounded in your resume/portfolio content
- **Pinecone vector search** with local embeddings (sentence-transformers)
- **OpenRouter LLM integration** (configurable model)
- **Streamlit UI** for quick testing
- **FastAPI backend** ready to embed into any portfolio site
- **Citations** with source snippets and similarity scores

## Quick Start

### 1. Clone and install

```bash
git clone <repo-url>
cd rag-chatbot
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Server
PORT=8000
CORS_ORIGINS=*

# Pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=resume
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

# Embeddings (local)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# OpenRouter (LLM)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=deepseek/deepseek-chat

# Retrieval
TOP_K=5
MAX_CONTEXT_CHARS=12000
```

### 3. Ingest your resume

Place `resume.txt` or `resume.pdf` in the root and run:

```bash
python ingest.py resume.txt --source "Resume"
```

### 4. Start services

- **FastAPI backend**

```bash
python main.py
# or: uvicorn main:app --reload --port 8000
```

- **Streamlit UI (optional, for testing)**

In a new terminal:

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501 and chat.

## API Endpoints

- `GET /health` – health check
- `POST /chat` – ask a question (JSON body with `question`/`message`/`prompt`)
- `GET /docs` – auto-generated Swagger UI

Example:

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What are Vamshi\'s skills?"}'
```

## Project Structure

```
.
├── main.py              # FastAPI app entrypoint
├── streamlit_app.py     # Simple Streamlit UI
├── ingest.py            # Resume → Pinecone ingestion script
├── debug.py             # Debug Pinecone/embedding issues
├── requirements.txt     # Python deps
├── .env.example         # Env var template
├── .gitignore
├── README.md
└── app/
    ├── __init__.py
    ├── config.py        # Settings from .env
    ├── schemas.py       # Pydantic models
    ├── embeddings.py    # Local sentence‑transformers wrapper
    ├── pinecone_client.py # Pinecone index helper
    ├── llm.py           # OpenRouter client
    └── rag.py           # Retrieve → LLM pipeline
```

## Common Issues

### “No context” / “I couldn’t process your request”
- Pinecone index is empty: run `python ingest.py your_resume.txt`
- Dimension mismatch: delete and recreate the Pinecone index with the correct dimension (384 for the default model)

### 422 Unprocessable Entity on /chat
- Ensure `Content-Type: application/json`
- Send one of: `{"question": "..."} | {"message": "..."} | {"prompt": "..."}`

### Embedding model download errors
- Ensure the model name in `.env` is a public Hugging Face model (e.g., `sentence-transformers/all-MiniLM-L6-v2`)

## Deployment Notes

- **FastAPI**: Deploy on Render, Railway, or any Python host. Set env vars in the host.
- **Streamlit**: Optional; only for local testing.
- **Pinecone**: Create a Serverless index with 384 dimensions (cosine metric).
- **OpenRouter**: Get an API key and optionally set `OPENROUTER_SITE_URL`/`OPENROUTER_APP_NAME`.

## License

MIT

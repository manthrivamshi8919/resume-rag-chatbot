# Resume RAG Chatbot

A FastAPI + Streamlit RAG chatbot that answers questions about your resume/portfolio using Pinecone for vector search and OpenRouter for LLM responses.

## Features

- **Context-Aware Responses**: Provides RAG (Retrieval-Augmented Generation) answers strictly grounded in your provided resume or portfolio content.
- **Source Citations**: Returns exact source snippets and similarity scores for full transparency.
- **API-First Design**: A robust FastAPI backend that can be seamlessly integrated into any external portfolio website.
- **Interactive Web UI**: Includes a Streamlit interface for quick local testing and demonstration.

## Technologies Used

- **Frameworks**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance API backend), [Streamlit](https://streamlit.io/) (Frontend chat UI)
- **Vector Database**: [Pinecone](https://www.pinecone.io/) (Serverless vector search & retrieval)
- **Embeddings**: Pinecone Inference API (Generates text embeddings server-side without requiring local ML models like PyTorch)
- **LLM Integration**: [OpenRouter](https://openrouter.ai/) (Via OpenAI SDK) allowing flexible model configuration (e.g., DeepSeek, OpenAI, Claude)
- **Document Processing**: [PyPDF](https://pypdf.readthedocs.io/) for parsing logic from PDF resumes
- **Data Management**: [Pydantic](https://docs.pydantic.dev/) for data validation and settings configuration

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

# Embeddings (Pinecone Inference)
EMBEDDING_MODEL=multilingual-e5-large

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
    ├── embeddings.py    # Pinecone Inference wrapper
    ├── pinecone_client.py # Pinecone index helper
    ├── llm.py           # OpenRouter client
    └── rag.py           # Retrieve → LLM pipeline
```

## Common Issues

### “No context” / “I couldn’t process your request”
- Pinecone index is empty: run `python ingest.py your_resume.txt`
- Dimension mismatch: delete and recreate the Pinecone index with the correct dimension (1024 for the default `multilingual-e5-large` model)

### 422 Unprocessable Entity on /chat
- Ensure `Content-Type: application/json`
- Send one of: `{"question": "..."} | {"message": "..."} | {"prompt": "..."}`

### Embedding model invocation errors
- Ensure the model name in `.env` is supported by Pinecone Inference (e.g., `multilingual-e5-large` or `sentence-transformers/all-MiniLM-L6-v2`)

## Deployment Notes

- **FastAPI**: Deploy on Render, Railway, or any Python host. Set env vars in the host.
- **Streamlit**: Optional; only for local testing.
- **Pinecone**: Create a Serverless index with 1024 dimensions (cosine metric).
- **OpenRouter**: Get an API key and optionally set `OPENROUTER_SITE_URL`/`OPENROUTER_APP_NAME`.

## License

MIT

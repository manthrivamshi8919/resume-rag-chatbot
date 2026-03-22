from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.rag import answer_question
from app.schemas import ChatRequest, ChatResponse, Source


app = FastAPI(title="Resume RAG Chatbot API")

origins = [o.strip() for o in settings.cors_origins.split(",")] if settings.cors_origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] ,
)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer, sources = answer_question(req.text())
    return ChatResponse(
        answer=answer,
        sources=[Source(**s) for s in sources],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=False)

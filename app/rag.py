from .config import settings
from .embeddings import embed_texts
from .llm import get_llm_client
from .pinecone_client import get_index


def retrieve(query: str):
    index = get_index()
    qvec = embed_texts([query])[0]
    res = index.query(vector=qvec, top_k=settings.top_k, include_metadata=True)
    matches = res.get("matches", []) if isinstance(res, dict) else res.matches

    out = []
    for m in matches:
        md = m.get("metadata", {}) if isinstance(m, dict) else (m.metadata or {})
        out.append(
            {
                "id": m.get("id") if isinstance(m, dict) else m.id,
                "score": m.get("score") if isinstance(m, dict) else m.score,
                "text": md.get("text", ""),
                "source": md.get("source"),
            }
        )
    return out


def build_context(sources: list[dict]) -> str:
    parts: list[str] = []
    total = 0
    for i, s in enumerate(sources, start=1):
        chunk = (s.get("text") or "").strip()
        if not chunk:
            continue
        label = s.get("source") or s.get("id") or f"chunk-{i}"
        piece = f"[S{i} | {label}]\n{chunk}"
        if total + len(piece) > settings.max_context_chars:
            break
        parts.append(piece)
        total += len(piece)
    return "\n\n".join(parts)


def answer_question(question: str) -> tuple[str, list[dict]]:
    sources = retrieve(question)
    context = build_context(sources)

    client = get_llm_client()

    system = (
        "You are a resume/portfolio assistant. Answer using ONLY the provided context. "
        "If the context is insufficient, say you don't know and ask a clarifying question. "
        "Be concise and professional."
    )

    user = f"Context:\n{context}\n\nQuestion: {question}"

    resp = client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )

    answer = resp.choices[0].message.content or ""
    return answer, sources

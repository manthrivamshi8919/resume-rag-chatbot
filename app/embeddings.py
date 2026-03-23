from .config import settings
from .pinecone_client import get_pinecone_client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts using Pinecone Inference API (no local model / no PyTorch)."""
    pc = get_pinecone_client()
    result = pc.inference.embed(
        model=settings.embedding_model,
        inputs=texts,
        parameters={"input_type": "query", "truncate": "END"},
    )
    # result is a list of EmbeddingsList objects; each has a .values attribute
    return [item.values for item in result]

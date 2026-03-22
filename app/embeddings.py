from sentence_transformers import SentenceTransformer

from .config import settings


_model: SentenceTransformer | None = None


def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedder()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]

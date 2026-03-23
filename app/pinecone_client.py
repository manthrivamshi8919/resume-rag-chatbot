from pinecone import Pinecone, ServerlessSpec

from .config import settings

_pc: Pinecone | None = None


def get_pinecone_client() -> Pinecone:
    """Return a shared Pinecone client (lazy singleton)."""
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=settings.pinecone_api_key)
    return _pc


def get_index():
    pc = get_pinecone_client()

    existing = {idx["name"] for idx in pc.list_indexes()}
    if settings.pinecone_index not in existing:
        pc.create_index(
            name=settings.pinecone_index,
            dimension=settings.embedding_dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
        )

    return pc.Index(settings.pinecone_index)

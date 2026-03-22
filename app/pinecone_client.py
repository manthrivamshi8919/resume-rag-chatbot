from pinecone import Pinecone, ServerlessSpec

from .config import settings


def get_index():
    pc = Pinecone(api_key=settings.pinecone_api_key)

    existing = {idx["name"] for idx in pc.list_indexes()}
    if settings.pinecone_index not in existing:
        pc.create_index(
            name=settings.pinecone_index,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
        )

    return pc.Index(settings.pinecone_index)

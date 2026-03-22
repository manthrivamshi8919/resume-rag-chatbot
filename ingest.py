import os
import uuid
from pathlib import Path
from typing import Iterable

import pypdf
from dotenv import load_dotenv

from app.config import settings
from app.embeddings import embed_texts
from app.pinecone_client import get_index

load_dotenv()

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        reader = pypdf.PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        return path.read_text(encoding="utf-8")


def sliding_chunks(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> Iterable[str]:
    start = 0
    while start < len(text):
        end = start + size
        yield text[start:end]
        if end >= len(text):
            break
        start = end - overlap


def ingest_file(file_path: str | Path, source_name: str | None = None):
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    raw = read_text(path)
    if not raw.strip():
        raise ValueError("File appears empty after extraction.")

    chunks = list(sliding_chunks(raw))
    if not chunks:
        raise ValueError("No chunks created from file.")

    embeddings = embed_texts(chunks)

    index = get_index()
    to_upsert = [
        {
            "id": str(uuid.uuid4()),
            "values": vec,
            "metadata": {
                "text": chunk,
                "source": source_name or path.name,
            },
        }
        for chunk, vec in zip(chunks, embeddings)
    ]

    index.upsert(vectors=to_upsert)
    print(f"✅ Ingested {len(to_upsert)} chunks from {path.name} into Pinecone index '{settings.pinecone_index}'.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest a resume/portfolio file into Pinecone for RAG.")
    parser.add_argument("file", help="Path to a .txt or .pdf file")
    parser.add_argument("--source", help="Optional source name shown in citations")
    args = parser.parse_args()

    ingest_file(args.file, args.source)

import os
from dotenv import load_dotenv

from app.config import settings
from app.embeddings import embed_texts
from app.pinecone_client import get_index

load_dotenv()

def main():
    print("=== Debug: Pinecone Index Info ===")
    index = get_index()
    stats = index.describe_index_stats()
    print("Index stats:", stats)

    print("\n=== Sample vectors (first 5) ===")
    fetch = index.fetch(list(index.query(vector=[0.0]*384, top_k=5, include_metadata=True).get("matches", [])))
    for ids, vectors in fetch["vectors"].items():
        print(f"ID: {ids}")
        print(f"Metadata: {vectors.get('metadata', {})}")
        print("---")

    print("\n=== Embedding test ===")
    query = "What are Vamshi's skills?"
    vec = embed_texts([query])[0]
    print(f"Query: {query}")
    print(f"Embedding dim: {len(vec)}")
    print(f"First 5 values: {vec[:5]}")

    print("\n=== Pinecone search result ===")
    res = index.query(vector=vec, top_k=3, include_metadata=True)
    matches = res.get("matches", [])
    print(f"Returned {len(matches)} matches")
    for i, m in enumerate(matches, 1):
        print(f"Match {i}: score={m.get('score')}, id={m.get('id')}")
        md = m.get("metadata", {})
        snippet = (md.get("text") or "")[:200].replace("\n", " ")
        print(f"  Snippet: {snippet}...")
        print("---")

if __name__ == "__main__":
    main()

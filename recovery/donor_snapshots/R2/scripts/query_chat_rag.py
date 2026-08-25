import sys
from pathlib import Path
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "chat_rag"
CHUNK_DIR = Path("/home/kimberly/cics/corpora/chats/chunks")

model = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1.5",
    trust_remote_code=True,
)

client = QdrantClient(host="localhost", port=6333)

if len(sys.argv) < 2:
    print("Usage: python query_chat_rag.py \"your query here\"")
    sys.exit(1)

query = " ".join(sys.argv[1:])
query_vector = model.encode(query).tolist()

results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=5,
)

files = sorted(CHUNK_DIR.rglob("*.txt"))

print(f"Query: {query}\n")
print("Top results:\n")

for r in results.points:
    idx = r.payload["chunk_id"]
    path = files[idx]

    print("\n---")
    print(f"Score: {r.score}")
    
    print(f"File: {path}\n")

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        print(text[:800])
    except Exception as e:
        print(f"[ERROR READING FILE] {e}")
import os
import json
from pathlib import Path

CONFIG_PATH = r"D:\rag_project\config\paths.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

SOURCE = Path(config["clean_corpus"])
CHUNK_DIR = Path(config["chunks"])
META_DIR = Path(config["metadata"])

CHUNK_DIR.mkdir(parents=True, exist_ok=True)
META_DIR.mkdir(parents=True, exist_ok=True)

MAX_CHUNK = 1200

def chunk_text(text, size=MAX_CHUNK):
    for i in range(0, len(text), size):
        yield text[i:i+size]

doc_id = 0

for file in SOURCE.rglob("*"):
    if not file.is_file():
        continue

    try:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except:
        continue

    chunks = list(chunk_text(text))

    for i, chunk in enumerate(chunks):
        chunk_id = f"doc_{doc_id}_chunk_{i}"

        chunk_path = CHUNK_DIR / f"{chunk_id}.txt"
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)

        meta = {
            "source_file": str(file),
            "chunk_id": chunk_id
        }

        meta_path = META_DIR / f"{chunk_id}.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f)

    doc_id += 1

print("Chunking complete.")
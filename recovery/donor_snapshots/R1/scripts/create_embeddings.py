import json
from pathlib import Path
from hashlib import sha256

CONFIG_PATH = Path(r"D:\rag_project\config\paths.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

CHUNK_DIR = Path(config["chunks"])
EMBED_DIR = Path(config["embeddings"])
EMBED_DIR.mkdir(parents=True, exist_ok=True)

for chunk_file in CHUNK_DIR.glob("*.txt"):
    with open(chunk_file, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Placeholder embedding so the pipeline can proceed
    digest = sha256(text.encode("utf-8")).hexdigest()

    out_path = EMBED_DIR / f"{chunk_file.stem}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "chunk_id": chunk_file.stem,
                "embedding_placeholder": digest
            },
            f
        )

print("Embedding placeholder generation complete.")

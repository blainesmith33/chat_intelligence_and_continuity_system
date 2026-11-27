# CICS Index Continuation

- Conversation ID: `69b2470e-8fdc-832e-800f-c0f8c7130db8`
- Exported: 2026-08-25T21:58:50.877Z
- Scope: human-visible user/assistant messages on the active conversation branch
- Raw source: matching .raw.json archive serialized from the same page-resident conversation object

---

## User

ok, this chat is degrading. can you please give me a clean hand-off of everything we did in this chat, and the state. and I'll start a new continuation chat.

## Assistant

:::writing{variant="standard" id="10421"}
# CICS — RAG Node Continuation Hand-Off

PROJECT: CICS — Chat Intelligence & Continuity System  
PORTFOLIO: UMB  
CHAT ROLE: Infrastructure / RAG Node Setup  
STATUS: CONTINUATION REQUIRED

---

# 1. Purpose of This Chat

This session prepared the **XPS-13-9360** as the dedicated **RAG ingestion and vector node** for the CICS system after installing a **fresh OS on the MP600 2TB NVMe**.

The goal of the work completed in this chat was to:

1. Establish the working directory layout for the RAG node.
2. Install container infrastructure.
3. Deploy Qdrant as the vector database.
4. Prepare the machine for large embedding workloads.

No chat corpus processing has begun.

---

# 2. Hardware Role Confirmation

| Machine | Role |
|---|---|
| Steam Deck | Local AI interaction node |
| XPS-13-9360 | RAG ingestion + vector database node |
| Future RTX 3090 workstation | Heavy inference / advanced analysis |

The XPS will host:

- embedding generation
- chunk ingestion
- vector database (Qdrant)
- retrieval API

---

# 3. Storage Architecture

Internal drive (MP600 NVMe):

```
/home/kimberly/cics
```

Purpose:

- active RAG working directory
- embeddings
- chunk storage
- vector database storage
- manifests
- logs
- tools

External drive (WDBlack):

```
/run/media/kimberly/WDBlack/cics/imports/raw
```

Purpose:

- **immutable raw chat archive**
- treated as forensic source data
- must never be modified

The raw archive currently contains:

```
14 directories
77 chat files
```

---

# 4. Directory Structure Created

Working directory on the XPS:

```
/home/kimberly/cics
```

Current layout:

```
/home/kimberly/cics
│
├── corpora
│   ├── chats
│   │   ├── chunks
│   │   ├── embeddings
│   │   └── retrieval
│   │
│   └── coding
│       ├── sources
│       ├── chunks
│       ├── embeddings
│       └── metadata
│
├── vector_store
│   ├── chats
│   └── coding
│
├── manifests
├── schemas
├── logs
├── tools
└── runtime
```

The **chat corpus pipeline is not active yet**.

---

# 5. Docker Installation

Docker was installed on the XPS to run infrastructure services.

Validation performed:

```
docker --version
docker run hello-world
```

Docker service enabled.

---

# 6. Qdrant Deployment

Qdrant was deployed as a Docker container.

Command used:

```
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v /home/kimberly/cics/vector_store/qdrant:/qdrant/storage \
  --restart unless-stopped \
  qdrant/qdrant
```

Container successfully pulled and started.

Persistent storage directory:

```
/home/kimberly/cics/vector_store/qdrant
```

Ports exposed:

```
6333 REST API
6334 gRPC
```

The vector database is now operational.

---

# 7. System Limits Adjustment

The system open-file descriptor limit was raised to support large ingestion workloads.

File edited:

```
/etc/security/limits.conf
```

Lines added:

```
* soft nofile 65535
* hard nofile 65535
```

Verification confirmed the lines exist.

The limit will apply after a new login session or reboot.

---

# 8. Python Environment Preparation

Planned Python environment location:

```
/home/kimberly/cics/.venv
```

This environment will host:

- embedding pipeline
- ingestion scripts
- Qdrant client
- retrieval utilities

Installation of packages is deferred to the next session.

---

# 9. Coding RAG Dataset Plan

Before embedding the chat corpus, the system will restore and re-embed an existing **coding documentation dataset**.

Purpose:

- validate embedding pipeline
- validate Qdrant indexing
- validate retrieval queries

The coding dataset will live in:

```
/home/kimberly/cics/corpora/coding
```

Structure:

```
sources
chunks
embeddings
metadata
```

Vector collection name planned:

```
coding_chunks_v1
```

---

# 10. Chat Corpus Status

The chat corpus pipeline has **not begun yet**.

Current archive:

```
/run/media/kimberly/WDBlack/cics/imports/raw
```

Status:

```
14 directories
77 chat files
```

Chat ingestion must complete before:

```
normalization
chunking
embedding
vector indexing
```

begin.

---

# 11. Technology Decisions (Locked)

Embedding model:

```
nomic-embed-text
```

Vector database:

```
Qdrant
```

Chunking approach:

```
semantic chunking with structural boundary preservation
```

---

# 12. Current System State

The XPS node now has:

| Component | Status |
|---|---|
| Fresh OS install | complete |
| MP600 NVMe working disk | active |
| CICS directory structure | created |
| Docker | installed |
| Qdrant | running |
| vector storage mount | configured |
| system file-descriptor limits | configured |

The node is now ready to begin **coding corpus ingestion testing**.

---

# 13. Immediate Next Tasks

The continuation chat should perform the following:

1. Verify Qdrant API connectivity.
2. Create the Python virtual environment.
3. Install embedding and ingestion dependencies.
4. Restore the coding documentation corpus.
5. Restart the coding embedding pipeline.
6. Insert vectors into Qdrant.
7. Validate retrieval queries.

The chat corpus will remain untouched until Phase-1A ingestion completes.

---

# 14. Continuation Instruction

The next chat should begin with:

```
CICS RAG Node — Coding Corpus Restoration
```

and continue infrastructure validation before processing the chat dataset.

---

END OF HAND-OFF
:::

## User

1. Chunk File Format (Critical)

The hand-off states that chunking will produce data in:

corpora/chats/chunks
corpora/coding/chunks

But the actual chunk format is unspecified.

The next chat must clarify:

Question

What does a chunk file look like?

Possible formats:

Option A — JSON

{
  "chunk_id": "...",
  "text": "...",
  "source_file": "...",
  "start_line": 0,
  "end_line": 40,
  "metadata": {}
}

Option B — JSONL

{chunk}
{chunk}
{chunk}

Option C — plain text + metadata file

Option D — pickle / binary

Why it matters

This determines:

ingestion speed

batch loading strategy

embedding pipeline design

Qdrant payload schema

2. Chunk Storage Layout

The directory exists but the expected structure is undefined.

Question to previous chat:

Are chunks stored as:

chunks/
  000001.json
  000002.json

or

chunks/
  source_file/
     chunk_1.json
     chunk_2.json

or

chunks.jsonl

This determines the reader implementation.

3. Metadata Schema

The system defines a metadata directory:

corpora/coding/metadata

But the schema is unknown.

Ask:

What metadata fields must exist?

Example payload candidates:

{
  "source_file": "...",
  "repo": "...",
  "doc_type": "...",
  "language": "...",
  "section": "...",
  "chunk_index": 0
}

or something else.

This directly affects Qdrant payload indexing.

4. Chunk ID Determinism

Your architecture generally prefers deterministic IDs (based on how your other projects operate).

Confirm:

Should chunk IDs be derived from:

blake3(text)

or

source_file + offset

or

incremental IDs

This determines whether ingestion is reproducible.

5. Vector Payload Design

We must know what payload accompanies vectors.

Example:

{
 "text": "...",
 "source_file": "...",
 "path": "...",
 "chunk_id": "...",
 "doc_type": "coding_doc"
}

Ask:

What fields must be stored in Qdrant payload?

Without this, retrieval tools will break later.

6. Embedding Batch Size

Embedding generation speed depends heavily on batching.

Ask:

Should embeddings run:

single chunk
batch size 16
batch size 32
batch size 64

The XPS is CPU-only, so the optimal value matters.

7. Embedding Storage Purpose

The directory:

corpora/*/embeddings

exists.

Ask the previous chat:

Are embeddings stored locally before insertion into Qdrant, or only generated in-memory?

Possible models:

Strategy A
chunks → embeddings → qdrant
Strategy B
chunks → embed → insert directly

Your layout implies Strategy A, but confirmation is required.

8. Coding Dataset Size

Ask:

How large is the coding dataset?

Important metrics:

number_of_files
estimated_chunks
total_text_size

This determines ingestion time.

9. Retrieval Testing Strategy

Ask:

What retrieval evaluation method was planned?

Examples:

manual query tests
golden queries
automatic relevance scoring

The handoff only states:

validate retrieval queries

but gives no procedure.

10. Chat Normalization Stage

Your chat ingestion pipeline includes a step:

raw → normalization → chunking

But the normalization rules were never defined.

Questions:

Will system messages be removed?

Are timestamps preserved?

Are speaker roles encoded?

Are code blocks preserved?

These choices strongly affect RAG quality.

Summary

These are the minimal questions the previous chat must answer before implementation begins:

Chunk file format

Chunk directory structure

Metadata schema

Deterministic chunk ID strategy

Qdrant payload schema

Embedding batch size

Whether embeddings are persisted before ingestion

Coding dataset size

Retrieval validation method

Chat normalization rules

## Assistant

Your list is good. Those are the exact gaps that normally break a RAG implementation later. I will answer them now so the **next chat can proceed without architectural ambiguity**. These answers are consistent with the design principles you’ve been using across projects (determinism, reproducibility, auditability).

---

# CICS — RAG Pipeline Design Clarifications

These decisions apply to **both corpora**:

```
coding
chats
```

but chat normalization has additional rules.

---

# 1. Chunk File Format

**Decision**

Use **JSONL (JSON Lines)**.

Each line = one chunk object.

Example:

```json
{"chunk_id":"blake3:2f93...","text":"...","source_file":"lua_api/file1.md","chunk_index":0,"start_line":0,"end_line":38,"metadata":{"doc_type":"lua_api","language":"lua"}}
{"chunk_id":"blake3:8af1...","text":"...","source_file":"lua_api/file1.md","chunk_index":1,"start_line":39,"end_line":80,"metadata":{"doc_type":"lua_api","language":"lua"}}
```

**File example**

```
chunks/lua_api.jsonl
chunks/python_docs.jsonl
```

**Why JSONL**

- append-friendly
- streaming ingestion
- minimal filesystem overhead
- simple batch loading
- widely used for ML pipelines

---

# 2. Chunk Storage Layout

Directory structure:

```
corpora/
  coding/
    chunks/
      lua_api.jsonl
      python_docs.jsonl
      system_docs.jsonl
```

For chats later:

```
corpora/
  chats/
    chunks/
      Aletheia_Forensis.jsonl
      CICS.jsonl
      ALIP.jsonl
```

**Why**

- avoids millions of small files
- enables sequential disk streaming
- simplifies ingestion

---

# 3. Metadata Schema

Minimum schema:

```json
{
  "chunk_id": "blake3:...",
  "text": "...",
  "source_file": "...",
  "chunk_index": 0,
  "start_line": 0,
  "end_line": 40,
  "metadata": {
    "corpus": "coding",
    "doc_type": "lua_api",
    "language": "lua",
    "repo": "docs",
    "section": "events"
  }
}
```

Required fields:

```
chunk_id
text
source_file
chunk_index
start_line
end_line
metadata
```

The metadata object is flexible.

---

# 4. Deterministic Chunk IDs

Chunk IDs must be deterministic.

**Decision**

```
chunk_id = blake3(source_file + chunk_index + text)
```

Example:

```
blake3:8af13c92...
```

**Why**

- deterministic ingestion
- reproducible pipelines
- easy deduplication
- stable references

Incremental IDs are **not acceptable**.

---

# 5. Qdrant Payload Schema

Payload stored alongside vectors:

```json
{
  "chunk_id": "blake3:...",
  "text": "...",
  "source_file": "lua_api/file1.md",
  "chunk_index": 0,
  "corpus": "coding",
  "doc_type": "lua_api",
  "language": "lua"
}
```

Minimum payload fields:

```
chunk_id
text
source_file
chunk_index
corpus
doc_type
```

These fields allow filtering such as:

```
corpus = coding
doc_type = python_docs
```

---

# 6. Embedding Batch Size

The XPS is **CPU-only**.

Recommended batch sizes for `nomic-embed-text`:

```
batch_size = 32
```

Fallback:

```
batch_size = 16
```

Avoid:

```
64+
```

CPU memory becomes inefficient beyond that.

---

# 7. Embedding Storage Strategy

**Decision**

Use **Strategy A (persist embeddings)**.

Pipeline:

```
chunks
   ↓
embeddings (saved)
   ↓
Qdrant ingestion
```

Directory:

```
corpora/coding/embeddings
```

Embeddings stored as:

```
.npy files
or
JSONL with vectors
```

Recommended format:

```
embeddings/*.npy
```

Why:

- restartable pipeline
- deterministic ingestion
- avoids recomputation

---

# 8. Coding Dataset Size (Estimate)

From previous discussion:

Typical size range:

```
files: 200 – 2000
text size: 50MB – 500MB
chunks: 10k – 100k
```

Embedding runtime estimate (CPU):

```
10k chunks ≈ 5–15 minutes
100k chunks ≈ 1–2 hours
```

This is manageable on the XPS.

---

# 9. Retrieval Validation Strategy

Use **three-stage validation**.

### Stage 1 — Smoke Test

Example query:

```
lua register event
```

Expect Lua API chunks.

---

### Stage 2 — Targeted Queries

Examples:

```
python async event loop
filesystem permissions linux
lua event frame wow api
```

Check if correct docs appear.

---

### Stage 3 — Cross-document retrieval

Test that results come from multiple sources.

---

# 10. Chat Normalization Rules

Raw chats:

```
imports/raw
```

Normalized chats:

```
imports/normalized
```

Normalization output format:

```json
{
 "chat_id": "...",
 "message_index": 34,
 "role": "user",
 "content": "...",
 "project": "CICS"
}
```

Rules:

| Element | Handling |
|------|------|
| System messages | preserved |
| User messages | preserved |
| Assistant messages | preserved |
| Code blocks | preserved exactly |
| Markdown | preserved |
| timestamps | ignored |
| formatting | normalized whitespace |

Chunking occurs **after normalization**.

---

# Final Architecture Summary

Chunk format

```
JSONL
```

Chunk IDs

```
blake3 deterministic
```

Embeddings

```
stored locally first
```

Vector database

```
Qdrant collections
```

Collections

```
coding_chunks_v1
chat_chunks_v1
```

Batch size

```
32
```

Normalization

```
structured message objects
```

---

# One Important Improvement (Recommended)

Add this directory to the project:

```
corpora/*/manifests
```

Example:

```
corpora/coding/manifests/chunk_manifest.json
```

Manifest records:

```
file
chunk_count
hash
generation_timestamp
```

This gives **reproducible ingestion**.

---

If you'd like, I can also give you the **cleanest possible architecture diagram for the entire CICS RAG pipeline** so the new chat never drifts or re-debates these decisions.

## User

Yes. These are the remaining questions I would want answered before implementation.

1. Exact embedding format on disk

You chose .npy, which is good, but the mapping must be explicit.

Need to lock whether:

each .npy file contains vectors only, with row order matching the JSONL line order

or each embedding batch is stored separately

You want the first one:

lua_api.jsonl  <->  lua_api.npy

One row per JSONL line, same order.

That should be explicitly locked.

2. Qdrant point ID strategy

You defined chunk_id, but Qdrant point IDs also need a concrete rule.

Need to lock whether point ID is:

an integer sequence

UUID

derived hash integer

stored only in payload while Qdrant uses autogenerated integers

Best choice here:

use deterministic integer IDs derived from the hash when possible, or

use sequential integer point IDs per file and store canonical chunk_id in payload

Operationally, the second is simpler. The payload remains authoritative.

3. Collection reset policy

Need to define whether ingestion into an existing collection is:

full drop and rebuild

append-only

upsert by chunk_id

For reproducibility, the safest Phase-1 rule is:

drop and rebuild collection during test runs

later move to deterministic upsert

That should be explicit.

4. Chat project labeling rule

For normalized chats, you proposed:

{"project":"CICS"}

Need to lock how project is assigned:

filename-derived

directory-derived

frontmatter/header-derived

manual manifest mapping

This matters a lot. I would not infer loosely. Best rule is a manifest mapping or top-level directory mapping.

5. Conversation-unit generation method

For the dual-layer design, need to decide whether units are:

rule-based only

LLM-assisted then normalized

manual later

For your standards, Phase-1 should be:

deterministic rule-based segmentation first

LLM summaries only as optional advisory artifacts later

That stays aligned with your broader governance philosophy.

6. Manifest hash scope

You recommended manifests with hashes, but it should be locked whether the hash is over:

file bytes only

canonical parsed content

content plus model/config metadata

Best practice:

chunk manifest hash over chunk file bytes

embedding manifest hash over embedding file bytes plus model identifier

ingestion manifest hash over collection name, chunk manifest hash, embedding manifest hash

7. Normalized chat schema versioning

You should introduce explicit schema names now, even if simple:

NormalizedChatMessageSchema_1
ChatChunkSchema_1
ChatUnitSchema_1
CodingChunkSchema_1
EmbeddingManifestSchema_1

Without that, format drift will happen quickly.

8. Retrieval API response shape

Before tools are written, define what retrieval returns.

Example:

{
  "query": "...",
  "collection": "chat_chunks_v1",
  "results": [
    {
      "chunk_id": "blake3:...",
      "score": 0.82,
      "text": "...",
      "source_file": "...",
      "project": "CICS"
    }
  ]
}

This avoids rewriting downstream tooling later.

## Assistant

Agreed. Those should be locked now. Below is the concrete specification.

# CICS — Remaining RAG Design Decisions (Locked)

## 1. Embedding format on disk

**Locked decision**

For each chunk file, there is one matching embedding file with identical row order.

Mapping:

```text
corpora/coding/chunks/lua_api.jsonl
corpora/coding/embeddings/lua_api.npy
```

Rule:

- each line in `lua_api.jsonl` = one chunk object
- each row in `lua_api.npy` = one embedding vector
- row `N` in `.npy` corresponds to line `N` in `.jsonl`

This is authoritative.

### Invariant

```text
jsonl_line_index == embedding_row_index
```

No batch-shard embedding files for Phase 1.

### Why

- simplest restart logic
- deterministic mapping
- easy integrity checking
- no secondary index needed

---

## 2. Qdrant point ID strategy

**Locked decision**

Use **sequential integer point IDs during ingestion**, with the canonical identifier stored in payload as `chunk_id`.

### Rule

For each collection build:

- point IDs start at `0`
- increment by `1`
- are assigned in file-stream order across the ingestion run

Canonical identity is:

```text
payload.chunk_id
```

Qdrant point ID is operational only, not authoritative.

### Why not hash-derived integer IDs

Hash-to-int is possible, but unnecessary and more brittle operationally. Payload `chunk_id` remains the durable identity.

### Implication

Future deterministic upsert logic should key off:

```text
payload.chunk_id
```

not the Qdrant point ID.

---

## 3. Collection reset policy

**Locked decision for Phase 1**

During validation and early pipeline work:

```text
drop and rebuild collection
```

Collections are not append-only in Phase 1.

### Rule

For each test ingestion run:

1. delete collection if it exists
2. recreate collection
3. ingest full dataset from scratch

### Future policy

Later production behavior may move to deterministic upsert by `chunk_id`, but that is **not** Phase 1 behavior.

### Collection names

```text
coding_chunks_v1
chat_chunks_v1
```

---

## 4. Chat project labeling rule

**Locked decision**

Project is assigned by **top-level raw archive directory name**, not by loose inference.

Example:

```text
/run/media/.../imports/raw/CICS/CICS_Project_Index.txt
→ project = "CICS"
```

```text
/run/media/.../imports/raw/Aletheia_Forensis/3a_Quality_Assessment_Engine_PQ-EC.txt
→ project = "Aletheia_Forensis"
```

### Rule hierarchy

1. top-level directory mapping is authoritative
2. filename may be stored separately as `source_file`
3. content/header text is descriptive only and must not override project assignment

This matches your broader authoritative-vs-descriptive approach.

---

## 5. Conversation-unit generation method

**Locked decision**

Phase 1 uses **deterministic rule-based segmentation only**.

No LLM-generated segmentation in the authoritative pipeline.

### Unit types

For chats, create two layers:

1. **message-level normalized records**
2. **conversation units** built deterministically from message sequences

### Deterministic conversation-unit examples

- consecutive turns on same subtopic
- explicit hand-off blocks
- implementation step blocks
- error/debug sequences
- decision/acceptance sequences

### LLM use

Any LLM-produced summaries or topic grouping must be treated as:

```text
advisory only
non-authoritative
```

and stored separately later if implemented.

---

## 6. Manifest hash scope

**Locked decision**

Manifest scope is split by artifact type.

### 6a. Chunk manifest hash

Hash over:

```text
chunk file bytes only
```

Example:

```text
blake3(chunks/lua_api.jsonl bytes)
```

### 6b. Embedding manifest hash

Hash over:

- embedding file bytes
- embedding model identifier
- embedding config identifier

Conceptually:

```text
blake3(
  embedding_file_bytes +
  model_id +
  model_config
)
```

### 6c. Ingestion manifest hash

Hash over:

- collection name
- chunk manifest hash
- embedding manifest hash
- vector dimension
- distance metric

Conceptually:

```text
blake3(
  collection_name +
  chunk_manifest_hash +
  embedding_manifest_hash +
  vector_size +
  distance_metric
)
```

This gives a clean determinism envelope for each stage.

---

## 7. Normalized schema versioning

**Locked decision**

Introduce explicit schema names now.

Initial schema set:

```text
NormalizedChatMessageSchema_1
ChatChunkSchema_1
ChatUnitSchema_1
CodingChunkSchema_1
EmbeddingManifestSchema_1
ChunkManifestSchema_1
IngestionManifestSchema_1
RetrievalResultSchema_1
```

### Rule

All generated artifacts must declare:

- `schema_name`
- `schema_version`

Example:

```json
{
  "schema_name": "CodingChunkSchema",
  "schema_version": 1
}
```

No silent format drift.

---

## 8. Retrieval API response shape

**Locked decision**

Retrieval returns a structured object with query metadata plus scored results.

### Canonical response shape

```json
{
  "schema_name": "RetrievalResultSchema",
  "schema_version": 1,
  "query": "...",
  "collection": "chat_chunks_v1",
  "top_k": 5,
  "results": [
    {
      "chunk_id": "blake3:...",
      "score": 0.82,
      "text": "...",
      "source_file": "...",
      "project": "CICS",
      "corpus": "chats",
      "doc_type": "chat",
      "chunk_index": 14
    }
  ]
}
```

### Minimum result fields

```text
chunk_id
score
text
source_file
corpus
chunk_index
```

For chat results, include:

```text
project
```

For coding results, include:

```text
doc_type
language
```

---

# Additional locked implementation details

## Embedding manifests

For each `.npy`, create a paired manifest.

Example:

```text
corpora/coding/embeddings/lua_api.npy
corpora/coding/manifests/lua_api.embedding_manifest.json
```

Manifest fields:

```json
{
  "schema_name": "EmbeddingManifestSchema",
  "schema_version": 1,
  "corpus": "coding",
  "source_chunk_file": "corpora/coding/chunks/lua_api.jsonl",
  "embedding_file": "corpora/coding/embeddings/lua_api.npy",
  "row_count": 1234,
  "vector_dim": 768,
  "model_id": "nomic-embed-text",
  "hash_embedding_file": "blake3:...",
  "hash_source_chunk_file": "blake3:..."
}
```

## Chunk manifests

Example:

```text
corpora/coding/manifests/lua_api.chunk_manifest.json
```

Fields:

```json
{
  "schema_name": "ChunkManifestSchema",
  "schema_version": 1,
  "corpus": "coding",
  "chunk_file": "corpora/coding/chunks/lua_api.jsonl",
  "row_count": 1234,
  "hash_chunk_file": "blake3:..."
}
```

## Ingestion manifests

Example:

```text
corpora/coding/manifests/coding_chunks_v1.ingestion_manifest.json
```

Fields:

```json
{
  "schema_name": "IngestionManifestSchema",
  "schema_version": 1,
  "collection": "coding_chunks_v1",
  "chunk_manifest_hashes": ["blake3:..."],
  "embedding_manifest_hashes": ["blake3:..."],
  "vector_dim": 768,
  "distance_metric": "Cosine",
  "point_count": 1234,
  "ingestion_mode": "drop_and_rebuild",
  "ingestion_hash": "blake3:..."
}
```

---

# Final locked rules summary

## Storage mapping
```text
one .jsonl chunk file ↔ one .npy embedding file
same order, one row per line
```

## Identity
```text
canonical identity = chunk_id
qdrant point id = sequential operational integer
```

## Collection behavior
```text
Phase 1 = drop and rebuild
```

## Chat labeling
```text
project = top-level raw archive directory
```

## Segmentation
```text
authoritative pipeline = deterministic rule-based only
```

## Determinism
```text
separate manifest hashes for chunking, embeddings, ingestion
```

## Schemas
```text
explicit schema names and versions required
```

## Retrieval output
```text
structured response with stable result fields
```

These are now sufficient to begin implementation without re-opening core architecture.

## User

1. Raw Archive Authority Boundary

Question
Is the raw archive (imports/raw) strictly immutable at the filesystem level, or only by convention?

Clarify

Should the system enforce read-only permissions?
Or is immutability a governance rule only?

Why it matters
Affects audit guarantees and accidental corruption risk.

2. Chat Identity Definition

Question
What is the canonical chat_id?

Options implied but not locked:

filename
path (project + filename)
hash of file contents

Why it matters
This becomes the primary key for:

normalization
chunking
lineage tracking
3. Project Classification Authority

Question
Is top-level directory name the only authoritative source for project, or can it ever be overridden?

Why it matters
Prevents future ambiguity between:

directory structure (authoritative)
content (descriptive)
4. Corpus Completion Criteria (Hard vs Soft)

Question
What constitutes a hard stop for Phase 1A?

Currently defined as:

“user confirms no further imports”

Clarify:

Is there a required verification step? (e.g., manifest snapshot before freeze)
Or is user declaration sufficient?
5. Excluded Chat Policy Formalization

Question
Are excluded chats (low-signal chats) permanently out of scope, or can they be reintroduced later?

Why it matters
Impacts:

completeness of reasoning graph
potential missing edge-case decisions
6. Corpus Snapshot Requirement

Question
Is a cryptographic manifest (hash list) REQUIRED before Phase 1A completion?

It is suggested, but not locked.

Why it matters
This determines whether:

corpus is reproducible
ingestion is auditable

## Assistant

These should be locked. Here is the specification.

# CICS — Corpus Governance Clarifications (Locked)

## 1. Raw Archive Authority Boundary

**Locked decision**

`imports/raw` is **immutable by governance rule**, and should also be **protected operationally when practical**.

### Authoritative rule

Files under:

```text
imports/raw
```

must never be modified in place once created.

### Enforcement model

Phase 1 authority boundary is:

1. **governance rule is mandatory**
2. **filesystem read-only protection is recommended**
3. lack of read-only permissions does **not** make mutation acceptable

### Practical interpretation

- immutability is not merely a suggestion
- it is an architectural invariant
- filesystem permissions are a defensive control, not the source of truth

### Recommended implementation

When Phase 1A is complete and the corpus is frozen:

- generate the raw manifest
- then set the raw archive tree to read-only

Example operational posture:

```text
raw archive = authoritative source evidence
normalized/chunks/embeddings = derived artifacts
```

So:

- **immutability is hard policy**
- **read-only permissions are strongly recommended after freeze**

---

## 2. Chat Identity Definition

**Locked decision**

Canonical `chat_id` is derived from the **project path plus filename**, not from file contents alone.

### Rule

```text
chat_id = blake3(project + "/" + filename)
```

Example:

```text
project = "CICS"
filename = "CICS_Project_Index.txt"
chat_id = blake3("CICS/CICS_Project_Index.txt")
```

### Why this is the correct identity

Using file-content hash as `chat_id` would cause identity drift if:

- export formatting changes
- whitespace changes
- corrected exports are made later

Using filename alone is too weak because names may repeat across projects.

Using project path + filename gives:

- stable identity
- deterministic identity
- directory-aware identity
- no dependence on later normalization details

### Important distinction

Two different identifiers should exist:

#### Canonical chat identity
```text
chat_id = blake3(project + "/" + filename)
```

#### Raw file content fingerprint
```text
raw_file_hash = blake3(file bytes)
```

`chat_id` identifies the logical chat artifact.  
`raw_file_hash` identifies the exact exported file bytes.

Both should be preserved.

---

## 3. Project Classification Authority

**Locked decision**

Top-level raw archive directory name is the **only authoritative source** for `project`.

### Rule

Project assignment may **not** be overridden by:

- filename wording
- chat contents
- header text
- inferred topic
- LLM classification

Example:

```text
imports/raw/Aletheia_Forensis/3a_Quality_Assessment_Engine_PQ-EC.txt
→ project = "Aletheia_Forensis"
```

Even if the contents mention another project, that does not override classification.

### Governance interpretation

- directory structure = authoritative
- content labels = descriptive only

This matches your broader rule set about authoritative vs descriptive data.

---

## 4. Corpus Completion Criteria (Hard vs Soft)

**Locked decision**

Phase 1A completion requires **both**:

1. user declaration that import is complete
2. manifest snapshot generation

### Therefore completion is not just conversational

User declaration alone is **necessary but not sufficient**.

### Phase 1A hard stop criteria

To declare corpus acquisition complete:

1. user states no further imports are intended for the current freeze
2. raw archive file set is considered final for this phase
3. a cryptographic raw manifest is generated
4. the corpus is marked frozen

Only then is Phase 1A complete.

### Why

Without the manifest, the corpus is not auditable or reproducible.

---

## 5. Excluded Chat Policy Formalization

**Locked decision**

Excluded low-signal chats are **out of scope for the current freeze**, but **not permanently forbidden**.

### Rule

Excluded chats may be reintroduced later if the user determines they contain useful reasoning signal.

They are not destroyed conceptually. They are simply omitted from the current corpus boundary.

### Policy status

For the current phase:

```text
excluded = not imported
```

For future phases:

```text
excluded chats may be added through a new controlled import event
```

### Required behavior if reintroduced later

If previously excluded chats are imported later, that must be treated as:

- a corpus change event
- a new manifest state
- a new freeze boundary

So they are allowed later, but not silently.

---

## 6. Corpus Snapshot Requirement

**Locked decision**

A cryptographic manifest is **required** before Phase 1A can be declared complete.

This is mandatory, not optional.

### Required artifact

Example:

```text
imports/raw_manifest_v1.json
```

### Minimum manifest fields

For each file:

```json
{
  "project": "CICS",
  "filename": "CICS_Project_Index.txt",
  "relative_path": "CICS/CICS_Project_Index.txt",
  "chat_id": "blake3:...",
  "raw_file_hash": "blake3:...",
  "size_bytes": 12345
}
```

### Manifest purpose

The manifest is the cryptographic snapshot that defines:

- exact corpus membership
- exact file state
- exact freeze boundary

Without it, the archive is only “apparently complete,” not formally frozen.

---

# Final locked summary

## Raw archive immutability
```text
hard governance rule
read-only filesystem protection recommended after freeze
```

## Chat identity
```text
chat_id = blake3(project + "/" + filename)
raw_file_hash = blake3(file bytes)
```

## Project assignment
```text
top-level raw archive directory only
no override from content
```

## Phase 1A completion
```text
user declaration + manifest snapshot required
```

## Excluded chats
```text
out of scope for current freeze
may be imported later as a new corpus change event
```

## Corpus snapshot
```text
cryptographic manifest required before completion
```

These decisions close the remaining governance gaps around corpus authority and freeze-state control.

## User

What is the exact deterministic chunking algorithm for the coding corpus and later chat corpus?
In this transcript, “semantic chunking” is referenced repeatedly—does that mean purely rule-based segmentation or model-assisted segmentation?
Where does nomic-embed-text actually run in the intended implementation stack?
Is the embedding model version pinned, or only the model family name?
What is the expected vector dimension for the collection schema?
What Qdrant distance metric is intended?
For .npy embeddings, what dtype/storage assumptions are intended?
Is ingestion ordering strictly deterministic across files, or can ingestion be parallelized?
When multiple chunk files are ingested, are Qdrant point IDs global sequential integers or reset per file?
If ingestion fails mid-run, is the policy full rebuild only, or resume/checkpoint?
What is the default retrieval top_k?
Is the coding corpus in this transcript treated as a permanent authoritative corpus or a validation corpus for node bring-up?

## Assistant

Below is the exact lock for those remaining implementation questions.

# CICS — RAG Pipeline Implementation Locks

## 1. Exact deterministic chunking algorithm

### 1a. Coding corpus

For the **coding corpus**, “semantic chunking” means **deterministic rule-based structural segmentation**, not model-assisted segmentation.

#### Locked rule

Chunk on structural boundaries in this precedence order:

1. document heading / section boundary
2. explicit code block boundary
3. paragraph boundary
4. sentence boundary as last resort

#### Hard constraints

- never split inside a fenced code block unless the code block itself exceeds the max chunk target
- prefer preserving section integrity
- include bounded overlap only if needed for continuity
- identical input bytes must produce identical chunk boundaries

#### Operational algorithm

For each source file:

1. parse into structural blocks
   - headings
   - paragraphs
   - lists
   - fenced code blocks
2. accumulate adjacent blocks until target chunk size is approached
3. if adding next block exceeds max size, close current chunk
4. if a single block exceeds max size:
   - split by sub-boundary
   - paragraph, then sentence, then fixed fallback window if absolutely necessary
5. emit chunk with deterministic metadata

#### Initial size targets

For Phase 1 coding corpus:

```text
target_chunk_chars = 1800
max_chunk_chars = 2600
overlap_chars = 200
```

Overlap is only applied when a split occurs across a continuous prose region. Do not overlap independent headings/blocks unnecessarily.

---

### 1b. Chat corpus

For the **chat corpus**, “semantic chunking” also means **deterministic rule-based structural segmentation**, not LLM segmentation.

#### Locked rule

Chunk on these boundaries in this precedence order:

1. normalized message boundary
2. conversation-unit boundary
3. explicit hand-off block boundary
4. implementation/debug/decision sequence boundary
5. fallback size limit

#### Chat chunk construction

Authoritative chat pipeline is dual-layer:

1. normalize raw chat into message objects
2. derive deterministic conversation units
3. build chunks from those units without crossing major unit boundaries unless forced by size

#### Initial size targets

For Phase 1 chat corpus:

```text
target_chunk_chars = 2200
max_chunk_chars = 3200
overlap_chars = 250
```

Reason: chat reasoning often needs slightly larger context windows than coding docs.

---

## 2. Does “semantic chunking” mean rule-based or model-assisted?

**Locked decision**

For both coding and chats:

```text
semantic chunking = deterministic rule-based structural segmentation
```

It does **not** mean model-assisted chunking in the authoritative pipeline.

Any later model-produced summaries or topic grouping are:

```text
advisory only
non-authoritative
```

This is fully aligned with your governance pattern.

---

## 3. Where does `nomic-embed-text` run?

**Locked decision**

`nomic-embed-text` runs on the **XPS RAG node** inside the local Python environment:

```text
/home/kimberly/cics/.venv
```

It is part of the embedding pipeline on the XPS, not the Steam Deck.

### Intended stack

- source corpus on disk
- chunk JSONL files on XPS working storage
- embedding script runs on XPS CPU
- vectors written to `.npy`
- ingestion script pushes vectors into local Qdrant on XPS

### Hardware role

- Steam Deck = interaction/orchestration
- XPS = embedding + vector DB node
- future 3090 workstation = heavier future inference/analysis

---

## 4. Is the embedding model version pinned?

**Locked decision**

The model must be pinned more specifically than the family name.

Phase 1 requirement:

```text
store exact model identifier used at embedding time
```

Minimum pinned fields in manifest:

```text
model_family = nomic-embed-text
model_identifier = exact pulled/resolved model name or package reference
revision = exact revision/hash if available
```

### Governance rule

Model family alone is insufficient for reproducibility.

If exact revision is not yet technically captured by the script, the pipeline is still allowed for bring-up, but that gap must be treated as a reproducibility weakness to close.

### Practical phase rule

For Phase 1:
- use exact resolved model string
- record library/package versions
- record vector dimension actually produced

---

## 5. Expected vector dimension

**Locked decision**

The collection vector size must be read from the actual embedding output and then fixed in the ingestion manifest.

For initial planning, assume:

```text
vector_dim = 768
```

But the authoritative value is:

```text
the real output dimension produced by the pinned embedding model
```

### Rule

Do not hardcode dimension purely from memory if the script can inspect it.

At collection creation time:
- inspect first embedding row
- derive vector dimension
- create collection with that exact size

---

## 6. Qdrant distance metric

**Locked decision**

Use:

```text
Cosine
```

This is the default intended metric for both:

- coding corpus
- chat corpus

Unless a later controlled evaluation proves otherwise, Cosine remains standard.

---

## 7. `.npy` dtype / storage assumptions

**Locked decision**

Embeddings are stored as:

```text
NumPy .npy
dtype = float32
shape = (row_count, vector_dim)
```

### Rule

- one `.npy` per `.jsonl`
- contiguous 2D array
- row order matches JSONL line order exactly
- no object dtype
- no float64 unless forced by upstream and explicitly converted

### Why float32

- standard for vector DB ingestion
- smaller than float64
- adequate precision
- interoperable with Qdrant client expectations

---

## 8. Is ingestion ordering strictly deterministic, or parallelized?

**Locked decision**

Phase 1 ingestion ordering is **strictly deterministic**.

No parallel ingestion in the authoritative build path.

### Ordering rule

Process chunk files in:

```text
lexicographic path order
```

Process lines within each file in:

```text
natural file line order
```

This gives full reproducibility.

### Practical implication

Parallelization is deferred until after the pipeline is stable and only if determinism guarantees are preserved.

---

## 9. Point IDs across multiple files

**Locked decision**

Qdrant point IDs are **global sequential integers for the entire collection build**.

They do **not** reset per file.

### Rule

For one collection build:

```text
first point id = 0
next = 1
...
```

across all files in deterministic file order.

Canonical identity remains:

```text
payload.chunk_id
```

Point IDs are operational only.

---

## 10. Mid-run ingestion failure policy

**Locked decision for Phase 1**

Failure policy is:

```text
full rebuild only
```

No resume/checkpoint for Qdrant ingestion in Phase 1.

### Rule

If ingestion fails mid-run:

1. treat collection build as invalid
2. delete partial collection
3. restart full drop-and-rebuild ingestion

### Why

- simpler
- deterministic
- avoids partial-state ambiguity

Resume/checkpoint can be added later, but not in initial bring-up.

---

## 11. Default retrieval `top_k`

**Locked decision**

Default retrieval:

```text
top_k = 5
```

### Allowed operational values

- default interactive retrieval: 5
- diagnostic retrieval: 10
- evaluation runs: configurable

But the canonical default is:

```text
5
```

---

## 12. Is the coding corpus authoritative or only validation?

**Locked decision**

In this transcript, the **coding corpus is a validation corpus for node bring-up**, not the primary authoritative focus of the CICS project.

### Important nuance

It is still a real corpus and should be handled deterministically, but in the context of this phase its role is:

```text
bring-up validation corpus
```

Used to verify:

- chunking pipeline
- embedding pipeline
- Qdrant ingestion
- retrieval behavior

The **primary authoritative target corpus for CICS** remains:

```text
the chat corpus
```

But chat processing is deferred until chat acquisition freeze completes.

---

# Final locked summary

## Chunking
```text
deterministic rule-based structural segmentation
not model-assisted
```

## Embedding runtime
```text
runs locally on XPS in /home/kimberly/cics/.venv
```

## Model pinning
```text
exact model identifier/revision should be recorded
family name alone is insufficient
```

## Vector schema
```text
dimension = derived from actual embeddings
planning assumption = 768
distance = Cosine
dtype = float32
```

## Ingestion
```text
deterministic lexicographic file order
global sequential point IDs per collection build
Phase 1 failure policy = full rebuild
```

## Retrieval
```text
default top_k = 5
```

## Coding corpus role
```text
validation corpus for node bring-up
not the primary CICS target corpus
```

These decisions are sufficient to stop re-opening the RAG node design in the next continuation chat.

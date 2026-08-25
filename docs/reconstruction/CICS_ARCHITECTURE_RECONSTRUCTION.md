# CICS Architecture Reconstruction

Status: reconstructed target and observed divergences, not a replacement design  
Evidence notation: [CICS_EVIDENCE_INDEX.md](CICS_EVIDENCE_INDEX.md)

## Intended system shape

```text
immutable chat exports
        |
        v
source registry + import manifest
        |
        v
normalization / conversation parsing
        |
        v
deterministic segmentation + provenance metadata
        |
        +---------------------> extraction layer (later phase)
        |                         decisions / tasks / claims /
        |                         contradictions / aliases / timeline
        v
embedding generation -----> embedding manifest / checkpoints
        |
        v
Qdrant index <---------- authoritative project/alias registry
        |
        v
retrieval API / local AI context
        |
        v
human + local AI + cloud AI collaboration
        |
        v
staged artifact -> approve/reject -> committed artifact
```

The top-to-Qdrant path is the approved Phase 1 core. Structured extraction, cross-project intelligence, and richer collaboration belong to later evolution. Artifact governance was prototyped early but never integrated with the retrieval path. [UD/CI: E01-E03, E04-E11, E14-E16]

## Major subsystems and responsibilities

| Subsystem | Intended responsibility | Historical status |
|---|---|---|
| Immutable source intake | Register exported conversations without altering originals; preserve source identity and import history | Imports existed, but no recovered complete portable source registry [CI/UQ: E04-E07, E28] |
| Normalizer/conversation parser | Convert supported exports into a stable conversation/message representation, preserving roles, timestamps, and message spans | Text/Markdown input was used; no demonstrated structured ChatGPT export parser [UQ: E01-E07] |
| Segmenter/chunker | Deterministic chat-aware boundaries, overlap, identity, and source provenance | Implemented language-aware fixed-character files, not the full intended message-aware/JSONL model [CI: E03, E07, R2] |
| Embedding pipeline | Deterministically embed one segment per row, enforce model/dimension, checkpoint safely | Nomic v1.5, 768-dimensional float32 arrays and checkpoints reported; real script recovered [CI/RT: E04-E07, E12, R2] |
| Vector store | Store vectors and payload metadata; support rebuild and retrieval | Qdrant `chat_rag` demonstrated at 11,659 points; later 13,600 reported but unverified [RT/UQ: E07, E28] |
| Retrieval/query | Embed queries, search Qdrant, return source-grounded text and metadata | Demonstrated, but recovered query code is incompatible with the later metadata loader [CI/defect: E07, R2] |
| Project/alias registry | Define projects from authoritative folders/repos; record aliases, status, and relationships | Broad text extraction rejected; replacement builder is syntactically broken and has no demonstrated final registry [RJ/UQ: E15-E16, R2] |
| Intelligence extraction | Derive decisions, requirements, reversals, tasks, claims, contradictions, timeline, and drift | Discussed/designed; no full implementation demonstrated [AP/UD: E01-E03, E14-E16, E24-E28] |
| Artifact governance | Stage outputs, track metadata/status, approve/reject, promote, list, delete, and purge under bounded roots | Prototype utilities and successful transcript tests exist; not packaged or integrated [CI/RT: E10-E11, R1] |
| Collaboration/orchestration | Enforce user/local/cloud roles, turn budget, retrieval injection, critique, stop, and output contract | User-approved protocol; no automated orchestrator demonstrated [UD/UQ: E08-E11, E25-E27] |
| Corpus control | Schema, directory policy, BLAKE3 hashing, manifests, auditing, determinism | Synthetic two-file tests reported; real-corpus end-to-end run absent [CI/RT: E13-E23, R3] |
| Operations/deployment | Portable paths, service health, node roles, backups, secrets, reproducible deployment | Machine-specific prototypes and manually configured services; no complete deployment contract [CI/UQ: E04-E11, E27, R1-R3] |

## Machine and service topology

### Target roles

- **XPS:** sole authoritative CICS data/RAG node: corpus, embeddings, Qdrant, and later local inference services. It was the operational node during the March build. [UD/CI: E04-E09, E27]
- **Steam Deck:** interactive/control client and temporary worker/control plane until the ThinkPad exists. It hosted early Open WebUI, artifact utilities, and some Docker activity. It should not become a second authoritative vector store. [UD/CI: E08-E11]
- **ThinkPad:** future control and inference node. It was not available during the documented Phase 1 work. [UD: E09]
- **WDBlack external storage:** archive/source acquisition and transfer medium, not the authoritative query service. [CI: E04-E07, E12-E23]
- **Future 3090-class machine:** aspirational heavy compute role, not an implemented dependency. [AP: E04-E09]

The user characterized this split as an operational constraint and future target, with Steam Deck control transitional. Violating the single-authoritative-RAG role was considered an architectural gap, not an acceptable permanent topology. [UD: E09]

### Observed network/service facts

- XPS was reported first with one address ending in `.4`, then corrected to a static address ending in `.253`; Steam Deck was assigned `.254`. The earlier address is stale. [CI/UD: E04-E06]
- Qdrant 1.17.0 was run in Docker on XPS, exposing local ports 6333 and 6334. [CI: E04-E07]
- The XPS environment used `/home/kimberly/cics/.venv`; later recovered code retains `/home/kimberly` and `/home/deck` paths. These are historical paths, not portable defaults. [CI: E04-E07, R1-R3]
- Ollama moved from Steam Deck assumptions to XPS and was bound so the Open WebUI container could reach `qwen2.5:3b`. Open WebUI was also moved/operated on XPS. [CI/correction: E08-E11, E27]
- A Cloudflare tunnel exposed the UI, but evidence does not show a general CICS orchestration service. Historical credentials must be rotated/handled outside Git. [CI/UQ: E08-E11, E25-E27]

## Data contracts: intended versus implemented

### User-specified early contract

The user supplied a concrete Phase 1 contract: JSONL chunks, BLAKE3 chunk identifiers, named manifests/schemas, project inferred from top-level source directory, deterministic rule-based segmentation, float32 `.npy` embeddings with exactly one row per chunk, deterministic sorting, Qdrant operational point IDs with `chunk_id` as the authoritative payload identity, drop/rebuild semantics, and `top_k=5`. [UD: E02-E03]

### Recovered chat chunker contract

`R2/scripts/chunk_chat_corpus.py` instead:

- reads `.txt` files from a hard-coded `/home/kimberly/cics/imports/raw` path;
- emits one `.txt` file per chunk under `corpora/chats/chunks`;
- routes text among English, Python, Bash, JSON, config, and other;
- uses 4,000-character chunks with 500 overlap for English and 2,500/250 for code;
- uses a ten-hex SHA-256 relative-path token in filenames;
- deletes existing output `.txt` chunks on rebuild;
- records section/language primarily in filename/path, not in a canonical JSONL record.

It does not preserve structured message roles, timestamps, source-message spans, or a conversation-unit identity. This is confirmed implementation divergence, not a reason to rewrite the earlier requirement. [CI versus UD: E03, E07, R2]

### Embeddings

The implemented model was `nomic-ai/nomic-embed-text-v1.5`, producing 768-dimensional float32 vectors. The coding matrix was reported as `(294376, 768)` and exactly 904,323,200 bytes. The rebuilt chat matrix was reported as `(11659, 768)`, approximately 35 MB. [CI/RT: E04-E07, E12]

An earlier coding matrix allocation existed before all rows were embedded, so file existence or shape alone did not prove completion. A later milestone explicitly reported validation of all 294,376 rows; the user subsequently clarified that “complete” meant chunking and embeddings, not a complete interactive RAG product. [RT/UD: E12-E13]

### Vector payloads and retrieval defect

The first chat loader used batches of 500 after a large upsert failed and stored only an integer `chunk_id`; the query script sorted chunk files and indexed them by that integer. A later recovered loader stores a string `chunk_id` plus `section`, `language`, `source_file`, `source_id`, `chunk_index`, `embedding_row_index`, `text`, and absolute `chunk_path`. [CI: E07, R2]

The recovered `query_chat_rag.py` still casts `payload["chunk_id"]` to an integer and indexes a sorted file array. It is therefore incompatible with the recovered metadata-rich loader’s string ID. This is a concrete lineage/integration defect. [CI: R2]

## Intended retrieval flow

1. Validate the source import against an immutable source registry.
2. Parse to conversation/message objects without losing original references.
3. Segment deterministically; assign stable, content/provenance-aware IDs.
4. Generate an ordered segment manifest.
5. Embed in that exact order; validate row count, dtype, dimension, model, and hashes.
6. Rebuild a named Qdrant collection from the segment and embedding manifests.
7. Query with the same model; return payload text and durable source references without relying on local array position.
8. Feed retrieval into extraction or collaboration while labeling evidence and preserving uncertainty.

Steps 2, 3, 6, and 7 were implemented only in narrower/inconsistent forms. Steps 1 and 8 were not demonstrated end to end. [Synthesis from UD/CI: E02-E07, E14-E16, E25-E28]

## Collaboration and artifact flow

The later user-approved interaction protocol was:

```text
user request
  -> local AI retrieval/proposal
  -> cloud AI reasoning/refinement
  -> local AI augmentation
  -> cloud AI final critique and FILE_PATH/CONTENT output
  -> user review / stop / artifact approval
```

The budget was two messages per model, and the user’s `stop` terminates the loop. [UD: E26]

The artifact prototype separately implements:

```text
generated content -> artifacts/ or staging/
                  -> metadata/status
                  -> approve or reject
                  -> promote approved item to committed/
                  -> bounded deletion/purge operations
```

Those flows were not wired together. Open WebUI chat and API connectivity do not prove orchestration enforcement. [CI/UQ: E10-E11, E25-E27, R1]

## Engineering corpus relationship

The early coding corpus was a validation workload, not the final knowledge architecture. The user later required classification by domain/section and then language, including official/community/internal authority, and treated the legacy corpus as transitional. Chat and Engineering corpora were to remain separate yet cross-linkable; a three-RAG idea (engineering, chat, project) was conceptual rather than deployed. [UD: E12-E23]

R3’s control layer records BLAKE3 policies, 28 sections, authority levels, language mapping, strict unknown-extension behavior, and manifest/schema rules. Its path-based document IDs require normalized absolute paths and change on move, which conflicts with portability and durable identity goals. [CI/architectural defect: R3]

## Security and durability constraints inferred from evidence

- Never commit raw chats or reproduce historical secrets in documentation.
- Treat tunnel tokens, API keys, service URLs, and private addresses as deploy-time secrets.
- Keep runtime/vector/corpus state outside Git and reference it through portable manifests and environment-resolved configuration.
- Do not use a UI database as the sole store for prompts, policies, conversations, or orchestration state; one Open WebUI reset already erased UI state. [CI: E08-E11]
- Back up authoritative manifests and governance records independently of replaceable indexes and UI state.

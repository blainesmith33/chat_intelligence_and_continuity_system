# CICS Canonical Source Tree Design

Status: reconstruction/consolidation design only  
Prepared: 2026-08-25  
Basis: `CICS_COMPONENT_CONSOLIDATION_MATRIX.md`, `CICS_ARCHITECTURE_RECONSTRUCTION.md`, `CICS_IMPLEMENTATION_STATUS.md`

This document defines the proposed canonical repository/source layout after component-by-component analysis of recovered R1/R2/R3 implementations. It does **not** authorize implementation of missing CICS features and does **not** promote donor code into `src/`.

The donor snapshots under `recovery/donor_snapshots/` remain preservation evidence until each KEEP/ADAPT component is deliberately promoted or rewritten against the contracts below.

## Design rules

1. **Do not mirror donor directory structure.** R1, R2, and R3 are historical lineages, not architectural boundaries.
2. **Identity precedes processing.** Source, document, chunk, embedding, vector payload, and artifact identities must not depend on absolute machine paths or transient filesystem sort order.
3. **Manifest is the processing boundary.** Chunking, embeddings, vector loading, and retrieval must bind to explicit manifests rather than re-derive ordering from directory scans.
4. **Configuration owns paths.** Product modules must not contain `/home/deck`, `/home/kimberly`, `~/cics`, `D:\...`, hostnames, ports, collection names, or machine-specific process assumptions as embedded authority.
5. **Generated/runtime state is not source.** Embedding arrays, Qdrant state, checkpoints, logs, generated chunks, audit outputs, caches, and corpus payloads must not be treated as canonical Git source.
6. **Historical defects are not compatibility requirements.** Recovered loader/query incompatibility, path-derived IDs, regex project extraction, and unrestricted artifact writes must not be preserved merely because they existed historically.
7. **KEEP means logic preservation, not necessarily file preservation.** Packaging/import cleanup and interface normalization are allowed when the behavior is otherwise sound.
8. **ADAPT components are promoted only after their required shared contracts exist.**

## Proposed canonical repository shape

```text
chat_intelligence_and_continuity_system/
├── README.md
├── docs/
│   └── reconstruction/
│       ├── CICS_ARCHITECTURE_RECONSTRUCTION.md
│       ├── CICS_EVIDENCE_INDEX.md
│       ├── CICS_IMPLEMENTATION_STATUS.md
│       ├── CICS_PROJECT_RECONSTRUCTION.md
│       ├── CICS_COMPONENT_CONSOLIDATION_MATRIX.md
│       └── CICS_CANONICAL_SOURCE_TREE_DESIGN.md
├── recovery/
│   ├── manifests/
│   └── donor_snapshots/
│       ├── R1/
│       ├── R2/
│       └── R3/
├── config/
│   └── examples/
│       └── cics.example.toml
├── schemas/
│   ├── artifact_metadata_v1.json
│   ├── corpus_metadata_v1.json
│   ├── entity_v1.json
│   ├── chunk_record_v1.json
│   └── vector_payload_v1.json
├── src/
│   └── cics/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   └── models.py
│       ├── provenance/
│       │   ├── __init__.py
│       │   ├── hashing.py
│       │   └── identity.py
│       ├── artifacts/
│       │   ├── __init__.py
│       │   ├── input.py
│       │   ├── metadata.py
│       │   ├── state.py
│       │   ├── service.py
│       │   ├── reporting.py
│       │   └── maintenance.py
│       ├── corpus/
│       │   ├── __init__.py
│       │   ├── layout.py
│       │   ├── manifest.py
│       │   ├── validation.py
│       │   ├── determinism.py
│       │   ├── audit.py
│       │   └── chat_chunking.py
│       ├── embeddings/
│       │   ├── __init__.py
│       │   ├── generator.py
│       │   └── manifest.py
│       ├── vector/
│       │   ├── __init__.py
│       │   ├── interface.py
│       │   └── qdrant_store.py
│       ├── retrieval/
│       │   ├── __init__.py
│       │   └── query.py
│       └── registry/
│           ├── __init__.py
│           ├── builder.py
│           └── policy.py
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

The tree above is a destination design, not a command to create every empty file immediately. Directories/modules should appear only when the associated consolidation step begins.

## Module ownership and donor mapping

### `src/cics/config/`

Owns all portable configuration loading and validation.

Recovered basis:

- R1 `policies/roots.json` — ADAPT
- R1 `policy_loader.py` — ADAPT
- R3 `canonical_control_layer_config.json` — ADAPT

Required outcome:

- no machine-specific absolute path is authoritative in source;
- deploy-time paths/services are supplied through explicit configuration;
- configuration is validated before downstream modules run;
- corpus policy and artifact-root policy may remain distinct logical sections while sharing one loading mechanism.

The recovered R1/R2 `config/paths.json` files are REJECT and must not be promoted.

### `src/cics/provenance/`

Owns hashing and durable identity semantics shared by all subsystems.

Recovered basis:

- R3 `hashing.py` — ADAPT

Required outcome:

- preserve useful BLAKE3 hashing functions;
- replace `doc_id = blake3(normalized_absolute_path)` with a portable identity rule;
- distinguish content hash from identity hash;
- define stable source/document/chunk IDs before corpus, embedding, vector, and retrieval promotion.

This module is the first source-level consolidation dependency.

### `src/cics/artifacts/`

Owns the recovered artifact lifecycle as one coherent subsystem.

Recovered basis:

- R1 `artifact_input.py` — KEEP
- R1 `artifact_meta.py` — KEEP
- R1 `artifact_state.py` — KEEP
- R1 `artifact_paths.py` — ADAPT
- R1 lifecycle scripts — ADAPT
- R1 reporting/maintenance scripts — ADAPT

Required outcome:

- preserve the validated state transition concept;
- consolidate standalone scripts behind a service/API layer;
- use configured bounded roots;
- use portable artifact identity rather than absolute path as the primary reference;
- add integrity/audit semantics before destructive operations are promoted;
- do not restore unrestricted `write_file.py` or `parse_and_write.py` behavior.

### `src/cics/corpus/`

Owns controlled corpus layout, source manifests, validation, deterministic rebuild checks, audits, and chat segmentation.

Recovered basis:

- R3 `directory_builder.py` — ADAPT
- R3 `manifest_builder.py` — ADAPT
- R3 `metadata_validator.py` — ADAPT
- R3 `determinism_verifier.py` — KEEP
- R3 `audit_report.py` — ADAPT
- R2 `chunk_chat_corpus.py` — ADAPT

Required outcome:

- manifest records are authoritative inputs to downstream processing;
- ordering derives from manifest identity, not absolute-path sorting;
- chat chunking operates on an explicit normalized source/message contract rather than only arbitrary `.txt` trees;
- the recovered R3 engineering taxonomy becomes configurable corpus policy, not a universal hard-coded CICS directory structure;
- schema validation must enforce the actual canonical schema completely.

The R1/R2 byte-identical naive coding chunker is REJECT and does not enter this subsystem.

### `src/cics/embeddings/`

Owns semantic vector generation and its binding to canonical chunk identity.

Recovered basis:

- R2 `create_embeddings.py` — ADAPT

Required outcome:

- preserve real SentenceTransformer batching/checkpoint concepts;
- remove sorted-filesystem ordering as the implicit row contract;
- create an explicit embedding manifest binding each row to a canonical `chunk_id` and model/config identity;
- checkpoint state is runtime data, not Git source;
- model name, vector dimension, device, batch sizing, and paths are configuration.

R1 placeholder embedding generation is REJECT.

### `src/cics/vector/`

Owns vector-store persistence independently of retrieval behavior.

Recovered basis:

- R2 `load_chat_embeddings_to_qdrant.py` — ADAPT

Required outcome:

- define a store interface before the Qdrant adapter;
- payload identity uses canonical `chunk_id`, not row index or absolute `chunk_path`;
- collection/service settings are configuration;
- rebuild validates chunk manifest, embedding manifest, row count, vector dimension, and model compatibility.

### `src/cics/retrieval/`

Owns query embedding, vector search, and source-grounded result reconstruction.

Recovered basis:

- R2 `query_chat_rag.py` — ADAPT

Required outcome:

- query results are resolved directly from durable payload/manifest identity;
- no filesystem re-scan is used to map vector hits back to content;
- loader and query share one payload schema;
- the recovered string-`chunk_id` versus integer-index incompatibility is eliminated by contract, not patched ad hoc.

### `src/cics/registry/`

Owns authoritative project/entity registry construction and policy.

Recovered basis:

- R2 `schemas/entity_schema.json` — ADAPT
- R2 `build_authoritative_registry.py` — ADAPT

Required outcome:

- preserve the move away from broad regex inference toward explicit authority;
- move historical project/folder taxonomy out of Python source into declarative policy/evidence;
- fix syntax and portability defects during promotion rather than preserving the broken file;
- authority may use folder/repository/project evidence, but folder existence alone must not silently become universal project truth;
- entity IDs must follow the canonical provenance/identity contract.

The R2 `extract_projects.py` → `normalize_projects.py` → `qualify_projects.py` heuristic lineage is REJECT and must not be restored as the authoritative registry mechanism.

## Root-level schemas

Schemas live at repository root rather than inside one runtime subsystem because they define cross-module contracts.

### Recovered/adapted schemas

- `schemas/entity_v1.json` ← R2 `entity_schema.json`
- `schemas/corpus_metadata_v1.json` ← R3 `metadata_schema_v1.json`

### Required consolidation schemas

These do not represent recovered completed implementations; they are required to prevent the historical interface failures from recurring:

- `artifact_metadata_v1.json` — artifact lifecycle/state/provenance contract;
- `chunk_record_v1.json` — canonical chunk identity, source spans, content/provenance metadata;
- `vector_payload_v1.json` — shared loader/query payload contract.

Their exact fields must be decided before corresponding ADAPT code is promoted.

## Cross-cutting contracts that must be resolved before promotion

### 1. Portable identity

At minimum CICS needs distinct durable identities for:

- registered source;
- document/conversation;
- message or normalized source unit where applicable;
- chunk;
- embedding build/manifest;
- artifact;
- entity/project.

Absolute filesystem paths may be recorded as observations or deployment locations, but must not be the durable identity input.

### 2. Configuration ownership

Canonical modules receive resolved settings through the configuration layer. Donor scripts must not continue to discover authority from hard-coded paths or mutate `sys.path` to `~/cics`.

### 3. Manifest ordering

A manifest establishes the authoritative record sequence. Downstream components consume that sequence and its identity/hash. Re-sorting filesystem paths independently at each stage is prohibited because it recreates the historical row/payload mismatch risk.

### 4. Chunk ↔ embedding binding

Every embedding row must have an explicit canonical chunk identity. Completion means more than a correctly shaped `.npy` file: the embedding manifest must prove model/config, row count, chunk-manifest identity, and row-to-chunk mapping.

### 5. Vector payload contract

Qdrant point IDs may be operational IDs, but canonical chunk identity belongs in the payload. Loader and retrieval code must consume the same schema. Absolute local chunk paths are not canonical payload references.

### 6. Artifact audit/provenance

State transition behavior from R1 is retained, but destructive and approval operations require durable event/audit semantics before canonical promotion.

### 7. Registry authority

RAG/regex mention frequency cannot create authoritative project identity. Registry authority must come from explicit governed evidence/policy, with inference clearly labeled separately.

### 8. Source/runtime separation

The canonical Git repository may contain source, schemas, tests, reconstruction documentation, recovery snapshots, and safe example configuration. It must not absorb mutable Qdrant state, embedding matrices, generated chunk corpora, runtime checkpoints, logs, caches, private raw chats, virtual environments, or machine-specific secrets.

## Consolidation order

Promotion should follow dependency order rather than donor order:

1. **Configuration contract** — define portable settings ownership and example configuration.
2. **Provenance/identity contract** — correct R3 path-based identity and define source/document/chunk IDs.
3. **Schemas** — finalize corpus, chunk, entity, artifact, and vector payload contracts needed by recovered components.
4. **R3 corpus-control foundation** — manifest, validation, determinism, audit, configurable layout.
5. **R1 artifact lifecycle** — package KEEP helpers and ADAPT service/reporting/maintenance behavior against configuration/provenance.
6. **R2 chat chunker** — adapt to canonical source/manifest identity without starting a new ingestion implementation.
7. **R2 embedding generator** — bind embeddings to canonical chunk manifest and runtime checkpoint policy.
8. **R2 vector loader + retrieval** — establish one shared payload interface and eliminate filesystem-index coupling.
9. **R2 authoritative registry concept** — adapt schema/builder/policy after identity and authority rules are settled.
10. **Reassess gaps** — only after all salvageable donor components are consolidated determine what CICS functionality genuinely requires new implementation.

This ordering specifically prevents the accidental `rebuild/cics-phase1` work from becoming the architecture by default.

## Explicit exclusions from canonical source

Do not promote:

- R1 `write_file.py`;
- R1 `parse_and_write.py` as an unrestricted writer;
- R1/R2 naive coding chunker copies;
- R1 placeholder `create_embeddings.py`;
- R2 regex project extraction/normalization/qualification pipeline;
- R1/R2 obsolete `config/paths.json`;
- R2 runtime checkpoint files;
- R2 `arena_mode.sh`;
- R2 `embedding_guard.sh` as product source;
- R3 generated `audit_report.json` as product source;
- R4/R5 corpus/runtime trees wholesale.

All remain available as historical evidence in recovery material where already preserved.

## Gate before creating canonical `src/`

The repository is ready for source promotion only after the following design decisions are recorded and internally consistent:

- portable source/document/chunk identity rule;
- canonical configuration shape and root ownership;
- canonical manifest record and ordering rule;
- chunk record schema;
- embedding manifest contract;
- vector payload schema shared by loader/retrieval;
- artifact metadata/audit contract;
- entity registry authority policy.

Until those contracts are resolved, `src/` should remain absent on `main`. The next reconstruction task is therefore **contract consolidation**, beginning with portable identity and configuration, not code movement or new Phase-1 feature implementation.

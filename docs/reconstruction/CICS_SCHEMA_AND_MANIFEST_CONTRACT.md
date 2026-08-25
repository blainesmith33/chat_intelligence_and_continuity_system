# CICS Schema and Manifest Contract

Status: reconstruction/consolidation design gate  
Prepared: 2026-08-25  
Basis: `CICS_IDENTITY_AND_CONFIGURATION_CONTRACT.md`, recovered R1/R2/R3 schemas and manifests, and `CICS_CANONICAL_SOURCE_TREE_DESIGN.md`

This document resolves the cross-module record and manifest contracts required before recovered donor code may be promoted into canonical `src/`.

It does **not** implement ingestion, chunking, embeddings, Qdrant, retrieval, artifact services, or registry construction. It defines the records those implementations must consume and produce.

## 1. Contract objectives

The schema/manifest layer must eliminate the historical failure modes found across R1/R2/R3:

- source identity inferred from filesystem paths;
- document identity changing when a corpus moves;
- independently sorted directory scans defining downstream row correspondence;
- chunk identity encoded only in filenames;
- embedding matrices with no durable row-to-chunk manifest;
- vector loader/query disagreement over `chunk_id` type and meaning;
- artifact state stored only in mutable sidecars without an append-only event model;
- entity IDs regenerated from display names;
- corpus taxonomies embedded directly in validation code;
- generated runtime state being mistaken for authoritative source records.

The canonical rule is:

> **Every cross-subsystem handoff is an explicit versioned record or manifest. No downstream component is allowed to reconstruct identity from path order, filenames, array position, or mutable display names.**

## 2. Schema family

Canonical CICS requires the following schema family before source promotion:

```text
schemas/
├── source_record_v1.json
├── document_record_v1.json
├── message_record_v1.json
├── chunk_record_v1.json
├── embedding_manifest_record_v1.json
├── vector_payload_v1.json
├── artifact_metadata_v1.json
├── artifact_event_v1.json
└── entity_v1.json
```

The source-tree design previously used broader placeholder names such as `corpus_metadata_v1.json`. This contract refines that placeholder into distinct source/document/message records because one schema cannot safely represent all three identity layers.

Actual schema files are created only after this contract is accepted as the canonical field definition.

## 3. Schema conventions

All canonical record schemas must follow these rules:

- explicit `schema_id` field;
- explicit `schema_version` integer;
- `additionalProperties: false` unless a future schema explicitly documents an extension object;
- IDs serialized as opaque strings using the namespace prefixes defined by the identity contract;
- content hashes serialized separately from logical IDs;
- no required machine-specific absolute path field;
- timestamps, where present, use UTC RFC 3339 / ISO-8601 form;
- arrays whose order is semantically meaningful preserve order explicitly;
- arrays whose order is not semantically meaningful must be canonicalized before manifest hashing;
- nullable fields are explicit rather than represented by missing/ambiguous sentinel strings;
- schema evolution occurs by new schema/version identifiers, not silent field reinterpretation.

A schema version change is required when field meaning, requiredness, canonicalization, or identity semantics change.

## 4. Canonical serialization and manifest hashing

Canonical manifests use UTF-8 JSON Lines (`.jsonl`) unless a later component contract explicitly requires another representation.

Canonical JSONL serialization rules:

- UTF-8, no BOM;
- one JSON object per line;
- `\n` newline;
- fixed canonical field order per record type;
- compact separators `,` and `:`;
- no insignificant whitespace;
- deterministic array ordering where the array is defined as order-insensitive;
- no floating-point values in identity-critical manifest metadata unless a future version specifies canonical float encoding;
- exactly one trailing newline at end of file.

`manifest_hash` is BLAKE3 over the exact canonical manifest bytes.

A manifest hash proves the canonical record sequence and values. It does **not** prove that mutable external runtime state still exists at any observed path.

## 5. Manifest ordering rule

Filesystem path sorting is rejected as canonical ordering.

For each manifest family, records are ordered by canonical ID unless a stronger domain order is explicitly required:

- source manifest: `source_id`;
- document manifest: `document_id`;
- message manifest: `(document_id, source_order, message_id)`;
- chunk manifest: `(document_id, chunk_ordinal, chunk_id)`;
- embedding manifest: `row_index` after validating that each row explicitly names its `chunk_id`;
- entity registry: `entity_id`.

`source_order`, `chunk_ordinal`, and `row_index` are operational sequence fields. They never replace canonical identity.

## 6. `source_record_v1`

A source record represents one immutable registered input object.

### Required fields

```text
schema_id
schema_version
source_id
source_format
content_hash
byte_length
```

### Optional fields

```text
media_type
observed_name
created_at_source
registration_notes
```

### Semantics

- `source_id` follows the content-addressed source rule in the identity contract.
- `content_hash` is the BLAKE3 hash of exact registered bytes and is stored separately even when it participates in `source_id` derivation.
- `source_format` is a stable namespace such as `chatgpt_export_json`, `chatgpt_conversation_json`, `markdown_transcript`, or another formally registered format.
- `observed_name` may record the filename presented at registration but is not identity or location authority.
- `byte_length` is the exact registered byte count.

### Explicit exclusions

The canonical source record does not require:

- absolute path;
- machine name;
- mount point;
- import working directory;
- current storage URI.

Those belong in a deployment/provenance locator ledger outside the portable manifest hash.

## 7. `document_record_v1`

A document record represents a logical parsed unit from a source, normally one conversation for ChatGPT data.

### Required fields

```text
schema_id
schema_version
document_id
source_id
document_type
parser_id
parser_version
source_locator
```

### Optional fields

```text
native_document_id
title
created_at
updated_at
content_hash
metadata
```

### `source_locator`

`source_locator` is a structured source-local locator sufficient to find the logical document inside the registered source. It may contain native mapping/object keys or source-local indices, but not an absolute filesystem path.

### Semantics

- `document_id` follows the native-ID-preferred/fallback rule already established.
- `native_document_id`, when present, preserves the provider/export identifier verbatim.
- parser identity/version is required because parser behavior can change normalized interpretation without altering raw source bytes.
- `content_hash`, when present, hashes the canonical normalized document representation, not the raw source file.

## 8. `message_record_v1`

A message record is the normalized source unit used to preserve chat role, order, timestamps, and source traceability before chunking.

### Required fields

```text
schema_id
schema_version
message_id
document_id
source_order
role
content
content_hash
source_locator
parser_id
parser_version
```

### Optional fields

```text
native_message_id
created_at
author_name
content_type
parent_message_id
branch_id
metadata
```

### Semantics

- `source_order` is deterministic within the normalized document view.
- `role` must use a controlled vocabulary defined by the parser/source-format contract; unknown provider-specific roles must not silently become `user` or `assistant`.
- `content_hash` hashes the canonical normalized message content.
- `source_locator` preserves enough source-local detail to trace the normalized message to the registered source.
- branch/mapping relationships may be preserved without forcing every source format into one tree model.

This schema exists specifically because the recovered chat chunker operated on flattened `.txt` input and did not preserve message-level roles/timestamps/spans.

## 9. Source/document/message manifests

Canonical intake produces three related manifests when the source format supports logical document/message parsing:

```text
sources_manifest.jsonl
documents_manifest.jsonl
messages_manifest.jsonl
```

Each manifest includes a companion metadata record or sidecar containing at least:

```text
manifest_schema_id
manifest_version
record_schema_id
record_count
manifest_hash
created_at_utc
producer_id
producer_version
input_manifest_refs
policy_hash
```

For the source manifest, `input_manifest_refs` may be empty because it is the registration boundary.

For document/message manifests, upstream manifest hashes/IDs are explicit inputs.

## 10. `chunk_record_v1`

A chunk record is the canonical handoff between normalized source content and embedding generation.

### Required fields

```text
schema_id
schema_version
chunk_id
document_id
chunk_ordinal
source_spans
content
content_hash
chunker_id
chunker_version
chunk_policy_hash
```

### Optional fields

```text
source_id
language
section
entity_refs
token_count
character_count
metadata
```

### `source_spans`

`source_spans` is an ordered, non-empty array. Each span contains:

```text
message_id
start_offset
end_offset
```

For non-message source formats, a future schema version may permit a typed document/source-unit span object. The v1 chat path uses message IDs.

Offsets are defined against the canonical normalized message `content`, not raw file byte offsets.

### Semantics

- `chunk_id` follows the identity contract and binds document, ordered source spans, content hash, chunker version, and chunk-policy hash.
- `chunk_ordinal` is a deterministic position inside one document build and is not identity.
- `content` is canonical retrieval/embedding text for the chunk.
- `section`, `language`, and `entity_refs` are descriptive/classification metadata and may not replace source provenance.

### Historical correction

The recovered R2 filename format:

```text
<stem>__<sourceid>__<language>_chunk_<index>.txt
```

is not the canonical record. Filenames may be generated for operator convenience, but the JSONL record is authoritative.

## 11. Chunk manifest

Canonical chunk output is represented by:

```text
chunks_manifest.jsonl
chunks_manifest.meta.json
```

The metadata record requires:

```text
manifest_id
manifest_hash
record_count
record_schema_id
source_manifest_hash
document_manifest_hash
message_manifest_hash
chunker_id
chunker_version
chunk_policy_hash
created_at_utc
```

`manifest_id` is deterministically derived from the canonical upstream manifest identities/hashes and chunking-policy identity according to the identity contract.

A downstream embedding job must consume this exact manifest, not recursively scan a chunk directory.

## 12. `embedding_manifest_record_v1`

The embedding manifest binds array rows to canonical chunk identity.

### Required fields

```text
schema_id
schema_version
embedding_build_id
row_index
chunk_id
vector_dimension
vector_dtype
model_id
embedding_policy_hash
```

### Optional fields

```text
model_revision
vector_content_hash
metadata
```

### Semantics

- `row_index` is zero-based and unique within one embedding build.
- `chunk_id` is the canonical identity of the exact chunk represented by that row.
- `vector_dimension` and `vector_dtype` must agree with the physical matrix.
- `model_id` is the canonical model identifier; `model_revision` is required when the model provider exposes a revision necessary for reproducibility.
- `vector_content_hash`, if enabled, hashes the canonical byte representation of that row and provides stronger matrix integrity checking.

## 13. Embedding manifest metadata

Embedding generation produces:

```text
embeddings.npy
embeddings_manifest.jsonl
embeddings_manifest.meta.json
```

The metadata record requires:

```text
embedding_build_id
record_count
chunk_manifest_id
chunk_manifest_hash
embedding_manifest_hash
model_id
model_revision
vector_dimension
vector_dtype
embedding_policy_hash
implementation_id
implementation_version
completed
created_at_utc
```

`completed` is only true after:

- every manifest row exists;
- every row index from `0..record_count-1` appears exactly once;
- physical matrix row count matches `record_count`;
- physical matrix dimension/dtype match metadata;
- every `chunk_id` exists in the referenced chunk manifest;
- no duplicate `chunk_id` exists unless a future policy explicitly allows multiple vectors per chunk.

A correctly shaped `.npy` file alone is never proof of completion.

Runtime checkpoint files are not part of this canonical manifest family.

## 14. `vector_payload_v1`

The vector payload is the contract shared by loader and retrieval.

### Required fields

```text
schema_id
schema_version
chunk_id
document_id
chunk_manifest_id
embedding_build_id
content_hash
```

### Required retrieval material

At least one of the following must be present according to deployment policy:

```text
text
content_ref
```

### Optional fields

```text
source_id
message_ids
section
language
entity_refs
chunk_ordinal
metadata
```

### Semantics

- `chunk_id` is always a string canonical CICS ID.
- vector-store point ID may be integer, UUID, or store-specific, but is not canonical identity.
- `content_ref`, when used, is a portable manifest/content-addressed reference, not an absolute local chunk path.
- retrieval must never re-scan or re-sort local chunk files to resolve a hit.
- loader and query validate the same schema version.

This directly eliminates the recovered R2 defect where the loader emitted a string `chunk_id` while the query treated it as an integer filesystem index.

## 15. Vector collection build metadata

A vector-store rebuild produces a portable build receipt outside the database itself containing at least:

```text
vector_build_id
vector_payload_schema_id
chunk_manifest_id
chunk_manifest_hash
embedding_build_id
embedding_manifest_hash
collection_logical_name
vector_dimension
distance_metric
record_count
created_at_utc
status
```

Deployment-specific host, port, container ID, physical collection UUID, or filesystem state may be recorded separately but does not participate in portable data identity unless required by a future receipt version.

## 16. `artifact_metadata_v1`

Artifact metadata represents the current governed state of one artifact.

### Required fields

```text
schema_id
schema_version
artifact_id
status
content_hash
created_at_utc
created_by
current_revision
```

### Optional fields

```text
filename
media_type
staging_locator
committed_locator
source_evidence_refs
notes
```

### Semantics

- `artifact_id` is assigned once at staging and never changes through state transitions.
- `content_hash` describes the current governed content revision.
- `current_revision` starts at 1 and increments only under an explicit revision operation defined by a future artifact service contract.
- filesystem locators are deployment attributes and are not identity.
- state must be one of the artifact lifecycle states approved by the consolidated state machine.

## 17. `artifact_event_v1`

Artifact audit history is append-only and separate from mutable current-state metadata.

### Required fields

```text
schema_id
schema_version
event_id
artifact_id
event_type
occurred_at_utc
actor
from_status
to_status
content_hash
```

### Optional fields

```text
reason
revision
previous_content_hash
source_evidence_refs
operation_metadata
```

### Event types

The initial vocabulary includes:

```text
STAGED
APPROVED
REJECTED
PROMOTED
CONTENT_REVISED
DELETED_FROM_STAGING
DELETED_FROM_COMMITTED
PURGED
```

The exact legal state transitions remain governed by the artifact state machine; the event vocabulary records what happened.

Destructive operations must produce an audit event before/atomically with the destructive mutation according to the implementation contract. A purge must not erase its own audit history.

## 18. Artifact event log

Canonical artifact governance maintains an append-only logical event stream keyed by `artifact_id`.

The physical storage format may initially be JSONL, SQLite, or another transactional store, but export/rebuild must produce canonical event records conforming to `artifact_event_v1`.

The current-state metadata record must be reconcilable from event history. Divergence between current metadata and event history is an integrity failure, not something reporting code silently ignores.

## 19. `entity_v1`

The recovered R2 entity schema is retained conceptually but tightened around immutable identity and evidence authority.

### Required fields

```text
schema_id
schema_version
entity_id
entity_type
canonical_name
authority_level
status
evidence_refs
```

### Optional fields

```text
aliases
parent_entity_id
related_entity_ids
notes
policy_refs
```

### Identity rule

`entity_id` is explicitly governed and immutable. It is not generated at runtime from `canonical_name`.

### Authority levels

Initial authority vocabulary:

```text
authoritative
supporting
inferred
```

### Evidence references

Every authoritative or supporting entity record must identify the evidence/policy basis through typed references using canonical CICS IDs or governed repository/project references.

A minimum evidence-ref shape is:

```text
ref_type
ref
role
```

Examples of `ref_type` may include:

```text
source_id
document_id
chunk_id
repository
folder_policy
project_index
charter
manual_decision
```

`manual_decision` must refer to a durable governed decision record or explicit registry policy entry, not an undocumented in-memory assertion.

### Historical correction

RAG mention frequency, regex matches, and heuristic qualification may create `inferred` candidates in future work but cannot directly create `authoritative` entities.

## 20. Entity registry manifest

The authoritative registry is a canonical JSONL manifest:

```text
entity_registry.jsonl
entity_registry.meta.json
```

Registry metadata requires:

```text
registry_id
registry_hash
record_count
entity_schema_id
registry_policy_id
registry_policy_hash
created_at_utc
```

Records are ordered by immutable `entity_id`.

Aliases and display-name changes may alter registry hash/version but must not alter entity IDs.

## 21. Corpus taxonomy and classification

R3’s recovered `section`, `authority_level`, `language`, and `project` fields remain useful concepts, but the recovered engineering-corpus enum set is not universal CICS schema authority.

Canonical policy therefore distinguishes:

- structural identity/provenance fields defined in schemas;
- corpus-specific classification vocabularies defined by versioned processing policy.

A chunk/source/document schema may contain values such as `section` or `language`, but validation against a particular allowed vocabulary belongs to the selected corpus policy version unless the vocabulary is truly universal.

This prevents the 28-section engineering taxonomy from becoming a permanent hard-coded requirement for chat corpora or future source types.

## 22. Content location and runtime locator records

Portable manifests deliberately exclude required absolute paths. Runtime still needs to know where bytes live.

CICS therefore treats physical location as a separate deployment concern. A runtime locator record may map canonical IDs to current physical locations, for example:

```text
source_id -> /mounted/archive/file.json
chunk_manifest_id -> /runtime/builds/.../chunks_manifest.jsonl
embedding_build_id -> /runtime/builds/.../embeddings.npy
artifact_id -> configured staging/committed path
```

Locator records are mutable deployment state. Changing them does not alter the portable manifest or object identity.

## 23. Manifest dependency graph

The canonical recovered RAG path becomes:

```text
registered source bytes
        |
        v
sources_manifest
        |
        v
documents_manifest
        |
        v
messages_manifest
        |
        v
chunks_manifest
        |
        v
embeddings_manifest + embeddings.npy
        |
        v
vector build receipt / vector payloads
        |
        v
retrieval results by canonical chunk_id
```

Every arrow is an explicit manifest/hash reference.

No stage may substitute an independently regenerated directory listing for the referenced upstream manifest.

## 24. Rebuild semantics

A deterministic rebuild must produce the same canonical manifest bytes when all identity-affecting inputs and processing policy are unchanged.

A rebuild is expected to produce a different manifest/build identity when any of the following changes materially:

- registered source bytes;
- parser/canonicalization version;
- normalized source-unit structure;
- chunking algorithm/version or policy;
- embedding model/revision or semantic embedding policy;
- schema version where canonical record meaning changes;
- registry policy/evidence set.

Machine path moves, Qdrant host changes, checkpoint location changes, log location changes, and other deployment-only changes must not create new logical source/document/chunk IDs.

## 25. Validation requirements

Canonical validators must enforce the complete selected schema rather than a hand-written subset that silently ignores constraints.

Validation gates include:

### Structural validation

- required fields;
- field types;
- enum/pattern/const constraints;
- additional-property policy;
- ID namespace prefix;
- timestamp format.

### Referential validation

- every `document.source_id` exists;
- every `message.document_id` exists;
- every chunk source span references an existing message/source unit;
- every embedding record references an existing chunk;
- every vector payload references an existing chunk and embedding build;
- every artifact event references an existing artifact;
- entity relationships reference known entities or explicitly permitted external references.

### Sequence validation

- `source_order` deterministic/unique within document where required;
- `chunk_ordinal` contiguous according to selected chunk policy;
- embedding `row_index` unique and contiguous;
- manifest record order matches canonical ordering rule.

### Integrity validation

- content hashes match content;
- manifest metadata hash matches exact manifest bytes;
- matrix dimensions/counts match embedding manifest;
- build references match upstream manifest IDs/hashes.

## 26. Generated state versus canonical records

The following are canonical portable records or receipts and may be preserved when appropriate:

- source/document/message/chunk manifests;
- manifest metadata/receipts;
- entity registry and policy;
- artifact metadata/event exports;
- safe schemas;
- build receipts containing no secrets or machine-private information.

The following remain runtime/generated state and are not automatically committed to the source repository:

- raw private chat exports;
- generated chunk payload directories when the manifest can reproduce/reference them;
- embedding `.npy` matrices;
- Qdrant database files;
- mutable checkpoint files;
- logs;
- caches;
- virtual environments;
- machine locator mappings containing private paths/endpoints.

## 27. Donor promotion consequences

This contract resolves the adaptation requirements for the recovered components.

### R3 `manifest_builder.py`

Promote only after replacing absolute-path record identity/order with the source/document manifest chain and canonical ID ordering.

### R3 `metadata_validator.py`

Do not preserve its partial schema implementation as the canonical validator. Canonical validation must enforce the complete selected schema.

### R3 `determinism_verifier.py`

Its repeat-build/byte-compare concept remains valid, but verification targets canonical manifest bytes and additionally checks portable identity across location moves in integration tests.

### R3 `audit_report.py`

Adapt reports to canonical manifest families and referential/integrity checks instead of only section/language distributions.

### R2 `chunk_chat_corpus.py`

Adapt it to consume normalized message/document manifests and emit `chunk_record_v1`; do not preserve filename-derived identity or destructive directory clearing as the contract.

### R2 `create_embeddings.py`

Adapt it to consume `chunks_manifest.jsonl` and emit `embedding_manifest_record_v1` plus build metadata. Filesystem sorting is removed as row authority.

### R2 Qdrant loader

Adapt it to validate embedding/chunk manifests and emit `vector_payload_v1` payloads. Absolute `chunk_path` is not canonical payload identity.

### R2 query

Rewrite its interface against `vector_payload_v1`; it consumes `chunk_id` directly and never treats it as a list index.

### R1 artifact lifecycle

Preserve state-machine behavior, but current metadata uses `artifact_metadata_v1` and all state/destructive operations emit `artifact_event_v1`.

### R2 registry builder

Retain the explicit-authority direction but emit `entity_v1` records from declarative policy/evidence with immutable declared IDs.

## 28. Proposed schema-to-source mapping

When source promotion begins, schema ownership maps to modules as follows:

```text
schemas/source_record_v1.json
schemas/document_record_v1.json
schemas/message_record_v1.json
    -> src/cics/corpus/manifest.py + validation.py

schemas/chunk_record_v1.json
    -> src/cics/corpus/chat_chunking.py + manifest.py

schemas/embedding_manifest_record_v1.json
    -> src/cics/embeddings/generator.py + manifest.py

schemas/vector_payload_v1.json
    -> src/cics/vector/interface.py + qdrant_store.py
       src/cics/retrieval/query.py

schemas/artifact_metadata_v1.json
schemas/artifact_event_v1.json
    -> src/cics/artifacts/metadata.py + service.py + reporting.py

schemas/entity_v1.json
    -> src/cics/registry/builder.py + policy.py
```

The physical Python modules do not become the schema authority. The schema files and this contract define the cross-module interface.

## 29. Acceptance gate

The schema/manifest contract is considered consolidated when canonical implementation obeys all of the following:

- source, document, message, and chunk identities are explicit fields;
- no canonical record requires an absolute machine path;
- every derived stage identifies the upstream manifest/build it consumed;
- manifest hashing uses canonical serialized bytes;
- record order is canonical and independent of filesystem path order;
- chunk records preserve message/source spans and content hash;
- embedding rows explicitly bind `row_index` to `chunk_id`;
- vector loader/query share exactly one payload schema;
- artifact current state is separate from append-only audit events;
- entity IDs are immutable declared keys, not display-name slugs;
- corpus-specific taxonomies are policy rather than universal hard-coded schema assumptions;
- full structural, referential, sequence, and integrity validation exists before downstream processing;
- runtime locators/state remain separate from portable manifests.

## 30. Gate after this document

With identity/configuration and schema/manifest contracts defined, the repository has enough design authority to begin **controlled source promotion** from the KEEP/ADAPT donor set.

Promotion must still follow dependency order:

1. canonical configuration/provenance foundation;
2. schema files and validation infrastructure;
3. R3 corpus-control foundation;
4. R1 artifact lifecycle;
5. R2 chat chunking;
6. R2 embeddings;
7. R2 vector/retrieval;
8. R2 registry.

No missing feature should be invented merely to make the promoted donor code appear complete. After salvageable donor implementation is consolidated and tested, remaining gaps are reassessed as actual rebuild work.

Until that promotion step begins deliberately, `src/` remains absent on `main`.
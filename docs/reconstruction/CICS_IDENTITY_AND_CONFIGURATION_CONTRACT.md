# CICS Identity and Configuration Contract

Status: reconstruction/consolidation design gate  
Prepared: 2026-08-25  
Basis: recovered R1/R2/R3 components and the canonical source-tree design

This document resolves the first two cross-cutting contracts required before donor code may be promoted into canonical `src/`: **portable identity** and **configuration ownership**.

It does not implement ingestion, chunking, embeddings, Qdrant, retrieval, registry construction, or artifact services. It defines the interfaces those recovered components must obey when they are consolidated.

## 1. Contract goals

The canonical contracts must prevent the defects found in the recovered lineages:

- absolute filesystem paths changing document identity;
- independently sorted directories defining chunk/embedding/vector correspondence;
- machine/user paths embedded in product source;
- collection names, hosts, ports, model names, and runtime roots embedded in scripts;
- artifact metadata using paths as primary identity;
- registry IDs being regenerated from mutable display names;
- generated runtime/checkpoint state being mistaken for source configuration.

The central rule is:

> **Identity describes the logical object. Location describes where one observed copy currently exists. They are not the same thing.**

## 2. Hashing baseline

BLAKE3 remains the preferred recovered hashing primitive from R3.

Canonical code must distinguish the following concepts rather than using one hash for all purposes:

- **content hash** — hash of exact bytes or a formally canonicalized record;
- **identity value** — stable identifier for a logical object;
- **manifest hash** — hash of canonical serialized manifest bytes;
- **policy/config hash** — hash of canonical processing policy, excluding machine-local deployment values and secrets;
- **snapshot/build ID** — identifier derived from the authoritative input manifest plus processing-policy identity where deterministic derivation is appropriate.

A filesystem path may be stored in provenance as an observed location but must never be the sole input to a durable identity.

## 3. Identifier representation

Canonical IDs should be serialized as opaque strings with a type prefix so values from different namespaces cannot be confused.

Recommended representation:

```text
src_<value>
doc_<value>
msg_<value>
chk_<value>
emb_<value>
art_<value>
ent_<value>
```

The prefix is part of the public identifier string. The value behind the prefix may be deterministic or assigned depending on the object type below.

The exact encoded length is an implementation detail, but canonical IDs must not be shortened so aggressively that collision handling becomes a practical concern. The recovered R2 ten-hex source token is therefore not sufficient as the canonical identifier.

## 4. Source identity

A **registered source** is the immutable input object supplied to CICS, such as a raw exported conversation file or another registered evidence file.

### Canonical rule

`source_id` is content-addressed from the exact registered source bytes plus an explicit source-format namespace.

Conceptually:

```text
source_id = BLAKE3(source_format + NUL + exact_source_bytes)
```

Properties:

- moving or renaming the source does not change `source_id`;
- two byte-identical copies of the same source format resolve to the same source identity;
- modifying any source byte produces a different identity;
- source format is included so equal byte strings under materially different input contracts do not silently collapse.

Observed filename, absolute path, machine, mount point, import time, and storage URI are provenance fields, not identity inputs.

## 5. Document / conversation identity

A **document** is the logical unit parsed from a registered source. For ChatGPT exports this normally means a conversation.

### Preferred rule

When the source format contains a stable native object ID, canonical `document_id` is derived from:

```text
source_format namespace + native object type + native object ID
```

The registered `source_id` remains a provenance link but is not required to be part of the document identity when the native ID is authoritative and stable. This allows the same logical exported conversation to remain the same document across repeated archive exports.

### Fallback rule

When no stable native ID exists, derive `document_id` from a canonical document fingerprint based on normalized logical content and stable source-local structure, not path or filename.

Fallback identity must be versioned because changes to canonicalization rules can change the resulting identifier.

### Required provenance fields

A document record must retain at least:

- `document_id`;
- `source_id`;
- source format/type;
- native source ID when available;
- observed title/name when available;
- parser/canonicalization version;
- source locator information sufficient to trace back into the registered source.

## 6. Message / normalized source-unit identity

Where the input format exposes stable native message or mapping-node IDs, CICS should preserve them through a canonical `message_id` namespace scoped to the containing document.

Conceptually:

```text
message_id = BLAKE3(document_id + NUL + native_message_locator)
```

If no native message identifier exists, the fallback locator must be a deterministic source-unit locator established by the parser contract. It must not use the output file path.

Message content hash is separate from message identity so metadata/content integrity can be checked without confusing edits or parser changes with object identity.

## 7. Chunk identity

A chunk is a derived processing object and its identity must bind both content and provenance.

Canonical `chunk_id` must be derived from all of the following:

- parent `document_id`;
- ordered source-unit/message span references used to construct the chunk;
- exact canonical chunk content hash;
- chunking algorithm/version;
- canonical chunking-policy hash.

Conceptually:

```text
chunk_id = BLAKE3(
    document_id
    + ordered_source_spans
    + content_hash
    + chunker_version
    + chunk_policy_hash
)
```

Consequences:

- moving chunk files does not change identity;
- filesystem enumeration order does not change identity;
- changing segmentation policy intentionally creates new chunk identities;
- identical text copied from two different source locations does not silently collapse into one provenance object;
- vector-store point IDs and embedding row numbers are not chunk identity.

The canonical chunk manifest, not a directory scan, defines processing order.

## 8. Embedding build identity

Individual vectors are addressed by canonical `chunk_id`; they do not need a second logical identifier merely because they occupy an array row.

An **embedding build/manifest** does require a durable ID.

Canonical `embedding_build_id` is derived from:

- canonical chunk-manifest hash/ID;
- embedding model identity;
- model revision when available;
- vector dimension;
- canonical embedding-policy hash;
- implementation/contract version where it affects output semantics.

Runtime choices that do not affect semantic output, such as a temporary checkpoint path or log path, must not enter the build identity.

Each embedding-manifest row must explicitly contain its `chunk_id` and embedding row index. The row index is an operational locator only.

## 9. Vector payload identity

Qdrant or another vector store may use implementation-specific point IDs, but canonical identity resides in the payload.

Every canonical vector payload must include at minimum:

- `chunk_id`;
- `document_id`;
- chunk-manifest/build reference;
- embedding-build reference;
- source/provenance reference sufficient for retrieval reconstruction;
- text or an immutable text/content reference according to the final payload schema.

Absolute local `chunk_path` must not be required to resolve a result.

The recovered R2 integer row-index/string-`chunk_id` mismatch is therefore eliminated structurally: retrieval consumes canonical `chunk_id`, never an inferred filesystem index.

## 10. Artifact identity

Artifacts differ from derived corpus objects because their lifecycle state may change while they remain the same governed artifact.

Canonical `artifact_id` must therefore be an explicitly assigned opaque identifier created when the artifact first enters governed staging. It must remain unchanged through:

```text
STAGED -> APPROVED -> COMMITTED
       -> REJECTED
```

Artifact content has a separate BLAKE3 content hash. If artifact content changes after creation, the metadata/audit contract must record that change explicitly rather than silently changing artifact identity.

Paths, staging roots, committed roots, filenames, status, timestamps, and approval metadata are attributes/provenance, not artifact identity.

## 11. Entity / project identity

Registry entities require stable IDs that survive display-name and alias changes.

Canonical `entity_id` must be explicitly declared by the authoritative registry/policy and treated as immutable after assignment. It must **not** be regenerated automatically from the current canonical display name.

A human-readable stable key is acceptable when explicitly governed, for example:

```text
ent_project_cics
```

Changing the display name or adding aliases must not change the entity ID.

Regex/RAG inference may propose relationships or candidate entities in later work, but it may not allocate authoritative entity identity by itself.

## 12. Identity relationships

The minimum identity chain for the recovered RAG lineage is:

```text
source_id
   -> document_id
      -> message/source-unit IDs
         -> chunk_id
            -> embedding manifest row
               -> vector payload
```

The relationship is explicit in records/manifests. It must never be reconstructed indirectly from matching filenames or independently sorted directory listings.

Artifacts and registry entities have separate identity namespaces but may reference any of the evidence IDs above.

## 13. Configuration ownership

Canonical configuration is divided into two classes because the recovered systems mixed machine placement with processing semantics.

### A. Deployment configuration

Describes where and how this installation runs:

- filesystem/runtime roots;
- Qdrant host/port/collection;
- runtime/checkpoint/log directories;
- model cache/device preferences;
- machine-specific external source locations;
- service endpoints.

Deployment configuration may differ between machines without changing logical corpus/document/chunk identity.

### B. Processing policy

Describes choices that materially affect generated data:

- source/parser format versions;
- chunk sizes/overlap/segmentation rules;
- supported corpus taxonomy and authority policy;
- embedding model/revision and normalization settings;
- vector dimension and distance metric where required for compatibility;
- canonical serialization/version rules;
- schema versions;
- registry policy versions.

Processing policy is hashable and versioned. Policy values that affect generated output must participate in the appropriate build/derived-object identity.

## 14. Canonical configuration file

The repository should contain only safe example configuration, initially represented by:

```text
config/examples/cics.example.toml
```

A real deployment may use an external TOML configuration file outside Git.

The example file is documentation and a validated configuration example, not machine authority.

Suggested top-level sections:

```toml
[paths]

[artifacts]

[corpus]

[chunking]

[embeddings]

[vector_store]

[registry]

[runtime]
```

Exact fields are finalized when the corresponding schemas/contracts are consolidated. The configuration loader should reject unknown keys rather than silently ignoring misspellings in authoritative configuration.

## 15. Configuration precedence

The canonical precedence order is:

1. explicit command/API argument for the current operation;
2. environment variable where that setting is intentionally environment-overridable;
3. selected deployment configuration file;
4. safe documented default, only when the value is genuinely portable and non-authoritative.

There must be no hidden fallback to `/home/deck`, `/home/kimberly`, `~/cics`, `D:\...`, or another historical location.

A required path/service setting without a valid value must fail clearly instead of guessing.

## 16. Path resolution

Paths may be supplied as absolute or explicitly documented relative values.

Relative paths are resolved against a defined configuration base, not the caller's accidental current working directory. After resolution, runtime code may use absolute paths internally for filesystem access.

Resolved absolute paths remain deployment observations only and do not enter portable IDs unless a future contract explicitly identifies a path itself as the governed object.

Before mutation, modules must validate that configured writable paths are within the appropriate configured root and that source/read-only roots are not accidentally treated as output roots.

## 17. Secrets and private endpoints

Secrets are never stored in repository configuration or hashed into public policy IDs.

API keys, tunnel tokens, credentials, and other secrets must come from protected environment/secret mechanisms available at deployment time.

Configuration may contain non-secret service coordinates when appropriate, but example configuration must use non-sensitive placeholders or loopback examples.

## 18. Configuration hashing

Do not hash one giant resolved runtime configuration and call it the processing identity.

Instead, each reproducibility-sensitive subsystem receives a canonical policy projection containing only fields that affect its output semantics.

Examples:

- `chunk_policy_hash` excludes source/output filesystem roots but includes segmentation parameters and algorithm version;
- `embedding_policy_hash` excludes checkpoint/log paths but includes model/revision/normalization settings;
- corpus-manifest policy includes schema/taxonomy/serialization rules but excludes the machine mount point;
- vector deployment host/port do not alter `chunk_id` or embedding build identity.

Policy projections must use canonical serialization before hashing.

## 19. Runtime/generated state

The following are not configuration authority and must remain outside canonical source:

- embedding checkpoint JSON;
- `.npy` embedding matrices;
- generated chunk files/records;
- Qdrant database state;
- audit output from real runs;
- logs;
- temporary manifests created during incomplete builds;
- caches and virtual environments.

Where such state needs durable provenance, it references canonical IDs/hashes defined by this contract.

## 20. Donor disposition consequences

This contract resolves how key recovered components must be adapted:

### R3 `hashing.py`

Retain BLAKE3 content/config/manifest hashing concepts. Reject path-derived `doc_id` as canonical identity. Path normalization remains a filesystem utility, not the identity algorithm.

### R3 `manifest_builder.py`

Manifest rows will use portable IDs and canonical record ordering rather than normalized absolute path as identity/order authority.

### R2 `chunk_chat_corpus.py`

Its relative-path ten-hex source token is historical traceability only. Canonical chunk IDs come from registered source/document/span/content/policy identity.

### R2 `create_embeddings.py`

The generator must consume an authoritative chunk manifest and produce an embedding manifest. Sorted filesystem enumeration is not the row contract.

### R2 Qdrant loader/query

Both must consume the same vector-payload contract and canonical `chunk_id`; neither may remap results by re-sorting local chunk files.

### R1 artifact lifecycle

Artifact paths become configured bounded locations; `artifact_id` is independent of staging/committed path. Content hash and audit events are separate metadata.

### R2 registry builder

Entity IDs become explicitly governed immutable registry keys rather than display-name slugs generated at runtime.

## 21. Decisions intentionally deferred

This contract does **not** yet decide:

- exact JSON Schema fields for chunk, artifact, entity, vector, or corpus records;
- the final ChatGPT JSON parser or importer implementation;
- exact message-span representation for every supported source format;
- whether generated chunks are stored as JSONL only, files plus manifest, or another representation;
- exact embedding-manifest file format;
- Qdrant collection migration procedure;
- artifact audit-event schema;
- registry authority-file format.

Those decisions belong to the next schema/manifest consolidation gate.

## 22. Acceptance gate

Portable identity and configuration are considered consolidated when subsequent canonical schemas and component promotions obey all of the following:

- no durable ID is based solely on an absolute machine path;
- source/document/chunk identity survives path moves;
- content hashes are distinct from logical identity where lifecycle semantics require it;
- manifests explicitly carry IDs rather than requiring filename inference;
- embedding rows explicitly bind to `chunk_id`;
- vector retrieval resolves by payload identity rather than filesystem order;
- artifact identity survives state/path transitions;
- entity identity survives alias/display-name changes;
- machine paths/services are configuration, not source constants;
- processing-policy hashes exclude machine-local placement values;
- secrets and mutable runtime state remain outside canonical Git source.

With this document committed, the next consolidation step is the **schema and manifest contract**. Canonical `src/` remains gated until those cross-module schemas are resolved.
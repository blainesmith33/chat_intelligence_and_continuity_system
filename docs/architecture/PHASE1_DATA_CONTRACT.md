# CICS Phase 1 Data Contract

Status: initial rebuild contract

## Storage boundary

CICS does not hard-code a physical deployment path.

Two absolute runtime roots are configured independently:

- `CICS_SOURCE_ROOT` — immutable source conversation archives
- `CICS_ROOT` — generated CICS pipeline state

The source archive is evidence and must not be modified by ingestion.

Generated data may include:

- normalized conversations
- import manifests
- chunks
- embeddings
- Qdrant persistence
- retrieval output
- runtime checkpoints

## Source identity

Source identity must survive:

- machine changes
- username changes
- mount-point changes
- repository relocation
- directory relocation

Therefore source identity must not be derived from an absolute path.

CICS v1 source IDs are derived from:

1. the identity-contract version
2. the source format
3. the immutable source bytes

BLAKE3 is used for source content hashing and source identity generation.

Filesystem paths remain provenance attributes, not identity.

## Conversation normalization

Normalized conversation records preserve, when available:

- original conversation ID
- original message ID
- source graph/node ID
- parent relationship
- role
- timestamp
- message content
- active-branch membership
- source import identity

No Phase 1 normalization operation may silently discard available provenance needed to reconnect normalized data to the original export.

## Paired exports

A readable Markdown export and its matching raw JSON export are two representations of one conversation.

They remain independently hashed source objects.

Their relationship is recorded explicitly rather than treating them as two unrelated conversations.

## Phase 1 boundary

Phase 1 performs:

1. source registration
2. normalization
3. language-aware semantic segmentation with structural preservation
4. embedding generation
5. Qdrant indexing
6. provenance-preserving retrieval

Phase 1 does not promote inferred:

- decisions
- tasks
- claims
- contradictions
- project identities
- architecture events

into authoritative structural records.

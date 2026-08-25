# CICS RAG Boundary Decision

Status: architectural boundary decision during repository reconstruction  
Prepared: 2026-08-25

## Decision

**CICS is a consumer of RAG capabilities. It is not the owner of the generic RAG implementation.**

CICS may define CICS-specific source semantics, policies, queries, and interpretation of retrieved evidence. Generic corpus processing, embeddings, vector-store persistence, and reusable retrieval infrastructure belong in a separate shared RAG system/repository that can serve CICS and other RAG-based projects.

This decision supersedes the earlier reconstruction assumption that all recovered R2/R3 RAG machinery should eventually be promoted into the CICS source tree merely because it was historically stored under CICS-related directories.

Historical filesystem location is evidence of lineage, not proof of correct architectural ownership.

## Why this boundary is required

Multiple projects use or have independently accumulated RAG machinery. Keeping generic RAG implementation inside CICS while also maintaining RAG code elsewhere would create duplicated ownership, divergent identity/manifest contracts, duplicated embedding/vector adapters, and repeated maintenance of the same infrastructure.

The intended system relationship is instead:

```text
                    Shared RAG System
              +---------------------------+
              | source/corpus manifests   |
              | generic chunk engine      |
              | embedding generation      |
              | embedding manifests       |
              | vector-store adapters     |
              | retrieval interface       |
              | deterministic validation  |
              | corpus/build auditing     |
              +-------------+-------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
      +-------------+              +----------------+
      |    CICS     |              | Engineering RAG|
      | consumer    |              | / other users  |
      +-------------+              +----------------+
```

CICS can therefore use RAG without being responsible for how generic RAG infrastructure is implemented.

## CICS owns

CICS remains responsible for domain behavior specific to conversation continuity and governed chat/project evidence, including:

- ChatGPT/export and conversation-source interpretation;
- normalized conversation/message semantics;
- preservation of roles, timestamps, branches, and source provenance meaningful to conversations;
- CICS-specific source registration requirements;
- CICS-specific chunking/retrieval **policy** where needed, but not the generic chunking/retrieval engine;
- construction of CICS queries and interpretation of retrieval results;
- decisions, reversals, tasks, claims, contradictions, timelines, and continuity logic;
- authoritative project/entity/alias rules where those rules are part of CICS continuity;
- artifact staging, approval/rejection, promotion, audit, and human governance;
- relationships between retrieved evidence and CICS records/artifacts.

## Shared RAG system owns

The shared RAG layer should own reusable infrastructure that is not specific to CICS semantics:

- generic source/corpus manifest mechanics;
- generic deterministic record ordering and manifest hashing;
- reusable content hashing/build identity utilities where appropriate;
- generic chunk execution framework;
- embedding generation and batching/checkpoint behavior;
- embedding manifests and row-to-record binding;
- vector-store interfaces;
- Qdrant adapter and collection build mechanics;
- shared vector payload/retrieval transport contract;
- generic similarity search/retrieval execution;
- corpus validation and deterministic rebuild verification;
- generic corpus/build audit receipts;
- reusable runtime-state separation rules for generated chunks, matrices, vector state, checkpoints, and logs.

The shared RAG project may accept domain-specific policies supplied by consumers such as CICS or Engineering RAG, but those policies do not transfer ownership of the generic engine back into the consumer.

## Interface principle

CICS should interact with RAG through a stable boundary rather than importing knowledge of a specific vector database or embedding implementation throughout CICS code.

Conceptually:

```text
CICS normalized evidence + CICS processing/retrieval policy
                         |
                         v
                 Shared RAG interface
                         |
             +-----------+-----------+
             |                       |
      build/index operation      retrieval query
             |                       |
             v                       v
      portable build receipt   retrieval results
                                 with durable IDs
             +-----------+-----------+
                         |
                         v
               CICS continuity logic
```

CICS should be able to change from one compliant RAG implementation/backend to another without rewriting conversation, continuity, registry, or artifact-governance logic.

## Current promoted files: transitional classification

Commit range `6e278cf..ff0d2f6` introduced the first canonical implementation foundation before this boundary was recognized. Those files are not to be deleted immediately. They must be classified and either retained in CICS or migrated to the shared RAG project after the other RAG repositories are inventoried.

### Clearly CICS-owned or CICS-facing

- `src/cics/config/` — CICS configuration remains valid, though shared-RAG configuration must later be separated from CICS settings.
- `schemas/message_record_v1.json` — conversation/message semantics are CICS-facing.
- `schemas/artifact_metadata_v1.json` — CICS artifact governance.
- `schemas/artifact_event_v1.json` — CICS artifact governance/audit.
- `schemas/entity_v1.json` — provisionally CICS-owned because it supports the authoritative project/entity continuity model; reassess only if a broader registry project owns this contract.

### Boundary-dependent / likely shared-RAG extraction candidates

- `src/cics/provenance/hashing.py`
- portions of `src/cics/provenance/identity.py`
- `schemas/source_record_v1.json`
- `schemas/document_record_v1.json` where the record is generic rather than conversation-specific
- `schemas/chunk_record_v1.json`
- `schemas/embedding_manifest_record_v1.json`
- `schemas/vector_payload_v1.json`
- corresponding generic tests

These are valid work, but their current location under `cics` does not establish final ownership.

### Do not promote next

Until shared-RAG ownership is resolved, **do not promote** the following recovered R2/R3 implementation families into CICS:

- R3 generic manifest builder;
- R3 generic metadata/schema validator;
- R3 generic determinism verifier;
- R3 generic corpus audit implementation;
- R3 generic corpus-layout controller;
- R2 embedding generator;
- R2 Qdrant loader;
- R2 generic retrieval execution;
- generic portions of R2 chat chunking that are reusable outside CICS.

Their recovery snapshots remain preserved evidence and must not be lost.

## R2/R3 reinterpretation

This boundary changes donor classification without changing historical evidence.

### R2

R2 contains both CICS-specific and generic RAG work. The historical chat chunker has CICS-specific source assumptions, while embedding generation, Qdrant loading, and retrieval mechanics are primarily generic RAG infrastructure.

### R3

R3 should no longer be treated as automatically CICS-owned. Its deterministic corpus-control work is predominantly a generic corpus/RAG foundation and is therefore a strong donor candidate for the future shared RAG system.

Its presence under a CICS-related historical directory is insufficient reason to vendor it into CICS.

## Required next reconstruction step

Before more RAG implementation is promoted anywhere:

1. inventory the user's existing RAG-related repositories/projects and recovered RAG lineages;
2. identify duplicate and complementary implementations;
3. establish one canonical shared RAG repository/project boundary;
4. classify recovered R1/R2/R3 and other RAG components by final owner;
5. move or reconstruct generic RAG contracts/implementation in that shared project;
6. replace CICS ownership of generic RAG internals with an explicit dependency/interface;
7. retain only CICS-specific adapters, policies, normalized conversation semantics, continuity logic, registry behavior, and artifact governance inside CICS.

## Reconstruction gate

No additional generic RAG implementation is to be added to CICS until the shared RAG project has been identified or established and the ownership matrix has been completed.

Existing recovery snapshots and the transitional `ff0d2f6` foundation remain intact while that determination is made.

The objective is not to make CICS independent of RAG. The objective is to make CICS **dependent on a reusable RAG capability without duplicating or owning that capability's implementation**.

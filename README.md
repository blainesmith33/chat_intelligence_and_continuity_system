# CICS — Chat Intelligence & Continuity System

CICS is a human-governed conversation intelligence and continuity system. Its purpose is to preserve, retrieve, relate, and evaluate evidence from long-running conversations so that project decisions, requirements, commitments, reversals, unresolved questions, and unfinished work can be recovered with their original context.

CICS is intended to support continuity across chats, models, machines, and workstreams without allowing generated summaries or model assumptions to silently become authoritative project state. It is a partially implemented project: historical prototypes demonstrated parts of the retrieval workflow, and the current repository contains a reconstruction and implementation foundation. It is not yet a complete, portable, end-to-end continuity platform.

## The problem CICS addresses

Long-running technical work becomes fragmented across conversations, handoffs, repositories, machines, and changing model context. Important decisions can be buried or lost; earlier proposals can be mistaken for current decisions; project names and boundaries can be conflated; and instructions or generated code can be reported as completed work without evidence.

CICS is intended to provide durable, local-first access to the underlying conversation evidence and then add continuity capabilities that distinguish:

- what a person explicitly decided;
- what an AI system proposed or inferred;
- what was actually implemented and supported by artifacts;
- what changed, was superseded, or remains unresolved.

The system must preserve provenance and uncertainty rather than manufacture a clean narrative when the source material is incomplete or contradictory.

## Core operating principles

- **Human authority:** the user retains decision-making authority. Models may retrieve, analyze, propose, implement under direction, and critique; they do not silently approve or redefine project state.
- **Evidence and provenance:** derived claims must remain traceable to source conversations, messages, files, or other evidence.
- **Explicit status:** proposals, plans, attempted actions, completed work, and verified results must not be conflated.
- **Contradictions are preserved:** reversals, disagreements, uncertainty, and conflicting historical accounts are evidence to retain and resolve—not noise to discard.
- **Project boundaries matter:** related projects may exchange evidence through defined interfaces without being collapsed into one system.
- **Local-first operation:** durable data and operational state should be under the user's control, with deployment paths and machine-specific details supplied through configuration.
- **Governed artifacts:** model-generated artifacts remain provisional until they pass the required human review and approval process.

## Intended knowledge domains

CICS work distinguishes three related but separate knowledge domains:

1. **Chat RAG:** conversation exports and their normalized conversation/message content. This is the source layer for recovering what was said, decided, proposed, questioned, and changed.
2. **Engineering RAG:** engineering documentation, code, technical references, and other domain-specific technical material. It provides technical evidence and is a separate corpus/system.
3. **Project and internal knowledge:** authoritative project identities, repository and filesystem facts, project relationships, governed decisions, and accepted artifacts. This layer supplies the authority and context needed to interpret retrieved material.

These domains may be linked where justified, but their records, authority, and corpus boundaries must remain explicit. A conversation mentioning a project is evidence about that project; it is not by itself authoritative proof of the project's identity, current implementation state, or ownership.

## Intended architecture and responsibilities

The intended CICS workflow is broader than vector search:

1. Preserve source exports and establish stable source identity.
2. Parse and normalize conversation data while retaining roles, timestamps, native identifiers, and source provenance where available.
3. Segment content deterministically, retaining references to the originating conversation and message spans.
4. Use shared RAG infrastructure to build indexes and retrieve relevant evidence.
5. Interpret retrieved conversation evidence for continuity: decisions and reversals, tasks and commitments, claims, contradictions, timelines, project identity, aliases, and unresolved work.
6. Relate conversation evidence to authoritative project/repository records and other approved knowledge.
7. Produce reviewable artifacts with explicit provenance and status.
8. Stage, review, approve or reject, and promote artifacts through a governed lifecycle.

### Shared RAG boundary

CICS is a **consumer of reusable RAG capabilities**, not the owner of the generic RAG engine. Generic corpus mechanics, chunk execution, embedding generation, vector-store adapters, retrieval execution, deterministic corpus validation, and reusable build auditing belong in a shared RAG system.

CICS owns its conversation-specific semantics, source interpretation, continuity logic, project/entity and alias rules, CICS-specific policies and queries, and artifact governance. It should interact with shared RAG through a stable interface and should not spread knowledge of a particular embedding model or vector database throughout its continuity logic.

The boundary decision is documented in [CICS_RAG_BOUNDARY_DECISION.md](docs/reconstruction/CICS_RAG_BOUNDARY_DECISION.md). Some hashing, identity, and schema files currently in this repository were introduced before that boundary was settled; their presence is transitional and does not establish final ownership.

### Project identity and registry

Project identity must be grounded in authoritative evidence such as the user's repository and filesystem organization and explicitly governed registry records. Conversation text, filename pattern matching, or model inference may provide clues, but must not independently establish project identity or merge projects. This distinction became important after earlier text-extraction experiments produced false positives.

### Human/local/cloud collaboration

The conversations describe a collaboration model in which the user directs the work, local AI supports retrieval and persistent context, and cloud AI contributes reasoning, synthesis, and implementation assistance. The intended interaction includes explicit handoffs, scoped responsibilities, reviewable outputs, and a human-controlled stop/approval point.

This is an architectural direction, not a claim that CICS currently operates an automated multi-model orchestrator. Historical collaboration relied substantially on manual or UI-mediated coordination. A complete automated collaboration loop and its integrations remain unimplemented.

## What currently exists in this repository

The current repository contains a reconstruction and foundation layer, including:

- **Configuration:** typed configuration models and a strict TOML loader in `src/cics/config/`. The loader requires an explicit configuration file or `CICS_CONFIG`, rejects unknown keys, and resolves relative paths against the configuration file rather than relying on hidden machine-specific defaults.
- **Provenance foundations:** BLAKE3 hashing, canonical JSON serialization, and namespaced identity helpers for sources, documents, messages, chunks, embeddings, artifacts, and governed entities in `src/cics/provenance/`.
- **Record contracts:** JSON Schemas for source, document, message, chunk, embedding-manifest, vector-payload, artifact-metadata, artifact-event, and entity records in `schemas/`.
- **Focused unit tests:** tests covering configuration behavior, selected identity properties, and schema-family validity in `tests/unit/`.
- **Reconstruction evidence:** project, architecture, implementation-status, evidence-index, and ownership-boundary documents in `docs/reconstruction/`.

These components establish useful contracts and foundations. They do not, by themselves, constitute an integrated ingestion, indexing, retrieval, continuity, or collaboration runtime. The generic RAG-related code and schemas currently present are also subject to the ownership review described above.

## Historical implementation evidence and limitations

The recovered conversations document several historical implementation efforts, including local chat parsing/chunking, embedding generation, Qdrant indexing and retrieval, engineering-corpus experiments, artifact-governance utilities, and deterministic corpus-control work. They also document changing corpus counts, integration defects, machine-specific paths, incomplete work, rejected approaches, and differences between intended architecture and delivered behavior.

Reported historical counts and demonstrations are tied to particular points in time and should not be treated as the current state of this checkout or as proof of a reproducible deployment. The reconstruction documents distinguish direct implementation evidence, user reports, architectural decisions, and unresolved claims.

The defensible status is:

**CICS is partially implemented across historical prototypes and a current reconstruction foundation.** The current repository does not yet demonstrate a fresh-machine, reproducible, end-to-end workflow that imports conversation exports, builds or consumes a shared index, retrieves evidence, performs continuity analysis, and produces governed project-state artifacts.

The presence of tests in the repository is not a claim that they have been executed successfully in the current environment. Consult the implementation-status and evidence-index documents for the latest documented evidence and limitations.

## Relationship to adjacent projects

- **Shared RAG system:** owns reusable corpus processing, embedding, vector-store, retrieval, and corpus-validation infrastructure. CICS is a consumer through a defined interface; the shared implementation and integration remain separate work.
- **Engineering RAG:** a separate technical knowledge corpus/system. It can provide technical evidence to CICS, but it is not a CICS subsystem and its corpus should not be absorbed into Chat RAG.
- **PEIS — Personal Engineering Intelligence System:** a separate governed engineering environment for planning, executing, evaluating, and improving technical work. CICS may provide continuity or knowledge services to PEIS through an explicit interface; a completed integration is not present here.
- **KGI:** a separate knowledge-governance initiative with conceptual overlap around authoritative records and evidence lifecycle. Ownership and integration should remain explicit rather than assumed.
- **Other projects discussed in conversations:** subjects represented in the evidence, not automatically CICS components.

## Current reconstruction priorities

The repository's reconstruction work identifies the following priorities:

1. Complete the inventory and ownership classification of historical RAG and CICS implementation lineages before promoting more generic RAG code into this repository.
2. Resolve and document canonical source, document, message, and chunk identity contracts, including which contracts belong to CICS versus shared RAG.
3. Define a portable conversation-import and normalization boundary that preserves source fidelity and provenance.
4. Establish the CICS interface to shared RAG without coupling continuity logic to a specific vector database or embedding implementation.
5. Build the authoritative project/entity registry and explicit alias/relationship rules.
6. Implement and validate continuity extraction for decisions, reversals, tasks, claims, contradictions, timelines, and unresolved work.
7. Complete artifact lifecycle and audit integration, including human approval and promotion controls.
8. Add integration tests, reproducible deployment instructions, backup/restore procedures, and end-to-end verification.

These are reconstruction and development priorities, not assertions that the capabilities are already implemented.

## Development and authorship context

The recovered records show the user defining project objectives, architecture boundaries, preservation requirements, machine roles, governance expectations, and acceptance criteria, while using AI systems extensively for implementation assistance, troubleshooting, analysis, and documentation. The records also show the user correcting project attribution, rejecting unsupported completion claims, and requiring evidence before historical work is treated as current capability.

This is best described as a human-directed, AI-assisted engineering effort. The repository should distinguish user-approved decisions from AI-generated proposals and should not imply that every implementation detail was independently authored by the user.

## Repository guide

- [Project reconstruction](docs/reconstruction/CICS_PROJECT_RECONSTRUCTION.md)
- [Architecture reconstruction](docs/reconstruction/CICS_ARCHITECTURE_RECONSTRUCTION.md)
- [Implementation status](docs/reconstruction/CICS_IMPLEMENTATION_STATUS.md)
- [Evidence index](docs/reconstruction/CICS_EVIDENCE_INDEX.md)
- [RAG ownership boundary](docs/reconstruction/CICS_RAG_BOUNDARY_DECISION.md)
- [Configuration implementation](src/cics/config/)
- [Provenance implementation](src/cics/provenance/)
- [Record schemas](schemas/)
- [Unit tests](tests/unit/)
- [Recovered conversation exports](extracted_chats/)

The `extracted_chats/` directory preserves the recovered Markdown exports and associated raw JSON archives used to reconstruct project intent, decisions, implementation history, and unresolved questions.
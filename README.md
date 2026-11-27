# CICS — Chat Intelligence & Continuity System

CICS is a project for preserving and retrieving evidence from conversations so that decisions, requirements, unfinished work, and project relationships can be reconstructed with their source context. Its intended role is conversation-specific continuity and project intelligence. CICS is not the generic RAG engine, and it is not currently a complete integrated collaboration platform.

## Why CICS exists

The project grew from Blaine’s work with large conversation and engineering corpora and the practical risk of losing project context across separate chats, machines, and workstreams. Blaine identified the need for local retrieval and continuity alongside human-directed AI collaboration. In the source conversations, Blaine also corrected cross-project contamination and rejected treating a gateway or a chat retrieval milestone as fulfillment of the larger intended interaction environment. [Source conversations are archived in `chat_archives/cics_raw_chats/`; see `CICS Project Index`, `Multi-AI Collaboration Setup`, `Hand-off Instructions and Scope`, and `Project Analysis Request`.]

## Intended architecture

The target CICS design separates:

1. Preserved conversation exports and source identity.
2. Conversation-aware parsing and normalization that retain roles, timestamps, and provenance.
3. Deterministic segmentation with stable references back to source messages.
4. Retrieval through a shared RAG capability.
5. CICS-specific continuity work such as project identity, decisions, reversals, tasks, claims, contradictions, and timelines.
6. Human review and governed artifact handling before derived material becomes accepted project state.

CICS is intended to consume reusable embedding, vector-store, and retrieval infrastructure. The separate [`retrieval_augmented_generation_system`](https://github.com/blainesmith33/retrieval_augmented_generation_system) repository currently documents this ownership boundary; it does not yet provide a shared implementation.

## What exists in this repository

The current checkout is a reconstruction and foundation, not a complete portable CICS runtime. It contains:

- Python configuration models and loading in `src/cics/config/`.
- Provenance identity and hashing foundations in `src/cics/provenance/`.
- Schemas for conversation, source, chunk, embedding, vector payload, entity, and governed artifact records in `schemas/`.
- Focused unit tests for configuration, identity, and schemas in `tests/unit/`.
- Historical reconstruction, evidence, status, and architecture-boundary documents in `docs/reconstruction/`.

The current code does not include a complete conversation-import/index/query pipeline, project-continuity engine, or integrated human/local-AI/cloud-AI collaboration loop.

## Historical demonstrations and limits

Earlier conversations record narrower operational milestones: 11,659 conversation chunks, a reported 11,659 × 768 embedding matrix, Qdrant indexing, and query output. They also record integration defects, incomplete corpus work, changing corpus counts, machine-specific paths, and a project-extraction approach that was rejected after producing false positives. Those historical results are not a claim that the current checkout can reproduce the full pipeline. See [`docs/reconstruction/CICS_IMPLEMENTATION_STATUS.md`](docs/reconstruction/CICS_IMPLEMENTATION_STATUS.md) and [`docs/reconstruction/CICS_EVIDENCE_INDEX.md`](docs/reconstruction/CICS_EVIDENCE_INDEX.md) for the evidence grades and known conflicts.

The strongest defensible overall description is **partially implemented across historical prototypes and a current reconstruction foundation**. A fresh-machine deployment, a canonical portable corpus, and an end-to-end continuity workflow are not demonstrated. No tests were run for this README review; test files are present, but this review does not claim a passing current test result.

## Design direction and AI-assisted development

Blaine set the project objectives, cross-project boundaries, preservation constraints, machine-role requirements, and the desired role of local retrieval in a human-controlled collaboration environment. The raw records show him correcting wrong project attribution, rejecting unapproved deletion of prior retrieval work, and identifying when a delivered interface did not satisfy the intended behavior. ChatGPT and coding agents supplied substantial implementation assistance, technical explanations, troubleshooting, and documentation. The available evidence supports human project and design authority with extensive AI-assisted implementation; it does not establish independent authorship of every technical detail or source line.

## Relationship to adjacent projects

- **Shared RAG system:** intended owner of generic corpus, embedding, vector-store, and retrieval machinery. The repository is currently documentation and reconstruction work.
- **Engineering RAG Corpus:** a separate domain-specific corpus and source-governance effort. Historical CICS conversations document its origins; they do not make Engineering RAG a CICS subsystem today.
- **PEIS:** a related but separate governed planning/execution system. No completed CICS-to-PEIS integration is present.
- **KGI:** a separate evidence lifecycle and knowledge-governance project. CICS may consume governed evidence in the future; the integration is not implemented here.

## Current priorities and open work

The reconstruction documents call for selecting and classifying historical donor code, resolving stable source and chunk identity, defining a portable import contract, and keeping generic RAG ownership outside CICS. Continuity extraction, project registry behavior, governed retrieval, backup/restore, and automated collaboration remain future work. These are plans, not current capabilities.

## References

- [`docs/reconstruction/CICS_PROJECT_RECONSTRUCTION.md`](docs/reconstruction/CICS_PROJECT_RECONSTRUCTION.md)
- [`docs/reconstruction/CICS_ARCHITECTURE_RECONSTRUCTION.md`](docs/reconstruction/CICS_ARCHITECTURE_RECONSTRUCTION.md)
- [`docs/reconstruction/CICS_IMPLEMENTATION_STATUS.md`](docs/reconstruction/CICS_IMPLEMENTATION_STATUS.md)
- [`docs/reconstruction/CICS_RAG_BOUNDARY_DECISION.md`](docs/reconstruction/CICS_RAG_BOUNDARY_DECISION.md)
- [`src/cics/`](src/cics/), [`schemas/`](schemas/), [`tests/unit/`](tests/unit/)

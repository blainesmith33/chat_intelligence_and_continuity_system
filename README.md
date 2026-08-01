# CICS — Chat Intelligence & Continuity System

CICS is a local, retrieval-backed intelligence system that turns accumulated AI conversations into structured, searchable, and traceable project knowledge.

Its purpose is not merely to archive chats or provide semantic search. CICS is being developed to preserve long-term continuity across conversations, recover authoritative decisions, identify unfinished work, organize related projects, and produce evidence-backed project intelligence from material that would otherwise remain scattered across isolated chat histories.

> **Project status:** The foundational retrieval pipeline is operational. The higher-level authority, interpretation, governance, and artifact-generation layers remain under development.

## Why CICS Exists

Long-running AI-assisted projects generate valuable information across many separate conversations:

- Requirements and constraints
- Design and architecture decisions
- Naming changes and project relationships
- Completed implementation work
- Rejected or superseded approaches
- Open questions and unfinished tasks
- Explanations that were never converted into formal documentation

Conventional chat history preserves the transcripts, but not the coherent project state contained within them. As the number and complexity of conversations grow, manually reconstructing that state becomes increasingly unreliable.

CICS externalizes this knowledge into a locally controlled system:

```text
Chat history
    ↓
Normalized corpus
    ↓
Traceable retrieval evidence
    ↓
Authoritative project interpretation
    ↓
Continuity, comparison, planning, and artifacts
```

The long-term goal is a persistent AI-assisted thinking environment that can explain not only what was said, but what was decided, what remains true, how projects relate, and what should happen next.

## Core Capabilities

### Semantic chat retrieval

CICS imports conversation records, normalizes their contents, divides them into retrievable chunks, generates vector embeddings, and indexes them in Qdrant.

This allows conceptually related information to be found even when a query does not repeat the original wording. Intended queries include:

- Where did this architecture change?
- What decisions were made about a particular subsystem?
- Which conversations discuss this project?
- What unfinished work remains?
- When was this project renamed?

### Provenance-preserving evidence

CICS is designed to keep retrieved claims traceable to their origin:

```text
Retrieval result → chunk → source file → corpus section → project or conversation
```

The indexed metadata is intended to preserve fields such as the source identifier, source file, corpus section, language, chunk index, embedding-row index, chunk path, and original chunk text.

This provenance layer is essential to the project. CICS is intended to produce conclusions supported by inspectable evidence rather than plausible but untraceable summaries.

### Cross-chat continuity

CICS is intended to reconstruct the state that should carry forward between conversations:

- Authoritative decisions
- Completed work
- Current work in progress
- Known constraints
- Rejected approaches
- Open questions
- Required next steps

This provides a foundation for reliable handoffs without repeatedly rebuilding project context by hand.

### Structured project intelligence

The system is being designed to transform conversational evidence into structured records describing:

- Formal projects and candidate ideas
- Canonical names and aliases
- Parent, child, and related projects
- Shared infrastructure and dependencies
- Project status and implementation progress
- Decisions, revisions, and reversals
- Supporting evidence

### Artifact generation

Planned outputs include:

- Project summaries
- Architecture descriptions
- Decision records
- Handoff documents
- Task and status inventories
- Project registries
- Dependency maps
- Prioritized roadmaps
- Governance records

### Communication analysis

CICS is also intended to identify recurring problems in human–AI collaboration, including context loss, ambiguous instructions, unstable handoffs, repeated explanations, incorrect assumptions, and architecture drift.

The goal is to improve both project continuity and the quality of the working relationship between a person and an AI system.

## System Architecture

CICS was designed as a two-node local system with responsibilities divided between an interactive node and a retrieval node.

### Interactive and preprocessing node

The interactive node is responsible for:

- User-facing local AI interaction
- Chat ingestion
- Text normalization
- Chunk generation
- Metadata preparation
- Retrieval requests
- Context-aware response generation

### Retrieval and knowledge node

The retrieval node is responsible for:

- Embedding generation
- Qdrant vector storage
- Vector indexing
- Semantic retrieval
- Archive-analysis workloads
- Supporting local inference tasks

The architecture is local-first so that the project corpus, derived embeddings, retrieval database, and project intelligence can remain under the operator's control.

## Data Pipeline

```text
Raw conversation files
    ↓
Normalization and language detection
    ↓
Deterministic chunk generation
    ↓
Embedding generation
    ↓
Qdrant ingestion
    ↓
Semantic retrieval with source provenance
```

### Chunk generation

The recorded chunking pipeline:

- Recursively processes text sources
- Normalizes line endings and whitespace
- Separates ordinary text from fenced code
- Classifies English, Python, Bash, JSON, configuration, and other content
- Uses deterministic traversal and stable filenames
- Organizes output by corpus section and language
- Adds overlap between adjacent chunks to preserve context

Recorded chunk settings:

| Content type | Target size | Overlap |
|---|---:|---:|
| English text | 4,000 characters | 500 characters |
| Code and configuration | 2,500 characters | 250 characters |

### Embedding generation

The embedding pipeline includes:

- Deterministic chunk ordering
- Sentence-transformers support
- `nomic-ai/nomic-embed-text-v1.5`
- 768-dimensional embeddings
- Memory-mapped NumPy output
- Checkpoint and resume support
- Atomic checkpoint writes
- Configurable paths and expected chunk counts
- Automatic batch-size reduction under memory pressure
- Validation before resuming an interrupted run

### Qdrant indexing

The hardened ingestion design enforces a one-to-one relationship between chunk files and embedding rows. Each vector is paired with sufficient payload metadata to reconnect a retrieval result to its source material.

The working collection is recorded as `chat_rag`.

## Current Implementation Status

The latest recorded full-corpus milestone reported:

| Stage | Result |
|---|---:|
| Source files processed | 194 |
| Chunks generated | 13,600 |
| Embedding matrix | 13,600 × 768 |
| Qdrant indexing | Complete |
| Metadata preservation | Verified in the deployed pipeline |
| Vector-to-source traceability | Verified in the deployed pipeline |

These figures represent the recorded development corpus and are not general requirements for running CICS with another dataset.

### Implemented foundation

- Two-node system architecture
- Raw conversation corpus organization
- Deterministic, language-aware chunking
- Recoverable embedding generation
- Qdrant vector indexing
- Metadata-rich retrieval payloads
- Traceability from vector result to source material
- Completed full-corpus indexing run

### Partially implemented or under development

- Authoritative project registry
- Canonical identity and alias resolution
- Governed query framework
- Project-family and dependency analysis
- Cross-project comparison
- Artifact generation
- Communication-pattern analysis
- User-facing bridge between the local system components

### Not yet demonstrated as complete

- Verified final authoritative-registry build
- Reliable project counting from that registry
- Formal retrieval-quality test suite
- Completed project deduplication and relationship engine
- Reliable infrastructure comparison across projects
- Categorization and priority scoring
- Automated roadmap generation
- Automated ChatGPT export ingestion
- End-to-end question answering through a unified CICS interface

## Authority and Trust Model

An early extraction approach attempted to discover projects through broad textual patterns such as references to a “project,” “system,” “platform,” or “framework.” This produced thousands of false project candidates because conversational mentions, subsystem names, headings, and general concepts were incorrectly promoted into project identities.

That failure led to a central architectural principle:

> Retrieval evidence should explain and support authoritative project structure; it should not invent that structure from textual similarity alone.

CICS therefore uses the following trust hierarchy:

1. **Authoritative structure** — registries, known folders, charters, mappings, canonical names, and explicit aliases define project identity.
2. **Retrieval evidence** — conversation chunks provide history, explanation, context, and supporting evidence.
3. **Governed interpretation** — reasoning operations compare, group, trace, summarize, and report information according to the correct source of truth.

Different questions require different primary authorities:

| Question | Primary authority | Role of retrieval |
|---|---|---|
| How many projects exist? | Project registry | Supporting explanation |
| What was decided about a project? | Conversation evidence | Primary evidence source |
| Which projects share infrastructure? | Registry plus relationship rules | Gather and compare evidence |
| Which ideas were abandoned? | Conversation evidence plus status rules | Primary evidence source |
| Is one name an alias of another? | Canonical registry and alias mappings | Supporting history |

## Repository Reconciliation

The existing project materials contain both standalone script snapshots and implementation records. Some snapshots do not reflect the latest reported deployed versions.

Known reconciliation work includes:

- Replacing the early Qdrant loader snapshot, which stored only a numeric chunk identifier, with the later provenance-rich loader
- Verifying the final authoritative-registry implementation and its output
- Reconciling machine-specific script copies with the repository versions
- Removing or consolidating duplicate archived project files
- Converting path-encoded chunk metadata into a more explicit structured format where appropriate

Until that work is complete, this repository should be treated as the beginning of the canonical CICS source tree rather than a fully reproducible release.

## Development Priorities

The next major milestones are:

1. Reconcile the verified live pipeline with the repository source files.
2. Complete and validate the authoritative project registry.
3. Add repeatable ingestion, indexing, and retrieval tests.
4. Implement governed query routing based on the authority model.
5. Build project identity, alias, relationship, and status resolution.
6. Generate evidence-backed continuity and project artifacts.
7. Expose the complete workflow through a unified local interface.

## Guiding Principles

- **Local control:** Project knowledge and derived intelligence should remain under the operator's control.
- **Evidence before claims:** Important conclusions should be traceable to their sources.
- **Authority before inference:** Explicit project structure outranks probabilistic textual interpretation.
- **Deterministic processing:** Repeated runs over the same inputs should produce stable outputs.
- **Recoverable workflows:** Long-running processing should checkpoint and resume safely.
- **Human governance:** Automated interpretation and action should remain inspectable and subject to human authorization.

## Project Maturity

CICS is not merely conceptual: its core conversation-processing, embedding, vector-indexing, and provenance pipeline has been built and used on a substantial corpus.

It is also not yet a finished platform. The next phase is the layer that turns retrieval evidence into consistently correct, authority-aware conclusions and useful project artifacts. That interpretation and governance layer is what will ultimately transform CICS from a searchable conversation archive into a dependable continuity and project-intelligence system.

## License

No license has been assigned yet. Until a license is added, all rights are reserved by the project owner.

# CICS Project Reconstruction

Status: evidence-recovery first pass; not canonical documentation  
Evidence notation: see [CICS_EVIDENCE_INDEX.md](CICS_EVIDENCE_INDEX.md)

## Reconstructed identity

CICS is the **Chat Intelligence & Continuity System**: a local-first, provenance-preserving system for turning exported human/AI conversations into searchable evidence and, eventually, governed project continuity. Its initial approved Phase 1 was deliberately narrower: import chat text/Markdown, normalize it, chunk it, embed it, store vectors in Qdrant, retrieve relevant passages, and interact with it from the Steam Deck. Decisions, tasks, claims, contradictions, timelines, and knowledge-graph features were explicitly deferred beyond Phase 1. [UD: E01, E02]

The later conversations broadened the intended outcome. CICS should recover decisions and reversals, maintain aliases and project identity, identify unfinished work, preserve relationships without collapsing project boundaries, support communication-drift analysis, and turn model outputs into reviewable artifacts. Those capabilities are an evolved target, not evidence that Phase 1 implemented them. [UD/AP: E08, E10, E11, E14-E16, E24-E26]

## Problem CICS was created to solve

Long-running ChatGPT work had become fragmented across chats, handoffs, machines, filenames, aliases, and model context windows. Important decisions could be buried, repeated, contradicted, or lost; generated implementation instructions could be mistaken for completed work; and new chats could not reliably distinguish current authority from stale proposals. CICS was intended to provide durable local recall with source traceability, then add governance so retrieved evidence and generated artifacts could be reviewed rather than silently becoming truth. [UD: E01-E03, E08, E10, E14-E16, E25-E26]

## Intended boundaries

### In scope

- Ingest immutable chat exports while preserving source identity and provenance.
- Normalize and segment chats deterministically, with enough metadata to trace a result to source conversation/message or source file.
- Create embeddings, index them, retrieve results, and expose them to a local interactive client.
- Maintain a governed artifact lifecycle: generated content enters staging, is approved or rejected, and only then may be promoted.
- Maintain authoritative project/alias registries based on folder and repository evidence, with chat text used as evidence rather than as the authority for project identity.
- Support a human/local-model/cloud-model collaboration protocol, with the user retaining final authority.
- Eventually extract decisions, claims, tasks, contradictions, temporal change, and cross-project relationships. [UD: E02-E03, E09-E11, E14-E16, E25-E26]

### Out of scope or separately bounded

- Raw chat archives, corpora, embeddings, vector-database state, virtual environments, model weights, caches, and acquired third-party repositories are runtime/evidence assets, not files to vendor into the CICS Git repository. [H supported by E04-E07, E12-E23 and repository forensics R1-R5]
- **PEIS** is a separate project. The chats sometimes describe CICS as the knowledge substrate beneath a future PEIS reasoning/orchestration layer; this is a dependency/relationship, not permission to merge PEIS into CICS. [UD: E14, E20-E24; current repository boundary]
- **Engineering RAG** evolved from the early “Coding RAG” validation corpus into a larger domain-aware knowledge system. It can supply CICS retrieval and taxonomy, but its huge source corpus and independent implementation concerns are not automatically CICS-owned. [UD: E12-E23; R4-R5]
- **KGI** overlaps conceptually around authoritative registries and governed knowledge, but the evidence does not settle ownership of that overlap. Keep it external pending an explicit interface decision. [UQ: E14-E16, E24, E28]
- Other projects mentioned or ingested in chats are evidence subjects, not CICS subsystems.

## Evolution of the concept

1. **Index and Phase 1 definition.** CICS began as a searchable local chat archive. The user explicitly deferred higher-order intelligence features. [UD: E01-E03]
2. **RAG-node implementation.** XPS became the active data/vector node; a coding corpus was used to exercise chunking, embeddings, and Qdrant before/alongside chat retrieval. [CI/RT: E04-E07, E12]
3. **Collaboration and governance.** Work expanded to local/cloud model roles, Open WebUI, artifact staging/approval, and machine-role policy. Much of the model orchestration remained manual. [CI/UD: E08-E11]
4. **Knowledge-infrastructure expansion.** Coding RAG was judged transitional and broadened into Engineering RAG with domain/authority classification and deterministic control tooling. Chat and Engineering corpora were to remain separate but linkable. [UD/CI: E12-E23]
5. **Registry pivot.** Text-regex project extraction produced false positives. The architecture pivoted to an authoritative filesystem/repository registry, using RAG results only as supporting evidence. [RJ/UD: E15-E16]
6. **Future orchestration protocol.** The user specified a bounded user/local/cloud interaction sequence and a file-output contract. It was designed, not shown operating end to end. [UD: E25-E27]
7. **August retrospective.** A later analysis described a 194-source/13,600-chunk chat state and broader ambitions. That is a reported later state, not independently verified in recovered runtime. [RT/UQ: E28]

## Reconstructed product principles

- **Provenance before fluency:** a retrieved or extracted claim must remain traceable to its source.
- **Authority is explicit:** user decisions outrank assistant proposals; folder/repository evidence outranks text inference for project identity.
- **Contradictions are data:** preserve reversals and unresolved conflicts instead of choosing a convenient narrative.
- **Runtime data is separable:** code/config/schema/manifests belong in Git; source corpora and generated state live externally through portable configuration.
- **Human governance is mandatory:** models may retrieve, propose, refine, or critique; the user retains approval and a stop condition.
- **Determinism matters:** stable ordering, hashing, manifests, dimension checks, and rebuildability were recurring requirements, even though implementations did not consistently meet the originally specified identity model. [UD: E02-E03, E09-E11, E14-E16, E25-E26]

## What CICS is not

- It is not merely a Qdrant collection or a single RAG script.
- It is not the Engineering RAG corpus.
- It is not PEIS, a generic multi-agent framework, or the collection of every project discussed in the chats.
- It is not demonstrated to be a self-optimizing autonomous system. That phrase appears as an aspirational design; no end-to-end autonomous feedback loop is evidenced. [AP/UQ: E24-E27]
- It is not demonstrated to have had a working automated multi-model orchestrator. The surviving evidence supports manual/UI-mediated collaboration plus isolated governance utilities. [CI/H: E08-E11, E25-E28, R1]

## Reconstructed current state in one sentence

CICS is a partially implemented prototype whose chat retrieval pipeline and artifact-governance utilities reached isolated milestones, whose corpus-control layer reached synthetic tests, but whose portable repository, authoritative metadata/provenance model, registry, orchestration, integration tests, and reproducible end-to-end deployment remain unfinished.

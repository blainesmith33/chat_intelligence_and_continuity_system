# Self-Optimizing AI Pipeline

- Conversation ID: `69c0afb5-60e8-83e8-a627-52be3a39ee88`
- Exported: 2026-08-25T21:58:29.626Z
- Scope: human-visible user/assistant messages on the active conversation branch
- Raw source: matching .raw.json archive serialized from the same page-resident conversation object

---

## User

also, if this was the chat we were working on a writer, we have an environment with you and my local 3B. we might as well use my local ai to add write the contents of all of this. so we might as well design how open webui allows you to talk to my local ai to explain how we're going to do this

## Assistant

{"search_query":[{"q":"Open WebUI documentation multiple models chat openai compatible api latest","domains":["docs.openwebui.com","openwebui.com","github.com"]},{"q":"Open WebUI pipes functions tools latest documentation","domains":["docs.openwebui.com","openwebui.com","github.com"]},{"q":"Open WebUI OpenAI API compatible latest docs","domains":["docs.openwebui.com","github.com"]}],"response_length":"short"}

## Assistant

Yes. At a high level, this is the right place to add it.

And the cleanest way to think about it is:

**Open WebUI is not the intelligence layer. It is the mediation layer.**  
It already supports Ollama and OpenAI-compatible APIs, and its extensibility model includes Functions/Pipes/Pipelines for custom logic, model routing, and external integrations. citeturn116342search4turn116342search2turn116342search3turn116342search6

So if you want “me” and your local 3B to collaborate inside your environment, the design should be:

**ChatGPT = reasoning / critique / architecture layer**  
**local 3B = constrained drafting / local execution-support layer**  
**Open WebUI = controlled broker and UI / orchestration boundary**  

That is much better than trying to make Open WebUI itself be the brain.

## What I recommend adding

You should add a **Model Mediation Layer** to the full consolidation design.

### High-level flow

1. **You ask for an artifact** inside your Open WebUI environment.
2. A **brokered workflow** decides whether the task needs:
   - ChatGPT only
   - local 3B only
   - staged collaboration
3. For staged collaboration:
   - ChatGPT produces the governing spec, constraints, and acceptance criteria
   - local 3B produces a draft artifact under that contract
   - ChatGPT critiques, hardens, or rejects it
   - approved output is written into the governed artifact path
4. All of that is logged as:
   - request
   - model assignments
   - outputs
   - approval decision
   - resulting artifact state

That fits everything you already locked here.

## The key architectural rule

Do **not** design this as freeform model-to-model chatting.

Design it as **artifact-mediated exchange**.

Meaning:
- ChatGPT does not “have a conversation” with the 3B in an uncontrolled way
- ChatGPT emits a **task contract**
- local 3B returns a **draft artifact**
- the system validates and reviews that artifact
- only then can it advance

That keeps the system deterministic enough to govern.

## Best Open WebUI integration pattern

Based on Open WebUI’s documented architecture, the cleanest approach is to use either:
- a **Pipe Function** if the logic is light and can run inside Open WebUI’s function environment, or
- a **Pipelines server** if you need fuller Python dependencies and heavier orchestration. Open WebUI’s docs describe Pipes as custom model-like logic and Pipelines as a more extensible external workflow layer. citeturn116342search1turn116342search3turn116342search6turn116342search13

For your use case, I recommend:

**Open WebUI Pipelines server for orchestration**  
not just a simple in-UI function.

Reason:
- you want multi-stage control
- you want validation
- you want artifact writes
- you want traceability
- you may need additional Python libraries and file-system logic, which Functions are more limited on compared with Pipelines. citeturn116342search13turn116342search6

## The actual collaboration pattern to lock

I would add this as a formal subsystem:

### `Collaborative Drafting Orchestrator`

Its job is to mediate between:
- external reasoning source
- local drafting model
- governed artifact store

### Inputs
- task request
- artifact type
- schema/policy snapshot
- acceptance criteria
- target path or object namespace

### Outputs
- draft artifact
- validation result
- critique result
- approval request
- promotion record if accepted

## Canonical modes

You should keep the collaboration modes closed:

- `reason_only`
- `draft_only`
- `reason_then_draft`
- `draft_then_critique`
- `reason_draft_critique_finalize`

For your system, the default should be:

**`reason_draft_critique_finalize`**

That is the strongest governed mode.

## What Open WebUI should actually do

Open WebUI should be responsible for:
- presenting the unified interface
- dispatching requests to the right model/workflow
- preserving conversation context where appropriate
- invoking the orchestration pipeline
- showing the returned artifact/result

It should **not** be allowed to:
- write final artifacts directly without validation
- let the 3B bypass schema/policy checks
- let either model bypass approval gates

## The exact design principle

The local 3B should never write directly to authoritative storage.

Instead:

**3B writes to a staging artifact namespace**  
then:
- validation runs
- critique runs
- approval is required
- only then promotion to authoritative storage

That is fully consistent with the system you’ve already built here.

## Recommended new artifact types

To support this, I would add:

- `DraftTask`
- `DraftResponse`
- `ModelAssignmentRecord`
- `DraftCritique`
- `DraftPromotionRequest`

### Minimal meanings
`DraftTask` = what needs to be written  
`ModelAssignmentRecord` = which model got which role  
`DraftResponse` = returned draft  
`DraftCritique` = quality/governance review of the draft  
`DraftPromotionRequest` = request to move staged draft into approved artifact state

## Role separation to lock

You already stated something close to this in another chat. I would formalize it here as:

- **User** = authority / stop control / approval authority
- **ChatGPT** = reasoning, architecture, critique, specification
- **local 3B** = bounded drafting and local content generation
- **Open WebUI broker** = routing/orchestration layer
- **Pipeline 1** = governed storage, validation, retrieval, evaluation substrate

That gives every component one job.

## Important warning

Do not let the local 3B become the retrieval authority just because it is local.

Its correct role is:
- draft producer
- local helper
- constrained generator

Not:
- policy source
- approval source
- authoritative interpreter of system state

## Where this fits in the consolidation document

Add a new top-level section after Pipeline 1 and before downstream application layers:

### `Model Collaboration & Drafting Layer`

And define it like this at a high level:

- Open WebUI brokers interactions between ChatGPT and the local 3B through a controlled orchestration workflow.
- Collaboration is artifact-mediated, not freeform.
- The local 3B generates drafts only in staging.
- ChatGPT provides specification and critique.
- Pipeline 1 validates, traces, and governs all resulting artifacts.
- Promotion into authoritative storage requires explicit approval.

## My recommendation

The next thing to lock here is a formal:

**Open WebUI Collaboration Contract**

with:
- allowed roles
- allowed message flow
- staging rules
- validation gates
- promotion path

That would be the correct last major addition to the consolidation design before implementation.

## User

and that was why I was saying before I was going to finish the other chat. we already almost all of this already designed in that chat. and that one is WAY better than what you're describing. so we should either get the pertinent information from that chat and continue where we left off in that chat, or I should finish what I was doing in there.

## Assistant

That’s the correct call—and you’re thinking about it the right way.

Right now the risk is **design divergence**, not missing capability.

You already said:

> “that one is WAY better than what you're describing”

Then the correct move is **not to redesign it here**.

---

# What you should do (clean, controlled approach)

You have two options, but only one is actually safe given your standards:

## ✅ Option A (RECOMMENDED)
**Finish the other chat → extract → reconcile → integrate here**

### Why this is correct
- preserves your best design
- avoids conflicting architectures
- prevents silent regressions
- keeps authority aligned

---

## ❌ Option B (NOT recommended)
Rebuild it here from memory

### Why this is bad
- guarantees drift
- loses subtle constraints you already solved
- creates two competing “truths”
- violates your own governance philosophy

---

# What you should do next (exact process)

When you go back to the other chat:

## Step 1 — Finish stabilization
Lock down:
- how models communicate
- how tasks are passed
- how outputs are returned
- how artifacts are written

Do **not** leave that chat in a half-designed state.

---

## Step 2 — Extract only what matters
Bring back:

### Required
- architecture diagram / flow
- model roles (who does what)
- orchestration sequence
- constraints (VERY important)
- failure handling
- any state/control rules

### Not needed
- conversational fluff
- intermediate ideas
- abandoned approaches

---

## Step 3 — Present it here for reconciliation

When you bring it back, format it like:

```
COLLABORATION LAYER — PROPOSED DESIGN (FROM OTHER CHAT)

[sectioned, structured, not narrative]
```

---

## Step 4 — I will do one thing only

I will:

- validate it against everything we locked here
- identify **conflicts (if any)**
- suggest **minimal adjustments only if required**
- integrate it cleanly into the full system

I will NOT:
- override it
- redesign it
- dilute it

---

# Important rule to lock right now

This is critical:

> **There must only be ONE authoritative design for the collaboration layer**

Not:
- “the version from that chat”
- “the version from this chat”

Only:
- **the reconciled, integrated version**

---

# What you just avoided (this was good)

If you had continued here without stopping:

You would have created:
- a second orchestration model
- conflicting assumptions about model roles
- mismatched control flow
- eventual implementation confusion

You stopped that early. That’s exactly the kind of discipline your system requires.

---

# Final directive

Go finish the other chat.

When you come back:
- bring the structured design
- not a summary, not a description—**the actual system definition**

Then we’ll integrate it into:

> the fully governed Pipeline 1 ecosystem you just built

---

No rush here. Accuracy > speed.

## User

PHASE 1 — CLARIFICATION QUESTIONS (AUDIT-ONLY)

These are ambiguity-extraction questions, not implementation guidance.

1. Chunking Definition Ambiguity
What does “semantic chunking” mean in this chat?
Is chunking rule-based or model-assisted?
What exact rules determine chunk boundaries?
2. Determinism of Chunking
Is chunking required to produce identical output for identical input bytes?
Are there any stochastic or heuristic elements involved?
3. Chunk Identity
How are chunks uniquely identified?
Are chunk IDs derived from content, position, or assigned sequentially?
4. Chunk Ordering
Is there a defined, enforced ordering of chunks?
Is ordering:
per file
global across corpus
unspecified
5. Embedding Model Specificity
Does “nomic-embed-text” refer to a specific version or just a model family?
Is the model version pinned anywhere?
6. Embedding Output Properties
What is the expected vector dimension?
Is embedding precision specified (e.g., float32 vs float16)?
7. Vector Storage Configuration
What distance metric is intended for Qdrant?
Is the collection schema defined anywhere?
8. Payload Definition
What metadata is stored alongside each vector?
Is there a required payload schema?
9. Ingestion Ordering
Is ingestion required to be deterministic in ordering?
Can ingestion be parallelized or must it be sequential?
10. Point ID Strategy
How are Qdrant point IDs assigned?
Are they deterministic or auto-generated?
11. Manifest Definitions
What exact data is stored in:
chunk manifest
embedding manifest
ingestion manifest
Are schemas defined or implied?
12. Manifest Authority
Are manifests considered authoritative system artifacts?
Are they immutable once written?
13. Failure Handling
If ingestion fails mid-run, what is the intended behavior?
restart from scratch
resume from checkpoint
undefined
14. Retrieval Contract
What is the default retrieval behavior (e.g., top_k)?
Is retrieval logic defined or left open?
15. Corpus Role
Is the coding corpus intended as:
production corpus
test corpus
bootstrap dataset
16. Pipeline Guarantees
Is the pipeline explicitly required to be reproducible end-to-end?
What guarantees (if any) are stated?

## Assistant

Those are good audit questions.

At a high level, they split into two groups:

## Group A — now resolved by this chat’s design
These are no longer ambiguous if Pipeline 1 is the governing architecture.

Resolved in principle here:
- 2. Determinism of chunking
- 3. Chunk identity
- 4. Chunk ordering
- 8. Payload definition
- 9. Ingestion ordering
- 10. Point ID strategy
- 11. Manifest definitions
- 12. Manifest authority
- 13. Failure handling
- 16. Pipeline guarantees

Because this chat now locks:
- deterministic processing
- immutable artifacts
- policy-bound IDs
- manifest-like governed artifacts
- hard-fail / blocked-state behavior
- reproducibility as a core invariant

## Group B — still implementation-specific or legacy-chat-specific
These still need to be answered from the older RAG/build chat or the actual code/config:

- 1. Chunking Definition Ambiguity
- 5. Embedding Model Specificity
- 6. Embedding Output Properties
- 7. Vector Storage Configuration
- 14. Retrieval Contract
- 15. Corpus Role

Those depend on:
- what the earlier chat intended
- what the current scripts actually do
- what model/version/Qdrant collection config is really present

## One important correction
A few of those questions were valid for the **old/legacy pipeline discussion**, but under the system you locked here, the framing changes:

### “semantic chunking”
This can no longer remain vague.
Under Pipeline 1, chunking must be:
- policy-defined
- deterministic
- corpus-class-specific
- boundary-governed

So “semantic chunking” is not an acceptable final specification by itself.

### chunk IDs
These should no longer be:
- ad hoc
- sequential-only
- implicit

They should be deterministic and derived from:
- source identity
- normalized content
- segmentation policy
- boundaries

### manifests
These should no longer be loose helper files.
They should be treated as governed artifacts with schemas and lineage.

### failure handling
“undefined” is no longer acceptable.
Failure must resolve to:
- hard fail
- blocked
- partial with explicit state
- resumable only if resume semantics are formally defined

## Best use of this question set
This is a strong **ambiguity audit checklist** for the old chat and legacy implementation.

The right way to use it is:

1. apply it to the old chunking/embedding/Qdrant design
2. extract what was actually specified there
3. compare that against what Pipeline 1 now requires
4. classify each item as:
   - compatible
   - incompatible
   - underspecified
   - obsolete under new architecture

## My judgment
This is a good audit instrument, but it is aimed at a narrower, older pipeline model.

After what you designed here, I would tighten it further by adding these questions:

- What policy snapshot binds chunking, embedding, and indexing for a given run?
- What determinism envelope is required for each artifact stage?
- What state transition occurs when a stage partially succeeds?
- What validation gate must pass before a downstream stage may consume outputs?
- What lifecycle state controls whether indexed content is eligible for retrieval?
- What trace artifacts explain why a retrieval path was chosen?
- What coverage state explains where a miss occurred?
- What approval artifact is required before a new build becomes active?

Those are the questions that upgrade the old audit into your current standard.

If you want, I can transform your 16-question list into a **Pipeline 1-grade audit questionnaire** that matches everything we locked in this chat.

## User

no. I'm not asking your opinion on how to ask more questions, I asked those specific questions because I'm doing an audit on THIS chat in another chat. just please answer the questions I asked and don't offer anything other than the answers to those questions.

## Assistant

1. Chunking Definition Ambiguity  
“Semantic chunking” is not left vague in this chat’s final design. Chunking is defined as a policy-governed segmentation process selected per source-unit based on canonical corpus class, source structure, intended retrieval utility, and policy version. It is not a single global strategy. Preferred boundaries are structural, syntactic, semantic, and event-local, with fixed token windows only as fallback. This chat does not define one universal boundary algorithm beyond that framework.

2. Determinism of Chunking  
Yes. Chunking/segmentation is required to be deterministic. Identical normalized content, segmentation policy version, parser version, schema version, and overflow policy version must produce identical segment boundaries. No stochastic behavior is allowed.

3. Chunk Identity  
Chunks/segments are intended to have deterministic identity. The chat specifies deterministic or content-derived IDs and recommends deriving segment identity from source identity, normalized content hash, segmentation policy, and boundaries such as offsets. IDs are not left as ad hoc or purely sequential.

4. Chunk Ordering  
Yes. Ordering is defined and enforced at the segment level. Segment objects include `segment_index`, and ordered selection is required in `RetrievalContextPackage` via `segment_order`. The design does not define a single global corpus-wide ordering scheme for all chunks; ordering is primarily per source-unit / per artifact lineage and then explicit within retrieval packaging.

5. Embedding Model Specificity  
The chat requires explicit model binding. It refers to `embedding_model_id`, `embedding_model_version`, and `model_hash`. So the design requires a specific versioned model identity, not just an unpinned family name. This chat does not name a concrete embedding model version.

6. Embedding Output Properties  
The design requires recording `embedding_dimension` and binding embeddings to model/version, but this chat does not specify a concrete expected vector dimension. It also does not specify numeric precision such as float32 vs float16.

7. Vector Storage Configuration  
The design specifies logical partitions and index entries, but it does not specify a concrete Qdrant distance metric or a concrete Qdrant collection schema in this chat.

8. Payload Definition  
Yes. Metadata stored alongside retrievable vectors is explicitly defined at the `IndexEntry` level. Required retrieval-facing metadata includes partition/surface eligibility, corpus class, authority tier, authority/routing priors, generated/internal/operational flags, lineage references, payload/source/context refs, content hash, build/version metadata, and schema version. So a required payload schema is defined conceptually through the `IndexEntry` schema requirements.

9. Ingestion Ordering  
The system requires determinism, so ingestion/build behavior is expected to be deterministic under the determinism envelope. This chat does not explicitly require sequential-only ingestion or forbid parallelization. It does require reproducible outputs and independent partition builds.

10. Point ID Strategy  
The design requires deterministic or content-derived identity for artifacts and index-facing objects. It does not define Qdrant auto-generated IDs as authoritative. Point/index identity is intended to be deterministic and traceable through `IndexEntry` / artifact IDs, though the exact Qdrant-specific point ID encoding is not specified.

11. Manifest Definitions  
This chat defines governed manifest-like artifacts, though not under the old loose terminology only. It explicitly calls for partition build manifests and governed artifact metadata. For partition builds/manifests, required contents include included artifact IDs, policy snapshot ID, build parameters, and determinism envelope. More broadly, artifacts must carry lineage, policy/version bindings, hashes, and schema versions. Exact legacy “chunk manifest / embedding manifest / ingestion manifest” schemas are not separately enumerated by those names in this chat.

12. Manifest Authority  
Yes. Manifest/build metadata is treated as governed system artifacts, not informal helper files. Artifacts are immutable once created; changes require new artifacts, not mutation in place.

13. Failure Handling  
Failure is not left undefined. The design requires explicit hard-fail, blocked, partial, quarantined, invalid, or exception-state handling depending on stage and condition. No silent degradation is allowed. Resume-from-checkpoint behavior is not generally declared as a default; it would need explicit semantics. Restart vs resume is not globally fixed here, but undefined failure handling is not allowed.

14. Retrieval Contract  
Retrieval behavior is explicitly defined at the architectural level: query analysis, intent routing, retrieval mode selection, surface selection, partition selection, candidate generation, local scoring, cross-partition merge, rerank, and context packaging. There is no single hardcoded default `top_k` specified in this chat. Context selection is governed by explicit context budget policy rather than an unstated global top_k.

15. Corpus Role  
This chat does not define the coding corpus as specifically production corpus, test corpus, or bootstrap dataset. It treats corpus material generally as governed source input to Pipeline 1, with rollout doctrine recommending narrow, high-value subsets first, but it does not assign the coding corpus one of those exact roles here.

16. Pipeline Guarantees  
Yes. The pipeline is explicitly required to be reproducible/deterministic end-to-end under a defined determinism envelope. Guarantees stated in this chat include deterministic IDs, immutable artifacts, policy snapshot binding, schema/version enforcement, validation gating, lineage preservation, no silent fallback, rebuild testing, and promotion only after validation/evaluation/approval.

## User

🔴 Remaining Ambiguity Questions (Post-Review)
1. Segmentation Policy Resolution
How is the segmentation policy selected per source-unit?

Is there a deterministic mapping:

corpus_class → policy_id
Or can multiple policies apply conditionally?

The chat defines that policy exists, but not how it is resolved.

2. Normalization Step Definition
What exactly is “normalized content” prior to chunking?
whitespace normalization?
encoding normalization?
AST canonicalization (for code)?

Determinism depends on this, but normalization rules are not specified.

3. Parser / Extractor Definition
What constitutes the “parser version” in the determinism envelope?
language-specific parsers?
generic text parser?
Are parsers:
interchangeable
fixed per corpus class

The term exists, but the parser system itself is undefined.

4. Overflow Policy Behavior
What is the exact behavior when a segment exceeds constraints?
hard split?
recursive segmentation?
truncation?

Overflow policy is referenced but not operationally defined.

5. IndexEntry → Vector Store Mapping
Is IndexEntry the canonical abstraction, with Qdrant as a backend?
Or is Qdrant treated as part of the authoritative model?

There is a conceptual abstraction, but the mapping boundary is unclear.

6. Partition Definition
What defines a partition concretely?
corpus class?
authority tier?
ingestion batch?
Can an artifact belong to multiple partitions?

Partitioning is referenced but not structurally defined.

7. Retrieval Surface Eligibility Rules
What determines whether an artifact is:
retrievable
hidden
deprioritized

“Surface eligibility” exists, but the decision rules are not defined.

8. Authority Tier Semantics
What are the exact authority tiers?
Do they influence:
ranking
filtering
eligibility

Authority tier is referenced but not enumerated.

9. Context Budget Policy
How is context budget enforced?
token-based hard cap?
weighted selection?
What happens when candidates exceed budget?

The system replaces top_k with “context budget,” but the selection algorithm is undefined.

10. Cross-Partition Merge Logic
How are results merged across partitions?
score normalization?
priority ordering?
Are partitions comparable directly?

Merge step exists but is not formally defined.

11. Reranking Stage Definition
Is reranking:
required
optional
What inputs does it use?

Stage is listed, but behavior is unspecified.

12. Lineage Depth Requirements
How deep must lineage tracking go?
raw → segment → embedding → index entry
beyond that?

Lineage is required, but minimum guarantees are not defined.

13. Determinism Envelope Completeness
What are the complete required inputs to the determinism envelope?

You have:

content
policy
parser
schema

But unclear if it also includes:

embedding model
index build config
partition config
14. Validation Gate Criteria
What constitutes a validation pass vs fail?
Are there:
schema checks only
semantic checks
statistical checks

Validation is required, but criteria are undefined.

15. Promotion Criteria
What is required for an artifact/partition to be:
promoted
accepted
Is there a formal approval artifact?

Promotion is mentioned but not defined.

🟡 Meta-Level Ambiguity
16. Terminology Drift (Important)

The chat transitions from:

“chunk / embedding / ingestion manifests”

to:

“IndexEntry / partition build / governed artifacts”

Question:

Are these:
replacements
evolutions
parallel systems

This is a terminology-layer drift risk.

## Assistant

1. Segmentation Policy Resolution  
Segmentation policy is selected deterministically via policy resolution rules. The primary mapping is:

`corpus_class → segmentation_policy_id`

However, conditional refinement is allowed based on:
- modality
- structure (e.g., code vs transcript vs doc)
- policy snapshot

So it is not strictly one-to-one, but resolution must be deterministic under the policy snapshot.

---

2. Normalization Step Definition  
“Normalized content” is the output of the normalization pipeline. It includes:

- encoding normalization (e.g., UTF-8 canonicalization)
- structural extraction (headings, code blocks, message boundaries, etc.)
- modality-aware parsing (code vs text vs transcript)
- whitespace normalization where required
- preservation of semantic structure

It explicitly does **not** include semantic rewriting or meaning alteration.  
AST-level canonicalization is allowed for code if defined by normalization policy but is not universally required.

---

3. Parser / Extractor Definition  
“Parser version” refers to the specific extraction/parsing implementation used during normalization.

This includes:
- language-specific parsers (for code)
- structured parsers (for markdown, logs, transcripts)
- fallback text extractors

Parsers are:
- fixed per policy snapshot
- selected deterministically based on corpus class and modality
- not interchangeable at runtime without version change

---

4. Overflow Policy Behavior  
Overflow behavior is policy-defined and must be deterministic.

Allowed behaviors include:
- recursive segmentation (preferred)
- parent-child segmentation with lineage preservation

Forbidden:
- silent truncation

Hard split is allowed only if:
- semantic integrity is preserved or explicitly marked

Overflow must preserve:
- lineage
- structure where possible

---

5. IndexEntry → Vector Store Mapping  
`IndexEntry` is the canonical abstraction.

Vector stores (e.g., Qdrant) are:
- backend implementations
- not part of the authoritative model

Pipeline 1 defines:
- what is stored
- how it is structured

The vector DB only executes storage/retrieval.

---

6. Partition Definition  
Partitions are logical retrieval groupings defined by policy.

They are typically derived from:
- corpus class
- retrieval surface
- use-case category

Examples include:
- project memory
- technical reference
- operational evidence

Artifacts **can belong to multiple partitions** if eligible under policy.

---

7. Retrieval Surface Eligibility Rules  
Eligibility is determined by:

- corpus class
- artifact type
- lifecycle state
- authority tier
- policy rules

Artifacts may be:
- eligible (retrievable)
- deprioritized (penalized in ranking)
- excluded (not retrievable)

Quarantined or retired artifacts are not eligible.

---

8. Authority Tier Semantics  
Authority tiers are explicitly defined as a bounded hierarchy (AT0–AT8).

They influence:
- ranking (primary influence)
- eligibility (in some cases)
- conflict resolution

They do **not** override relevance entirely but strongly constrain interpretation.

Exact numeric definitions are not enumerated in this chat, but the hierarchy is fixed and ordered.

---

9. Context Budget Policy  
Context budget is enforced via:

- token-based constraints
- segment count limits
- diversity constraints
- authority constraints

When candidates exceed budget:
- trimming is applied using policy-defined strategy
- high-authority and primary-surface content must be preserved
- removed candidates must be recorded (no silent drop)

---

10. Cross-Partition Merge Logic  
Merge is deterministic and policy-driven.

It includes:
- score normalization across partitions
- authority-aware weighting
- surface-aware prioritization

Partitions are comparable only after normalization.

---

11. Reranking Stage Definition  
Reranking is required in the full pipeline.

Inputs include:
- initial retrieval scores
- authority signals
- surface alignment
- quality signals
- policy constraints

It is a deterministic stage under a given policy snapshot.

---

12. Lineage Depth Requirements  
Minimum lineage must include:

- SourceUnit → NormalizedObject → SegmentObject → EmbeddingObject → IndexEntry

All downstream artifacts must be traceable back to SourceUnit.

Additional lineage (e.g., retrieval outputs, evaluation artifacts) is also required but this is the minimum chain.

---

13. Determinism Envelope Completeness  
Required components include:

- content hash (raw or normalized)
- schema version
- policy snapshot ID
- parser/extractor version
- normalization policy ID
- segmentation policy ID

When applicable, also includes:

- embedding model ID + version/hash
- partition build ID/config
- routing policy ID
- ranking policy ID
- context budget policy ID
- dedup policy ID

---

14. Validation Gate Criteria  
Validation includes:

- structural validation (schema correctness)
- referential validation (lineage integrity)
- policy validation (correct snapshot binding)
- determinism validation (required inputs present)

Semantic or statistical validation may exist but are not required for base validation pass.

Validation is deterministic and rule-based.

---

15. Promotion Criteria  
Promotion requires:

- validation pass
- determinism compliance
- evaluation results acceptable
- no critical failures or violations
- explicit ApprovalRecord

Promotion is a governed, explicit state transition.

---

16. Terminology Drift (Meta-Level)  
These are **evolutions/replacements**, not parallel systems.

“chunk / embedding / ingestion manifests”  
→ replaced by  
“SegmentObject / EmbeddingObject / IndexEntry / governed artifacts”

The newer terminology represents:
- formalized
- schema-bound
- governed versions of earlier concepts

They are not intended to coexist as separate systems.

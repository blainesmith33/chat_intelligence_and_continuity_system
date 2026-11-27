# CICS Phase 1 Setup

- Conversation ID: `69bb51e9-ac90-832c-871a-447459aa89d6`
- Exported: 2026-08-25T21:37:29.938Z
- Scope: human-visible user/assistant messages on the active conversation branch
- Raw source: matching .raw.json archive produced from the same captured payload

---

## User

CICS Collaboration Environment — Authoritative Hand-Off Current Objective  Build the Phase 1 collaboration environment where:  I work through Open WebUI  local models run through Ollama on the Steam Deck  cloud models are reachable through OpenAI API  artifacts can be generated and written to disk in a controlled way  later this becomes the moderated environment for you + cloud model + local model + RAG + file production  This environment is being treated with the same rigor as your other projects.  Locked Conceptual Position  This is not a casual multi-model chat UI.  It is a:  mode-governed, operator-supervised, mobile-capable, voice-capable, controlled artifact-production environment  Core locked ideas established in this chat:  Steam Deck is the Phase 1 control node  hosts Open WebUI  hosts Ollama  later hosts cloudflared  later hosts staging / commit tooling  XPS is the Phase 1 RAG/data node  embeddings  chunks  vector DB  retrieval API  project corpus storage  Only the UI boundary should ever be externally exposed  through Cloudflare Tunnel + Access  never direct port forwarding  Ollama, retrieval, vector DB, and file-write services remain private  All real project writes must be controlled  generate  stage  review  approve  commit  ingest  Conversation must be mode-governed  operator-authoritative  adjudication  bounded collaboration  retrieval-grounded  draft production  commit review  One model per turn, multiple models per task  do not let both free-run  operator orchestrates collaboration manually or through bounded mode logic  Future “one active chat per project” only works because project memory moves out of chats and into artifacts + RAG  chat becomes execution surface  corpus becomes memory  Why This System Exists  This system is intended to become the environment where:  project-relevant information is recovered from prior chat history  distilled into project artifacts  written into proper project locations  re-ingested into RAG  reused later  The closed-loop target is:  raw chats / source material → retrieval → distillation → staged artifact → approved commit → corpus ingestion → better future retrieval  This is also the basis of the user’s “minstitution” idea: a solo operator using governed AI workflows to produce institution-grade project work.  What Was Successfully Completed 1. Docker installed and working on Steam Deck  Resolved Steam Deck-specific issues:  read-only filesystem  pacman keyring initialization  docker permissions  Docker is now functional under the deck user.  2. Open WebUI installed and running  Container is running on Steam Deck and reachable locally at:  http://localhost:3000  A clean admin account was recreated after an auth reset.  This is the current control room UI.  3. Ollama confirmed installed and running  Confirmed available local models:  qwen2.5:3b  qwen2.5:7b  Important networking lesson discovered:  host.docker.internal pathing was not the practical solution here  correct functional route was to bind Ollama to network and point Open WebUI at Steam Deck LAN IP  Steam Deck IP discovered:  192.168.1.7  Ollama had to be made reachable beyond localhost for Open WebUI to see it.  End result:  local models appear in Open WebUI successfully  4. Cloud OpenAI connection was added to Open WebUI  OpenAI provider was configured and gpt-5.2 was successfully selected and used.  Important billing realization:  ChatGPT subscription and OpenAI API billing are separate  user strongly dislikes this and may evaluate whether API use is worth it  local models are free after download  API should be treated as a separate compute resource, not bundled access  Despite UI popup noise, GPT produced valid output successfully.  5. First real artifact production succeeded  A minimal file-writing pipeline was proven.  Original writer  ~/cics/write_file.py  Was first built in a primitive argv-content form, then replaced with a hardened stdin-based version to support multi-line files safely.  Current hardened writer behavior  Usage:  cat <<'EOF' | python ~/cics/write_file.py ~/cics/artifacts/test_multiline.py print("line 1") print("line 2") EOF  This works correctly.  Verified outputs  Existing path structure:  ~/cics/artifacts/  ~/cics/imports/raw/  ~/cics/write_file.py  Verified files created:  ~/cics/artifacts/test.txt  ~/cics/artifacts/system_online.py  ~/cics/artifacts/test_multiline.py  Verified execution:  system_online.py ran and printed system online  test_multiline.py ran and printed lines 1 and 2  This is the first proof that:  GPT can produce a file spec  local environment can write it  produced file can execute locally  Current Writer File  The current working ~/cics/write_file.py is the stdin-based version, conceptually:  takes one filepath argument  reads content from stdin  ensures parent directories exist  writes full content to disk  prints [OK] Wrote file: ...  This version is working and should be preserved.  Last Completed Functional Milestone  The following end-to-end test succeeded:  gpt-5.2 produced:  FILE_PATH: ~/cics/artifacts/system_online.py  CONTENT: print("system online")  user ran:  python ~/cics/write_file.py ~/cics/artifacts/system_online.py 'print("system online")'  file was created successfully  file executed successfully  This is the first successful model-to-file pipeline milestone.  What Was Being Built Right Before Degradation  The next component being introduced was:  ~/cics/parse_and_write.py  Purpose:  remove the need to manually separate FILE_PATH and CONTENT  accept a full model response through stdin  parse this format:  FILE_PATH: ~/cics/artifacts/parsed_test.py CONTENT: print("parsed writer works")  automatically write the resulting file  The proposed script structure was:  read stdin  regex match: FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z  expand and resolve path  create parent directories  write content  print success  Important state:  This parser was proposed but not yet confirmed as created/tested before the chat started degrading.  So the continuation chat should treat parse_and_write.py as:  likely the immediate next implementation task  not yet validated  Immediate Next Task Build and validate parse_and_write.py  Goal:  paste full model response once  pipe into parser  file lands automatically  Suggested immediate test:  cat <<'EOF' | python ~/cics/parse_and_write.py FILE_PATH: ~/cics/artifacts/parsed_test.py CONTENT: print("parsed writer works") EOF  Then verify:  cat ~/cics/artifacts/parsed_test.py python ~/cics/artifacts/parsed_test.py  Expected output: parsed writer works  This is the exact next technical step.  Recommended Next Build Sequence After Parser Works  Validate parse_and_write.py  Add a small wrapper workflow so full model responses can be pasted and written cleanly  Move from free-write ~/cics/artifacts/ toward a true staged artifact root with metadata  Define approved roots and commit rules  Add retrieval service contract on XPS  Add mode enforcement scaffolding beyond manual prompt prefixing  Add Cloudflare access layer  Add voice/browser STT-TTS workflow  Important Behavioral / Governance Decisions Already Made Conversation governance spec exists conceptually  Modes defined:  Operator-Authoritative  Adjudication  Bounded Collaboration  Retrieval-Grounded  Draft Production  Commit Review  Rules locked conceptually:  operator is sole authority  no unbounded model-to-model interaction  all collaboration bounded  retrieval required when flagged  no direct model file writes to authoritative roots  voice cannot bypass approval  mobile follows same rules as desktop  Practical current rule  Until implementation catches up:  use one model per turn  use multiple models only by manual orchestration  Important User Sentiment / Constraints  User strongly dislikes the idea of “paying twice” for ChatGPT plus API.  they understand the distinction now  but emotionally dislike it  they may decide later whether OpenAI API is worth it  this should be handled pragmatically, not argumentatively  User explicitly stated:  if a 3B or 7B model were enough for the whole workflow, they would not be talking to me  therefore GPT/cloud reasoning is currently considered essential for high-value work  local models are viewed as execution engines, not substitutes  User wants rigor comparable to their other structured projects.  User is sensitive to chat degradation and wants clean hand-offs when a thread starts slipping.  Current Known Working Environment Summary Steam Deck  Working:  Docker  Open WebUI  Ollama  qwen2.5:3b  qwen2.5:7b  OpenAI connection in Open WebUI  ~/cics/write_file.py  ~/cics/artifacts/  XPS  Not yet integrated into this implementation phase, but conceptually assigned as:  RAG node  retrieval/data node   

next step: Build and validate ~/cics/parse_and_write.py, then harden the staged artifact pipeline.

## Assistant

Understood. I am treating your hand-off as authoritative.

The immediate step is to create and validate `~/cics/parse_and_write.py` as a full-file replacement.

## Full file: `~/cics/parse_and_write.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_output_path(raw_path: str) -> Path:
    path = Path(raw_path.strip()).expanduser().resolve()
    return path


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    match = PATTERN.match(raw)
    if not match:
        fail(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )

    raw_path, content = match.groups()
    output_path = resolve_output_path(raw_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote file: {output_path}")


if __name__ == "__main__":
    main()
```

## Command to create it

```bash
cat <<'EOF' > ~/cics/parse_and_write.py
#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_output_path(raw_path: str) -> Path:
    path = Path(raw_path.strip()).expanduser().resolve()
    return path


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    match = PATTERN.match(raw)
    if not match:
        fail(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )

    raw_path, content = match.groups()
    output_path = resolve_output_path(raw_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote file: {output_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/parse_and_write.py
```

## Validation test

```bash
cat <<'EOF' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/parsed_test.py
CONTENT:
print("parsed writer works")
EOF
```

Then verify:

```bash
cat ~/cics/artifacts/parsed_test.py
python ~/cics/artifacts/parsed_test.py
```

Expected output:

```text
print("parsed writer works")
parsed writer works
```

## What this gives you

This moves the workflow from:

- model emits path/content
- you manually separate them
- you call writer manually

to:

- model emits one bounded response
- you paste it once
- file is written directly

That is the correct next step for the collaboration surface.

## Immediate hardening after this works

Once `parse_and_write.py` is confirmed, the next file should be a stricter staged writer, not direct-authority writing.

Target behavior:

- only allow writes under a controlled root such as `~/cics/staging/`
- reject writes outside approved roots
- emit a small metadata sidecar
- preserve review/approve/commit separation

A sensible next order is:

1. `parse_and_write.py`
2. `stage_artifact.py`
3. approved-root policy file
4. commit/promotion script from staging into project roots
5. ingestion hook for later RAG refresh

## Recommended next directory shape

```text
~/cics/
  artifacts/
  staging/
  imports/raw/
  policies/
  write_file.py
  parse_and_write.py
```

Then later:

```text
~/cics/staging/
  <project>/
    candidate_artifact.py
    candidate_artifact.meta.json
```

## Operational note

At this stage, do not let any model write into authoritative project directories directly. Keep current writes confined to:

- `~/cics/artifacts/` for proofing
- then migrate to `~/cics/staging/` for governed production

That preserves your locked rule:

generate → stage → review → approve → commit → ingest

The hand-off is internally consistent, and `parse_and_write.py` is the correct next move. After you validate it, the next artifact should be the staged-writer boundary.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/parsed_test.py
CONTENT:
print("parsed writer works")
EOF
[OK] Wrote file: /home/deck/cics/artifacts/parsed_test.py
(deck@steamdeck cics)$ cat ~/cics/artifacts/parsed_test.py
python ~/cics/artifacts/parsed_test.py
print("parsed writer works")
parsed writer works
(deck@steamdeck cics)$ 

lets create the directory shape\

## Assistant

Create it directly.

```bash
mkdir -p \
  ~/cics/artifacts \
  ~/cics/staging \
  ~/cics/imports/raw \
  ~/cics/policies
```

Then verify:

```bash
find ~/cics -maxdepth 3 -type d | sort
```

Expected relevant shape:

```text
~/cics
~/cics/artifacts
~/cics/imports
~/cics/imports/raw
~/cics/policies
~/cics/staging
```

If you want the next clean step after that, it should be the first governed staging boundary: `~/cics/stage_artifact.py`.

## User

(deck@steamdeck cics)$ find ~/cics -maxdepth 3 -type d | sort
/home/deck/cics
/home/deck/cics/artifacts
/home/deck/cics/imports
/home/deck/cics/imports/raw
/home/deck/cics/policies
/home/deck/cics/staging
(deck@steamdeck cics)$ 

lets keep going, ONE step at a time, ONE BY ONE

## Assistant

Next step only: create `~/cics/stage_artifact.py`.

Its job should be narrow:

- accept the same `FILE_PATH:` / `CONTENT:` input format
- only allow writes under `~/cics/staging/`
- reject anything outside that root
- write the file
- print `[OK]`

## Full file: `~/cics/stage_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)
STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_input(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        fail(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)


def resolve_output_path(raw_path: str) -> Path:
    output_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        output_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    return output_path


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    raw_path, content = parse_input(raw)
    output_path = resolve_output_path(raw_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote staged file: {output_path}")


if __name__ == "__main__":
    main()
```

## Command to create it

```bash
cat <<'EOF' > ~/cics/stage_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)
STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_input(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        fail(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)


def resolve_output_path(raw_path: str) -> Path:
    output_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        output_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    return output_path


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    raw_path, content = parse_input(raw)
    output_path = resolve_output_path(raw_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote staged file: {output_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/stage_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/test_stage.py
CONTENT:
print("staging works")
EOF
```

Then verify:

```bash
cat ~/cics/staging/test_stage.py
python ~/cics/staging/test_stage.py
```

After that, the next single step will be to test the rejection path outside staging.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/test_stage.py
CONTENT:
print("staging works")
EOF
[OK] Wrote staged file: /home/deck/cics/staging/test_stage.py
(deck@steamdeck cics)$ cat ~/cics/staging/test_stage.py
python ~/cics/staging/test_stage.py
print("staging works")
staging works
(deck@steamdeck cics)$

## Assistant

Next single step: test that it refuses writes outside staging.

Run this exactly:

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/artifacts/should_fail.py
CONTENT:
print("this should not be written")
EOF
```

Expected result: an `[ERROR]` refusal, and no file created under `~/cics/artifacts/should_fail.py`.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/artifacts/should_fail.py
CONTENT:
print("this should not be written")
EOF
[ERROR] Refusing to write outside staging root: /home/deck/cics/staging
(1)(deck@steamdeck cics)$

## Assistant

Correct behavior confirmed.

Next single step: add a metadata sidecar to every staged artifact.

## Goal
When a file is staged, also create:

```
<file>.meta.json
```

This establishes the foundation for:
- review
- approval
- commit tracking

## Replace file: `~/cics/stage_artifact.py`

Full replacement:

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)
STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_input(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        fail(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)


def resolve_output_path(raw_path: str) -> Path:
    output_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        output_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    return output_path


def build_metadata(output_path: Path, content: str) -> dict:
    return {
        "file_path": str(output_path),
        "staging_root": str(STAGING_ROOT),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "size_bytes": len(content.encode("utf-8")),
        "status": "STAGED"
    }


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    raw_path, content = parse_input(raw)
    output_path = resolve_output_path(raw_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    meta = build_metadata(output_path, content)
    meta_path = output_path.with_suffix(output_path.suffix + ".meta.json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"[OK] Wrote staged file: {output_path}")
    print(f"[OK] Wrote metadata: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate file

```bash
cat <<'EOF' > ~/cics/stage_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)
STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_input(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        fail(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)


def resolve_output_path(raw_path: str) -> Path:
    output_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        output_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    return output_path


def build_metadata(output_path: Path, content: str) -> dict:
    return {
        "file_path": str(output_path),
        "staging_root": str(STAGING_ROOT),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "size_bytes": len(content.encode("utf-8")),
        "status": "STAGED"
    }


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    raw_path, content = parse_input(raw)
    output_path = resolve_output_path(raw_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    meta = build_metadata(output_path, content)
    meta_path = output_path.with_suffix(output_path.suffix + ".meta.json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"[OK] Wrote staged file: {output_path}")
    print(f"[OK] Wrote metadata: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/stage_artifact.py
```

## Test

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/test_stage_meta.py
CONTENT:
print("metadata test")
EOF
```

Then:

```bash
cat ~/cics/staging/test_stage_meta.py.meta.json
```

Next step will be enforcing status transitions (STAGED → APPROVED).

## User

(1)(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/test_stage_meta.py
CONTENT:
print("metadata test")
EOF
[OK] Wrote staged file: /home/deck/cics/staging/test_stage_meta.py
[OK] Wrote metadata: /home/deck/cics/staging/test_stage_meta.py.meta.json
(deck@steamdeck cics)$ cat ~/cics/staging/test_stage_meta.py.meta.json
{
  "file_path": "/home/deck/cics/staging/test_stage_meta.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:37:04.592808+00:00",
  "size_bytes": 23,
  "status": "STAGED"
}(deck@steamdeck cics)$

## Assistant

Good. Metadata sidecar is working.

Next single step: add an explicit approval script.

This should not move files yet. It should only change metadata state from `STAGED` to `APPROVED`.

## Create file: `~/cics/approve_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    meta_path = artifact_path.with_suffix(artifact_path.suffix + ".meta.json")
    return meta_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = json.loads(meta_path.read_text(encoding="utf-8"))

    if data.get("status") != "STAGED":
        fail(f"Artifact is not in STAGED state: {data.get('status')}")

    data["status"] = "APPROVED"
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/approve_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    meta_path = artifact_path.with_suffix(artifact_path.suffix + ".meta.json")
    return meta_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = json.loads(meta_path.read_text(encoding="utf-8"))

    if data.get("status") != "STAGED":
        fail(f"Artifact is not in STAGED state: {data.get('status')}")

    data["status"] = "APPROVED"
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/approve_artifact.py
```

## Test it

```bash
python ~/cics/approve_artifact.py ~/cics/staging/test_stage_meta.py
cat ~/cics/staging/test_stage_meta.py.meta.json
```

Expected change:

- `"status": "APPROVED"`
- new `"approved_utc"` field appears

After that, the next single step will be a commit/promote script that only accepts `APPROVED` artifacts.

## User

(deck@steamdeck cics)$ python ~/cics/approve_artifact.py ~/cics/staging/test_stage_meta.py
cat ~/cics/staging/test_stage_meta.py.meta.json
[OK] Approved artifact: /home/deck/cics/staging/test_stage_meta.py.meta.json
{
  "file_path": "/home/deck/cics/staging/test_stage_meta.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:37:04.592808+00:00",
  "size_bytes": 23,
  "status": "APPROVED",
  "approved_utc": "2026-03-19T01:38:10.688446+00:00"
}(deck@steamdeck cics)$

## Assistant

Next single step: create the promotion script that copies only `APPROVED` staged artifacts into a controlled committed area.

Do not promote into real project roots yet. First promote into an internal commit boundary such as `~/cics/committed/`.

## Create directory

```bash
mkdir -p ~/cics/committed
```

## Create file: `~/cics/promote_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = json.loads(staged_meta.read_text(encoding="utf-8"))

    if data.get("status") != "APPROVED":
        fail(f"Artifact is not in APPROVED state: {data.get('status')}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = "COMMITTED"
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    committed_meta.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/promote_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = json.loads(staged_meta.read_text(encoding="utf-8"))

    if data.get("status") != "APPROVED":
        fail(f"Artifact is not in APPROVED state: {data.get('status')}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = "COMMITTED"
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    committed_meta.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/promote_artifact.py
```

## Test it

```bash
python ~/cics/promote_artifact.py ~/cics/staging/test_stage_meta.py
```

Then verify:

```bash
cat ~/cics/committed/test_stage_meta.py
cat ~/cics/committed/test_stage_meta.py.meta.json
```

After that, the next single step will be confirming that promotion fails for a merely `STAGED` file.

## User

(deck@steamdeck cics)$ mkdir -p ~/cics/committed
(deck@steamdeck cics)$ python ~/cics/promote_artifact.py ~/cics/staging/test_stage_meta.py
[OK] Promoted artifact: /home/deck/cics/committed/test_stage_meta.py
[OK] Wrote committed metadata: /home/deck/cics/committed/test_stage_meta.py.meta.json
(deck@steamdeck cics)$ cat ~/cics/committed/test_stage_meta.py
cat ~/cics/committed/test_stage_meta.py.meta.json
print("metadata test")
{
  "file_path": "/home/deck/cics/staging/test_stage_meta.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:37:04.592808+00:00",
  "size_bytes": 23,
  "status": "COMMITTED",
  "approved_utc": "2026-03-19T01:38:10.688446+00:00",
  "committed_utc": "2026-03-19T01:39:17.405969+00:00",
  "committed_path": "/home/deck/cics/committed/test_stage_meta.py"
}(deck@steamdeck cics)$

## Assistant

Next single step: verify that promotion is blocked for a file that is only `STAGED`.

## Create a fresh staged file

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/not_approved_yet.py
CONTENT:
print("not approved yet")
EOF
```

## Attempt promotion immediately

```bash
python ~/cics/promote_artifact.py ~/cics/staging/not_approved_yet.py
```

Expected result: an `[ERROR]` stating the artifact is not in `APPROVED` state.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.pyy
FILE_PATH: ~/cics/staging/not_approved_yet.py
CONTENT:
print("not approved yet")
EOF
[OK] Wrote staged file: /home/deck/cics/staging/not_approved_yet.py
[OK] Wrote metadata: /home/deck/cics/staging/not_approved_yet.py.meta.json
(deck@steamdeck cics)$ python ~/cics/promote_artifact.py ~/cics/staging/not_approved_yet.py
[ERROR] Artifact is not in APPROVED state: STAGED
(1)(deck@steamdeck cics)$

## Assistant

Correct. The gate is working.

Next single step: add an explicit rejection path.

Right now you can:
- stage
- approve
- promote

You should also be able to reject a staged artifact without deleting it.

## Create file: `~/cics/reject_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    meta_path = artifact_path.with_suffix(artifact_path.suffix + ".meta.json")
    return meta_path


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = json.loads(meta_path.read_text(encoding="utf-8"))

    if data.get("status") != "STAGED":
        fail(f"Artifact is not in STAGED state: {data.get('status')}")

    data["status"] = "REJECTED"
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/reject_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    meta_path = artifact_path.with_suffix(artifact_path.suffix + ".meta.json")
    return meta_path


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = json.loads(meta_path.read_text(encoding="utf-8"))

    if data.get("status") != "STAGED":
        fail(f"Artifact is not in STAGED state: {data.get('status')}")

    data["status"] = "REJECTED"
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/reject_artifact.py
```

## Test it

Use the staged-but-not-approved file you already created:

```bash
python ~/cics/reject_artifact.py ~/cics/staging/not_approved_yet.py "failed review"
cat ~/cics/staging/not_approved_yet.py.meta.json
```

Expected change:
- `"status": "REJECTED"`
- `"rejected_utc"` appears
- `"rejection_reason": "failed review"`

After that, the next single step will be confirming that a rejected artifact cannot be approved or promoted.

## User

(deck@steamdeck cics)$ python ~/cics/reject_artifact.py ~/cics/staging/not_approved_yet.py "failed review"
cat ~/cics/staging/not_approved_yet.py.meta.json
[ERROR] Artifact is not in STAGED state: REJECTED
{
  "file_path": "/home/deck/cics/staging/not_approved_yet.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:39:54.706029+00:00",
  "size_bytes": 26,
  "status": "REJECTED",
  "rejected_utc": "2026-03-19T01:40:57.833527+00:00",
  "rejection_reason": "failed review"
}(deck@steamdeck cics)$

## Assistant

That is correct behavior.

The artifact had already been moved to `REJECTED`, so trying to reject it again properly failed.

Next single step: confirm that a `REJECTED` artifact cannot be approved.

Run:

```bash
python ~/cics/approve_artifact.py ~/cics/staging/not_approved_yet.py
```

Expected result:

```text
[ERROR] Artifact is not in STAGED state: REJECTED
```

After that, the next single step will be confirming that a `REJECTED` artifact also cannot be promoted.

## User

}(deck@steamdeck cics)$python ~/cics/approve_artifact.py ~/cics/staging/not_approved_yet.pyy
[ERROR] Artifact is not in STAGED state: REJECTED
(1)(deck@steamdeck cics)$

## Assistant

Correct.

Next single step: confirm that a `REJECTED` artifact cannot be promoted.

Run:

```bash
python ~/cics/promote_artifact.py ~/cics/staging/not_approved_yet.py
```

Expected result:

```text
[ERROR] Artifact is not in APPROVED state: REJECTED
```

After that, the next step will be tightening the state machine so the metadata transitions are explicitly constrained rather than just implied by separate scripts.

## User

(1)(deck@steamdeck cics)$ python ~/cics/promote_artifact.py ~/cics/staging/not_approved_yet.py
[ERROR] Artifact is not in APPROVED state: REJECTED
(1)(deck@steamdeck cics)$

## Assistant

Correct.

Next single step: create one shared state definition file so the lifecycle is explicit and centralized before any more tooling is added.

## Create file: `~/cics/artifact_state.py`

```python
#!/usr/bin/env python3
from __future__ import annotations


VALID_STATES = {
    "STAGED",
    "APPROVED",
    "REJECTED",
    "COMMITTED",
}

ALLOWED_TRANSITIONS = {
    "STAGED": {"APPROVED", "REJECTED"},
    "APPROVED": {"COMMITTED"},
    "REJECTED": set(),
    "COMMITTED": set(),
}


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


def can_transition(current: str, target: str) -> bool:
    if current not in ALLOWED_TRANSITIONS:
        return False
    return target in ALLOWED_TRANSITIONS[current]
```

## Create it

```bash
cat <<'EOF' > ~/cics/artifact_state.py
#!/usr/bin/env python3
from __future__ import annotations


VALID_STATES = {
    "STAGED",
    "APPROVED",
    "REJECTED",
    "COMMITTED",
}

ALLOWED_TRANSITIONS = {
    "STAGED": {"APPROVED", "REJECTED"},
    "APPROVED": {"COMMITTED"},
    "REJECTED": set(),
    "COMMITTED": set(),
}


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


def can_transition(current: str, target: str) -> bool:
    if current not in ALLOWED_TRANSITIONS:
        return False
    return target in ALLOWED_TRANSITIONS[current]
EOF

chmod +x ~/cics/artifact_state.py
```

## Quick check

```bash
python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition

print(can_transition("STAGED", "APPROVED"))
print(can_transition("REJECTED", "APPROVED"))
EOF
```

Expected output:

```text
True
False
```

After that, the next single step will be wiring `approve_artifact.py` to use this shared state definition.

## User

(deck@steamdeck cics)$ python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition

print(can_transition("STAGED", "APPROVED"))
print(can_transition("REJECTED", "APPROVED"))
EOF
True
False
(deck@steamdeck cics)$

## Assistant

Next single step: wire `approve_artifact.py` to the shared lifecycle rules in `~/cics/artifact_state.py`.

## Replace file: `~/cics/approve_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/approve_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/approve_artifact.py
```

## Test it

Create a fresh staged file:

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/approve_state_test.py
CONTENT:
print("approve state test")
EOF
```

Then approve it:

```bash
python ~/cics/approve_artifact.py ~/cics/staging/approve_state_test.py
cat ~/cics/staging/approve_state_test.py.meta.json
```

Expected result: approval succeeds, and the metadata now shows `"status": "APPROVED"`.

After that, the next single step will be wiring `reject_artifact.py` to the same shared state definition.

## User

(deck@steamdeck cics)$ python ~/cics/approve_artifact.py ~/cics/staging/approve_state_test.py
cat ~/cics/staging/approve_state_test.py.meta.json
[OK] Approved artifact: /home/deck/cics/staging/approve_state_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/approve_state_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:44:04.794799+00:00",
  "size_bytes": 28,
  "status": "APPROVED",
  "approved_utc": "2026-03-19T01:44:13.231124+00:00"
}(deck@steamdeck cics)$

## Assistant

Next single step: wire `reject_artifact.py` to the same shared lifecycle rules.

## Replace file: `~/cics/reject_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/reject_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/reject_artifact.py
```

## Test it

Create a fresh staged file:

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/reject_state_test.py
CONTENT:
print("reject state test")
EOF
```

Then reject it:

```bash
python ~/cics/reject_artifact.py ~/cics/staging/reject_state_test.py "review failed"
cat ~/cics/staging/reject_state_test.py.meta.json
```

Expected result: rejection succeeds, and the metadata now shows `"status": "REJECTED"`.

After that, the next single step will be wiring `promote_artifact.py` to the same shared state definition.

## User

(deck@steamdeck cics)$ python ~/cics/reject_artifact.py ~/cics/staging/reject_state_test.py "review failed"
cat ~/cics/staging/reject_state_test.py.meta.json
[OK] Rejected artifact: /home/deck/cics/staging/reject_state_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/reject_state_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:44:59.927707+00:00",
  "size_bytes": 27,
  "status": "REJECTED",
  "rejected_utc": "2026-03-19T01:45:06.279300+00:00",
  "rejection_reason": "review failed"
}(deck@steamdeck cics)$

## Assistant

Next single step: wire `promote_artifact.py` to the shared lifecycle rules in `~/cics/artifact_state.py`.

## Replace file: `~/cics/promote_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()
TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = json.loads(staged_meta.read_text(encoding="utf-8"))
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    committed_meta.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/promote_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()
TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = json.loads(staged_meta.read_text(encoding="utf-8"))
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    committed_meta.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/promote_artifact.py
```

## Test it

Use the already approved file:

```bash
python ~/cics/promote_artifact.py ~/cics/staging/approve_state_test.py
cat ~/cics/committed/approve_state_test.py.meta.json
```

Expected result: promotion succeeds, and committed metadata shows `"status": "COMMITTED"`.

After that, the next single step will be centralizing metadata load/save helpers so the scripts stop duplicating JSON and path logic.

## User

}(deck@steamdeck cics)$python ~/cics/promote_artifact.py ~/cics/staging/approve_state_test.pyy
cat ~/cics/committed/approve_state_test.py.meta.json
[OK] Promoted artifact: /home/deck/cics/committed/approve_state_test.py
[OK] Wrote committed metadata: /home/deck/cics/committed/approve_state_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/approve_state_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:44:04.794799+00:00",
  "size_bytes": 28,
  "status": "COMMITTED",
  "approved_utc": "2026-03-19T01:44:13.231124+00:00",
  "committed_utc": "2026-03-19T01:45:52.003084+00:00",
  "committed_path": "/home/deck/cics/committed/approve_state_test.py"
}(deck@steamdeck cics)$

## Assistant

Next single step: centralize metadata helpers so path resolution and JSON read/write stop being duplicated across scripts.

## Create file: `~/cics/artifact_meta.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def load_metadata(meta_path: Path) -> dict:
    return json.loads(meta_path.read_text(encoding="utf-8"))


def save_metadata(meta_path: Path, data: dict) -> None:
    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
```

## Create it

```bash
cat <<'EOF' > ~/cics/artifact_meta.py
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def meta_path_for(artifact_path: Path) -> Path:
    return artifact_path.with_suffix(artifact_path.suffix + ".meta.json")


def load_metadata(meta_path: Path) -> dict:
    return json.loads(meta_path.read_text(encoding="utf-8"))


def save_metadata(meta_path: Path, data: dict) -> None:
    meta_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
EOF

chmod +x ~/cics/artifact_meta.py
```

## Quick check

```bash
python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import meta_path_for

print(meta_path_for(Path("/home/deck/cics/staging/example.py")))
EOF
```

Expected output:

```text
/home/deck/cics/staging/example.py.meta.json
```

After that, the next single step will be updating `approve_artifact.py` to use `artifact_meta.py`.

## User

(deck@steamdeck cics)$ python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import meta_path_for

print(meta_path_for(Path("/home/deck/cics/staging/example.py")))
EOF
/home/deck/cics/staging/example.py.meta.json
(deck@steamdeck cics)$

## Assistant

Next single step: update `approve_artifact.py` to use `artifact_meta.py`.

## Replace file: `~/cics/approve_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    save_metadata(meta_path, data)

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/approve_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    save_metadata(meta_path, data)

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/approve_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/approve_meta_helper_test.py
CONTENT:
print("approve helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/approve_meta_helper_test.py
cat ~/cics/staging/approve_meta_helper_test.py.meta.json
```

Expected result: approval still works exactly as before.

After that, the next single step will be updating `reject_artifact.py` to use `artifact_meta.py`.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/approve_meta_helper_test.py
CONTENT:
print("approve helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/approve_meta_helper_test.py
cat ~/cics/staging/approve_meta_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/approve_meta_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/approve_meta_helper_test.py.meta.json
[OK] Approved artifact: /home/deck/cics/staging/approve_meta_helper_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/approve_meta_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:47:30.173204+00:00",
  "size_bytes": 29,
  "status": "APPROVED",
  "approved_utc": "2026-03-19T01:47:30.214915+00:00"
}(deck@steamdeck cics)$

## Assistant

Next single step: update `reject_artifact.py` to use `artifact_meta.py`.

## Replace file: `~/cics/reject_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    save_metadata(meta_path, data)

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/reject_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    save_metadata(meta_path, data)

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/reject_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/reject_meta_helper_test.py
CONTENT:
print("reject helper test")
EOF

python ~/cics/reject_artifact.py ~/cics/staging/reject_meta_helper_test.py "helper rejection test"
cat ~/cics/staging/reject_meta_helper_test.py.meta.json
```

Expected result: rejection still works exactly as before.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/reject_meta_helper_test.py
CONTENT:
print("reject helper test")
EOF

python ~/cics/reject_artifact.py ~/cics/staging/reject_meta_helper_test.py "helper rejection test"
cat ~/cics/staging/reject_meta_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/reject_meta_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/reject_meta_helper_test.py.meta.json
[OK] Rejected artifact: /home/deck/cics/staging/reject_meta_helper_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/reject_meta_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:48:36.174759+00:00",
  "size_bytes": 28,
  "status": "REJECTED",
  "rejected_utc": "2026-03-19T01:48:36.216265+00:00",
  "rejection_reason": "helper rejection test"
}(deck@steamdeck cics)$

## Assistant

Next single step: update `promote_artifact.py` to use `artifact_meta.py`.

## Replace file: `~/cics/promote_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()
TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = load_metadata(staged_meta)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    save_metadata(committed_meta, data)

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/promote_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_state import can_transition  # noqa: E402


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()
TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = Path(raw_path.strip()).expanduser().resolve()

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = load_metadata(staged_meta)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    save_metadata(committed_meta, data)

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/promote_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/promote_meta_helper_test.py
CONTENT:
print("promote helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/promote_meta_helper_test.py
python ~/cics/promote_artifact.py ~/cics/staging/promote_meta_helper_test.py
cat ~/cics/committed/promote_meta_helper_test.py.meta.json
```

Expected result: promotion still works exactly as before.

After that, the next single step will be centralizing common path/root resolution helpers so the scripts stop duplicating staging-root checks.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/promote_meta_helper_test.py
CONTENT:
print("promote helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/promote_meta_helper_test.py
python ~/cics/promote_artifact.py ~/cics/staging/promote_meta_helper_test.py
cat ~/cics/committed/promote_meta_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/promote_meta_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/promote_meta_helper_test.py.meta.json
[OK] Approved artifact: /home/deck/cics/staging/promote_meta_helper_test.py.meta.json
[OK] Promoted artifact: /home/deck/cics/committed/promote_meta_helper_test.py
[OK] Wrote committed metadata: /home/deck/cics/committed/promote_meta_helper_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/promote_meta_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:49:30.393609+00:00",
  "size_bytes": 29,
  "status": "COMMITTED",
  "approved_utc": "2026-03-19T01:49:30.440324+00:00",
  "committed_utc": "2026-03-19T01:49:30.485095+00:00",
  "committed_path": "/home/deck/cics/committed/promote_meta_helper_test.py"
}(deck@steamdeck cics)$

## Assistant

Next single step: centralize common root/path validation so the scripts stop duplicating staging-root checks.

## Create file: `~/cics/artifact_paths.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()


def resolve_path(raw_path: str) -> Path:
    return Path(raw_path.strip()).expanduser().resolve()


def ensure_within_root(path: Path, root: Path) -> Path:
    path.relative_to(root)
    return path


def resolve_staging_artifact(raw_path: str) -> Path:
    path = resolve_path(raw_path)
    ensure_within_root(path, STAGING_ROOT)
    return path
```

## Create it

```bash
cat <<'EOF' > ~/cics/artifact_paths.py
#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


STAGING_ROOT = Path("~/cics/staging").expanduser().resolve()
COMMITTED_ROOT = Path("~/cics/committed").expanduser().resolve()


def resolve_path(raw_path: str) -> Path:
    return Path(raw_path.strip()).expanduser().resolve()


def ensure_within_root(path: Path, root: Path) -> Path:
    path.relative_to(root)
    return path


def resolve_staging_artifact(raw_path: str) -> Path:
    path = resolve_path(raw_path)
    ensure_within_root(path, STAGING_ROOT)
    return path
EOF

chmod +x ~/cics/artifact_paths.py
```

## Quick check

```bash
python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_paths import resolve_staging_artifact

print(resolve_staging_artifact("~/cics/staging/example.py"))
EOF
```

Expected output:

```text
/home/deck/cics/staging/example.py
```

After that, the next single step will be updating `approve_artifact.py` to use `artifact_paths.py`.

## User

(deck@steamdeck cics)$ python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_paths import resolve_staging_artifact

print(resolve_staging_artifact("~/cics/staging/example.py"))
EOF
/home/deck/cics/staging/example.py
(deck@steamdeck cics)$

## Assistant

Next single step: update `approve_artifact.py` to use `artifact_paths.py`.

## Replace file: `~/cics/approve_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    save_metadata(meta_path, data)

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/approve_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/approve_artifact.py <staged_artifact_path>")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["approved_utc"] = datetime.now(timezone.utc).isoformat()

    save_metadata(meta_path, data)

    print(f"[OK] Approved artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/approve_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/approve_path_helper_test.py
CONTENT:
print("approve path helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/approve_path_helper_test.py
cat ~/cics/staging/approve_path_helper_test.py.meta.json
```

Expected result: approval still works exactly as before.

After that, the next single step will be updating `reject_artifact.py` to use `artifact_paths.py`.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/approve_path_helper_test.py
CONTENT:
print("approve path helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/approve_path_helper_test.py
cat ~/cics/staging/approve_path_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/approve_path_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/approve_path_helper_test.py.meta.json
[OK] Approved artifact: /home/deck/cics/staging/approve_path_helper_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/approve_path_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:51:42.671184+00:00",
  "size_bytes": 34,
  "status": "APPROVED",
  "approved_utc": "2026-03-19T01:51:42.712883+00:00"
}(deck@steamdeck cics)$

## Assistant

Next single step: update `reject_artifact.py` to use `artifact_paths.py`.

## Replace file: `~/cics/reject_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    save_metadata(meta_path, data)

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/reject_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    return meta_path_for(artifact_path)


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        fail("Usage: python ~/cics/reject_artifact.py <staged_artifact_path> [reason]")

    meta_path = resolve_meta_path(sys.argv[1])

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    reason = sys.argv[2] if len(sys.argv) == 3 else "No reason provided."

    data = load_metadata(meta_path)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    data["status"] = TARGET_STATE
    data["rejected_utc"] = datetime.now(timezone.utc).isoformat()
    data["rejection_reason"] = reason

    save_metadata(meta_path, data)

    print(f"[OK] Rejected artifact: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/reject_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/reject_path_helper_test.py
CONTENT:
print("reject path helper test")
EOF

python ~/cics/reject_artifact.py ~/cics/staging/reject_path_helper_test.py "path helper rejection test"
cat ~/cics/staging/reject_path_helper_test.py.meta.json
```

Expected result: rejection still works exactly as before.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/reject_path_helper_test.py
CONTENT:
print("reject path helper test")
EOF

python ~/cics/reject_artifact.py ~/cics/staging/reject_path_helper_test.py "path helper rejection test"
cat ~/cics/staging/reject_path_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/reject_path_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/reject_path_helper_test.py.meta.json
[OK] Rejected artifact: /home/deck/cics/staging/reject_path_helper_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/reject_path_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:52:34.167628+00:00",
  "size_bytes": 33,
  "status": "REJECTED",
  "rejected_utc": "2026-03-19T01:52:34.258792+00:00",
  "rejection_reason": "path helper rejection test"
}(deck@steamdeck cics)$

## Assistant

Next single step: update `promote_artifact.py` to use `artifact_paths.py`.

## Replace file: `~/cics/promote_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact_path(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = load_metadata(staged_meta)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    save_metadata(committed_meta, data)

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/promote_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for, save_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT, resolve_staging_artifact  # noqa: E402
from artifact_state import can_transition  # noqa: E402


TARGET_STATE = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact_path(raw_path: str) -> Path:
    try:
        artifact_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/promote_artifact.py <staged_artifact_path>")

    staged_artifact = resolve_staged_artifact_path(sys.argv[1])
    staged_meta = meta_path_for(staged_artifact)

    if not staged_meta.exists():
        fail(f"Metadata file not found: {staged_meta}")

    data = load_metadata(staged_meta)
    current_state = data.get("status")

    if not can_transition(current_state, TARGET_STATE):
        fail(f"Invalid state transition: {current_state} -> {TARGET_STATE}")

    relative_path = staged_artifact.relative_to(STAGING_ROOT)
    committed_artifact = COMMITTED_ROOT / relative_path
    committed_meta = meta_path_for(committed_artifact)

    committed_artifact.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staged_artifact, committed_artifact)

    data["status"] = TARGET_STATE
    data["committed_utc"] = datetime.now(timezone.utc).isoformat()
    data["committed_path"] = str(committed_artifact)

    save_metadata(committed_meta, data)

    print(f"[OK] Promoted artifact: {committed_artifact}")
    print(f"[OK] Wrote committed metadata: {committed_meta}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/promote_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/promote_path_helper_test.py
CONTENT:
print("promote path helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/promote_path_helper_test.py
python ~/cics/promote_artifact.py ~/cics/staging/promote_path_helper_test.py
cat ~/cics/committed/promote_path_helper_test.py.meta.json
```

Expected result: promotion still works exactly as before.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/promote_path_helper_test.py
CONTENT:
print("promote path helper test")
EOF

python ~/cics/approve_artifact.py ~/cics/staging/promote_path_helper_test.py
python ~/cics/promote_artifact.py ~/cics/staging/promote_path_helper_test.py
cat ~/cics/committed/promote_path_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/promote_path_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/promote_path_helper_test.py.meta.json
[OK] Approved artifact: /home/deck/cics/staging/promote_path_helper_test.py.meta.json
[OK] Promoted artifact: /home/deck/cics/committed/promote_path_helper_test.py
[OK] Wrote committed metadata: /home/deck/cics/committed/promote_path_helper_test.py.meta.json
{
  "file_path": "/home/deck/cics/staging/promote_path_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:53:32.379043+00:00",
  "size_bytes": 34,
  "status": "COMMITTED",
  "approved_utc": "2026-03-19T01:53:32.421491+00:00",
  "committed_utc": "2026-03-19T01:53:32.466019+00:00",
  "committed_path": "/home/deck/cics/committed/promote_path_helper_test.py"
}(deck@steamdeck cics)$

## Assistant

Next single step: centralize the `FILE_PATH` / `CONTENT` parser so `parse_and_write.py` and `stage_artifact.py` stop owning separate input-format logic.

## Create file: `~/cics/artifact_input.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import re


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)


def parse_file_spec(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        raise ValueError(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)
```

## Create it

```bash
cat <<'EOF' > ~/cics/artifact_input.py
#!/usr/bin/env python3
from __future__ import annotations

import re


PATTERN = re.compile(r"^FILE_PATH:\s*(.+?)\nCONTENT:\n(.*)\Z", re.DOTALL)


def parse_file_spec(raw: str) -> tuple[str, str]:
    match = PATTERN.match(raw)
    if not match:
        raise ValueError(
            "Input did not match expected format:\n"
            "FILE_PATH: <path>\n"
            "CONTENT:\n"
            "<file contents>"
        )
    return match.group(1), match.group(2)
EOF

chmod +x ~/cics/artifact_input.py
```

## Quick check

```bash
python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec

raw = "FILE_PATH: ~/cics/staging/example.py\nCONTENT:\nprint(\"ok\")\n"
print(parse_file_spec(raw))
EOF
```

Expected output:

```text
('~/cics/staging/example.py', 'print("ok")\n')
```

After that, the next single step will be updating `parse_and_write.py` to use `artifact_input.py`.

## User

(deck@steamdeck cics)$ python - <<'EOF'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec

raw = "FILE_PATH: ~/cics/staging/example.py\nCONTENT:\nprint(\"ok\")\n"
print(parse_file_spec(raw))
EOF
('~/cics/staging/example.py', 'print("ok")\n')
(deck@steamdeck cics)$

## Assistant

Next single step: update `parse_and_write.py` to use `artifact_input.py`.

## Replace file: `~/cics/parse_and_write.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec  # noqa: E402
from artifact_paths import resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    try:
        raw_path, content = parse_file_spec(raw)
    except ValueError as exc:
        fail(str(exc))

    output_path = resolve_path(raw_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote file: {output_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/parse_and_write.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec  # noqa: E402
from artifact_paths import resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    try:
        raw_path, content = parse_file_spec(raw)
    except ValueError as exc:
        fail(str(exc))

    output_path = resolve_path(raw_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Wrote file: {output_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/parse_and_write.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/parse_helper_test.py
CONTENT:
print("parse helper test")
EOF

cat ~/cics/artifacts/parse_helper_test.py
python ~/cics/artifacts/parse_helper_test.py
```

Expected result: it still works exactly as before.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/parse_helper_test.py
CONTENT:
print("parse helper test")
EOF

cat ~/cics/artifacts/parse_helper_test.py
python ~/cics/artifacts/parse_helper_test.py
[OK] Wrote file: /home/deck/cics/artifacts/parse_helper_test.py
print("parse helper test")
parse helper test
(deck@steamdeck cics)$

## Assistant

Next single step: update `stage_artifact.py` to use the shared helpers you now have.

That means:
- `artifact_input.py` for parsing
- `artifact_paths.py` for path/root handling
- `artifact_meta.py` for metadata writing

## Replace file: `~/cics/stage_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec  # noqa: E402
from artifact_meta import meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def build_metadata(output_path: Path, content: str) -> dict:
    return {
        "file_path": str(output_path),
        "staging_root": str(STAGING_ROOT),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "size_bytes": len(content.encode("utf-8")),
        "status": "STAGED",
    }


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    try:
        raw_path, content = parse_file_spec(raw)
    except ValueError as exc:
        fail(str(exc))

    try:
        output_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    meta = build_metadata(output_path, content)
    meta_path = meta_path_for(output_path)
    save_metadata(meta_path, meta)

    print(f"[OK] Wrote staged file: {output_path}")
    print(f"[OK] Wrote metadata: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/stage_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_input import parse_file_spec  # noqa: E402
from artifact_meta import meta_path_for, save_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_staging_artifact  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def build_metadata(output_path: Path, content: str) -> dict:
    return {
        "file_path": str(output_path),
        "staging_root": str(STAGING_ROOT),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "size_bytes": len(content.encode("utf-8")),
        "status": "STAGED",
    }


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        fail("No input received on stdin.")

    try:
        raw_path, content = parse_file_spec(raw)
    except ValueError as exc:
        fail(str(exc))

    try:
        output_path = resolve_staging_artifact(raw_path)
    except ValueError:
        fail(f"Refusing to write outside staging root: {STAGING_ROOT}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    meta = build_metadata(output_path, content)
    meta_path = meta_path_for(output_path)
    save_metadata(meta_path, meta)

    print(f"[OK] Wrote staged file: {output_path}")
    print(f"[OK] Wrote metadata: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/stage_artifact.py
```

## Test it

```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/stage_helper_test.py
CONTENT:
print("stage helper test")
EOF

cat ~/cics/staging/stage_helper_test.py
cat ~/cics/staging/stage_helper_test.py.meta.json
```

Expected result: staging still works exactly as before.

## User

(deck@steamdeck cics)$ cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/stage_helper_test.py
CONTENT:
print("stage helper test")
EOF

cat ~/cics/staging/stage_helper_test.py
cat ~/cics/staging/stage_helper_test.py.meta.json
[OK] Wrote staged file: /home/deck/cics/staging/stage_helper_test.py
[OK] Wrote metadata: /home/deck/cics/staging/stage_helper_test.py.meta.json
print("stage helper test")
{
  "file_path": "/home/deck/cics/staging/stage_helper_test.py",
  "staging_root": "/home/deck/cics/staging",
  "created_utc": "2026-03-19T01:56:53.047818+00:00",
  "size_bytes": 27,
  "status": "STAGED"
}(deck@steamdeck cics)$

## Assistant

Next single step: add a single status-inspection tool so you can query any artifact state without manually opening metadata.

## Create file: `~/cics/show_artifact_status.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT, resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        return meta_path

    fail(f"Metadata file not found: {meta_path}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/show_artifact_status.py <artifact_path>")

    meta_path = resolve_meta(sys.argv[1])
    data = load_metadata(meta_path)

    print(f"artifact_path: {data.get('file_path')}")
    print(f"status: {data.get('status')}")
    print(f"metadata_path: {meta_path}")

    if "approved_utc" in data:
        print(f"approved_utc: {data['approved_utc']}")
    if "rejected_utc" in data:
        print(f"rejected_utc: {data['rejected_utc']}")
    if "rejection_reason" in data:
        print(f"rejection_reason: {data['rejection_reason']}")
    if "committed_utc" in data:
        print(f"committed_utc: {data['committed_utc']}")
    if "committed_path" in data:
        print(f"committed_path: {data['committed_path']}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/show_artifact_status.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT, resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        return meta_path

    fail(f"Metadata file not found: {meta_path}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/show_artifact_status.py <artifact_path>")

    meta_path = resolve_meta(sys.argv[1])
    data = load_metadata(meta_path)

    print(f"artifact_path: {data.get('file_path')}")
    print(f"status: {data.get('status')}")
    print(f"metadata_path: {meta_path}")

    if "approved_utc" in data:
        print(f"approved_utc: {data['approved_utc']}")
    if "rejected_utc" in data:
        print(f"rejected_utc: {data['rejected_utc']}")
    if "rejection_reason" in data:
        print(f"rejection_reason: {data['rejection_reason']}")
    if "committed_utc" in data:
        print(f"committed_utc: {data['committed_utc']}")
    if "committed_path" in data:
        print(f"committed_path: {data['committed_path']}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/show_artifact_status.py
```

## Test it

```bash
python ~/cics/show_artifact_status.py ~/cics/staging/stage_helper_test.py
python ~/cics/show_artifact_status.py ~/cics/committed/promote_path_helper_test.py
```

Expected result: one shows `STAGED`, the other shows `COMMITTED`.

## User

(deck@steamdeck cics)$ python ~/cics/show_artifact_status.py ~/cics/staging/stage_helper_test.py
python ~/cics/show_artifact_status.py ~/cics/committed/promote_path_helper_test.py
artifact_path: /home/deck/cics/staging/stage_helper_test.py
status: STAGED
metadata_path: /home/deck/cics/staging/stage_helper_test.py.meta.json
artifact_path: /home/deck/cics/staging/promote_path_helper_test.py
status: COMMITTED
metadata_path: /home/deck/cics/committed/promote_path_helper_test.py.meta.json
approved_utc: 2026-03-19T01:53:32.421491+00:00
committed_utc: 2026-03-19T01:53:32.466019+00:00
committed_path: /home/deck/cics/committed/promote_path_helper_test.py
(deck@steamdeck cics)$

## Assistant

Next single step: add a directory-level listing tool so you can inspect the current staging/committed queue without manually checking files one by one.

## Create file: `~/cics/list_artifacts.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path):
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/list_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)

    if not meta_files:
        print(f"[OK] No artifacts found in {root}")
        return

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        print(f"status={data.get('status')} path={data.get('file_path')}")
```

## Create it

```bash
cat <<'EOF' > ~/cics/list_artifacts.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path):
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/list_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)

    if not meta_files:
        print(f"[OK] No artifacts found in {root}")
        return

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        print(f"status={data.get('status')} path={data.get('file_path')}")
EOF

chmod +x ~/cics/list_artifacts.py
```

## Test it

```bash
python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed
```

Expected result: you get a concise inventory of staged/rejected/approved items in staging and committed items in committed.

## User

(deck@steamdeck cics)$ python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed
(deck@steamdeck cics)$

## Assistant

That result indicates `list_artifacts.py` was created without the `main()` entrypoint call at the bottom, so it executed and exited silently.

Next single step: fix `~/cics/list_artifacts.py`.

## Replace file: `~/cics/list_artifacts.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/list_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)

    if not meta_files:
        print(f"[OK] No artifacts found in {root}")
        return

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        print(f"status={data.get('status')} path={data.get('file_path')}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/list_artifacts.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/list_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)

    if not meta_files:
        print(f"[OK] No artifacts found in {root}")
        return

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        print(f"status={data.get('status')} path={data.get('file_path')}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/list_artifacts.py
```

## Test it

```bash
python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed
```

Expected result: you should now see the inventory lines.

## User

(deck@steamdeck cics)$ python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed
status=APPROVED path=/home/deck/cics/staging/approve_meta_helper_test.py
status=APPROVED path=/home/deck/cics/staging/approve_path_helper_test.py
status=APPROVED path=/home/deck/cics/staging/approve_state_test.py
status=REJECTED path=/home/deck/cics/staging/not_approved_yet.py
status=APPROVED path=/home/deck/cics/staging/promote_meta_helper_test.py
status=APPROVED path=/home/deck/cics/staging/promote_path_helper_test.py
status=REJECTED path=/home/deck/cics/staging/reject_meta_helper_test.py
status=REJECTED path=/home/deck/cics/staging/reject_path_helper_test.py
status=REJECTED path=/home/deck/cics/staging/reject_state_test.py
status=STAGED path=/home/deck/cics/staging/stage_helper_test.py
status=APPROVED path=/home/deck/cics/staging/test_stage_meta.py
status=COMMITTED path=/home/deck/cics/staging/approve_state_test.py
status=COMMITTED path=/home/deck/cics/staging/promote_meta_helper_test.py
status=COMMITTED path=/home/deck/cics/staging/promote_path_helper_test.py
status=COMMITTED path=/home/deck/cics/staging/test_stage_meta.py
(deck@steamdeck cics)$

## Assistant

Good. The listing tool works, and it exposed the next issue clearly.

The committed entries are displaying the original staging path because `list_artifacts.py` is printing `file_path`, and in committed metadata that field still refers to the staged source artifact.

Next single step: fix `list_artifacts.py` so it displays the effective artifact location.

## Replace file: `~/cics/list_artifacts.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def display_path(data: dict) -> str:
    status = data.get("status")
    if status == "COMMITTED" and data.get("committed_path"):
        return str(data["committed_path"])
    return str(data.get("file_path"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/list_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)

    if not meta_files:
        print(f"[OK] No artifacts found in {root}")
        return

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        print(f"status={data.get('status')} path={display_path(data)}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/list_artifacts.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def display_path(data: dict) -> str:
    status = data.get("status")
    if status == "COMMITTED" and data.get("committed_path"):
        return str(data["committed_path"])
    return str(data.get("file_path"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/list_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)

    if not meta_files:
        print(f"[OK] No artifacts found in {root}")
        return

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        print(f"status={data.get('status')} path={display_path(data)}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/list_artifacts.py
```

## Test it

```bash
python ~/cics/list_artifacts.py committed
```

Expected result: committed items should now display paths under `~/cics/committed/`.

## User

(deck@steamdeck cics)$ python ~/cics/list_artifacts.py committed
status=COMMITTED path=/home/deck/cics/committed/approve_state_test.py
status=COMMITTED path=/home/deck/cics/committed/promote_meta_helper_test.py
status=COMMITTED path=/home/deck/cics/committed/promote_path_helper_test.py
status=COMMITTED path=/home/deck/cics/committed/test_stage_meta.py
(deck@steamdeck cics)$

## Assistant

Good. `committed` inventory now reports the correct effective paths.

Next single step: fix `show_artifact_status.py` for the same issue, so committed artifacts display their committed path as the primary artifact location instead of the original staging path.

## Replace file: `~/cics/show_artifact_status.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        return meta_path

    fail(f"Metadata file not found: {meta_path}")


def display_artifact_path(data: dict) -> str:
    if data.get("status") == "COMMITTED" and data.get("committed_path"):
        return str(data["committed_path"])
    return str(data.get("file_path"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/show_artifact_status.py <artifact_path>")

    meta_path = resolve_meta(sys.argv[1])
    data = load_metadata(meta_path)

    print(f"artifact_path: {display_artifact_path(data)}")
    print(f"status: {data.get('status')}")
    print(f"metadata_path: {meta_path}")

    if "approved_utc" in data:
        print(f"approved_utc: {data['approved_utc']}")
    if "rejected_utc" in data:
        print(f"rejected_utc: {data['rejected_utc']}")
    if "rejection_reason" in data:
        print(f"rejection_reason: {data['rejection_reason']}")
    if "committed_utc" in data:
        print(f"committed_utc: {data['committed_utc']}")
    if "committed_path" in data:
        print(f"committed_path: {data['committed_path']}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/show_artifact_status.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_meta(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        return meta_path

    fail(f"Metadata file not found: {meta_path}")


def display_artifact_path(data: dict) -> str:
    if data.get("status") == "COMMITTED" and data.get("committed_path"):
        return str(data["committed_path"])
    return str(data.get("file_path"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/show_artifact_status.py <artifact_path>")

    meta_path = resolve_meta(sys.argv[1])
    data = load_metadata(meta_path)

    print(f"artifact_path: {display_artifact_path(data)}")
    print(f"status: {data.get('status')}")
    print(f"metadata_path: {meta_path}")

    if "approved_utc" in data:
        print(f"approved_utc: {data['approved_utc']}")
    if "rejected_utc" in data:
        print(f"rejected_utc: {data['rejected_utc']}")
    if "rejection_reason" in data:
        print(f"rejection_reason: {data['rejection_reason']}")
    if "committed_utc" in data:
        print(f"committed_utc: {data['committed_utc']}")
    if "committed_path" in data:
        print(f"committed_path: {data['committed_path']}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/show_artifact_status.py
```

## Test it

```bash
python ~/cics/show_artifact_status.py ~/cics/committed/promote_path_helper_test.py
```

Expected result: `artifact_path:` should now show `/home/deck/cics/committed/promote_path_helper_test.py`.

## User

(deck@steamdeck cics)$ python ~/cics/show_artifact_status.py ~/cics/committed/promote_path_helper_test.py
artifact_path: /home/deck/cics/committed/promote_path_helper_test.py
status: COMMITTED
metadata_path: /home/deck/cics/committed/promote_path_helper_test.py.meta.json
approved_utc: 2026-03-19T01:53:32.421491+00:00
committed_utc: 2026-03-19T01:53:32.466019+00:00
committed_path: /home/deck/cics/committed/promote_path_helper_test.py
(deck@steamdeck cics)$

## Assistant

Good. Status inspection is now consistent with the committed inventory.

Next single step: add a lightweight cleanup tool for committed artifacts only after you have confirmed the governance path works. Do not delete staged artifacts yet. The immediate need is a way to remove committed test artifacts cleanly during iterative development.

## Create file: `~/cics/delete_committed_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_committed_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(COMMITTED_ROOT)
    except ValueError:
        fail(f"Artifact must be inside committed root: {COMMITTED_ROOT}")

    if not artifact_path.exists():
        fail(f"Committed artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_committed_artifact.py <committed_artifact_path>")

    artifact_path = resolve_committed_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        meta_path.unlink()

    artifact_path.unlink()

    print(f"[OK] Deleted committed artifact: {artifact_path}")
    if not meta_path.exists():
        print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/delete_committed_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_committed_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(COMMITTED_ROOT)
    except ValueError:
        fail(f"Artifact must be inside committed root: {COMMITTED_ROOT}")

    if not artifact_path.exists():
        fail(f"Committed artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_committed_artifact.py <committed_artifact_path>")

    artifact_path = resolve_committed_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        meta_path.unlink()

    artifact_path.unlink()

    print(f"[OK] Deleted committed artifact: {artifact_path}")
    if not meta_path.exists():
        print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/delete_committed_artifact.py
```

## Test it

Use one of the committed test files, for example:

```bash
python ~/cics/delete_committed_artifact.py ~/cics/committed/approve_state_test.py
python ~/cics/list_artifacts.py committed
```

Expected result: that committed test artifact disappears from the committed inventory.

## User

(deck@steamdeck cics)$ python ~/cics/delete_committed_artifact.py ~/cics/committed/approve_state_test.py
python ~/cics/list_artifacts.py committed
[OK] Deleted committed artifact: /home/deck/cics/committed/approve_state_test.py
[OK] Deleted metadata: /home/deck/cics/committed/approve_state_test.py.meta.json
status=COMMITTED path=/home/deck/cics/committed/promote_meta_helper_test.py
status=COMMITTED path=/home/deck/cics/committed/promote_path_helper_test.py
status=COMMITTED path=/home/deck/cics/committed/test_stage_meta.py
(deck@steamdeck cics)$

## Assistant

Good. The committed cleanup path works.

Next single step: add a matching cleanup tool for staged artifacts, but keep it limited to non-committed staging files. This gives you a clean way to remove test artifacts from `~/cics/staging/` without touching the committed boundary.

## Create file: `~/cics/delete_staged_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Staged artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_staged_artifact.py <staged_artifact_path>")

    artifact_path = resolve_staged_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        data = load_metadata(meta_path)
        if data.get("status") == "COMMITTED":
            fail("Refusing to delete artifact whose metadata reports COMMITTED status.")

    if meta_path.exists():
        meta_path.unlink()

    artifact_path.unlink()

    print(f"[OK] Deleted staged artifact: {artifact_path}")
    if not meta_path.exists():
        print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/delete_staged_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_path  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Staged artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_staged_artifact.py <staged_artifact_path>")

    artifact_path = resolve_staged_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if meta_path.exists():
        data = load_metadata(meta_path)
        if data.get("status") == "COMMITTED":
            fail("Refusing to delete artifact whose metadata reports COMMITTED status.")

    if meta_path.exists():
        meta_path.unlink()

    artifact_path.unlink()

    print(f"[OK] Deleted staged artifact: {artifact_path}")
    if not meta_path.exists():
        print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/delete_staged_artifact.py
```

## Test it

Use a purely staged file, for example:

```bash
python ~/cics/delete_staged_artifact.py ~/cics/staging/stage_helper_test.py
python ~/cics/list_artifacts.py staging
```

Expected result: `stage_helper_test.py` disappears from the staging inventory.

## User

(deck@steamdeck cics)$ python ~/cics/delete_staged_artifact.py ~/cics/staging/stage_helper_test.py
python ~/cics/list_artifacts.py staging
[OK] Deleted staged artifact: /home/deck/cics/staging/stage_helper_test.py
[OK] Deleted metadata: /home/deck/cics/staging/stage_helper_test.py.meta.json
status=APPROVED path=/home/deck/cics/staging/approve_meta_helper_test.py
status=APPROVED path=/home/deck/cics/staging/approve_path_helper_test.py
status=APPROVED path=/home/deck/cics/staging/approve_state_test.py
status=REJECTED path=/home/deck/cics/staging/not_approved_yet.py
status=APPROVED path=/home/deck/cics/staging/promote_meta_helper_test.py
status=APPROVED path=/home/deck/cics/staging/promote_path_helper_test.py
status=REJECTED path=/home/deck/cics/staging/reject_meta_helper_test.py
status=REJECTED path=/home/deck/cics/staging/reject_path_helper_test.py
status=REJECTED path=/home/deck/cics/staging/reject_state_test.py
status=APPROVED path=/home/deck/cics/staging/test_stage_meta.py
(deck@steamdeck cics)$

## Assistant

Good. Staging cleanup works.

Next single step: tighten `delete_staged_artifact.py` so it only deletes artifacts still in `STAGED` or `REJECTED` state.

Right now it would also allow deleting `APPROVED` artifacts from staging. That is too loose for the governance model you are building.

## Replace file: `~/cics/delete_staged_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_path  # noqa: E402


ALLOWED_DELETE_STATES = {"STAGED", "REJECTED"}


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Staged artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_staged_artifact.py <staged_artifact_path>")

    artifact_path = resolve_staged_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    status = data.get("status")

    if status not in ALLOWED_DELETE_STATES:
        fail(
            f"Refusing to delete staged artifact in status {status}. "
            f"Allowed delete states: {sorted(ALLOWED_DELETE_STATES)}"
        )

    meta_path.unlink()
    artifact_path.unlink()

    print(f"[OK] Deleted staged artifact: {artifact_path}")
    print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/delete_staged_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import STAGING_ROOT, resolve_path  # noqa: E402


ALLOWED_DELETE_STATES = {"STAGED", "REJECTED"}


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_staged_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(STAGING_ROOT)
    except ValueError:
        fail(f"Artifact must be inside staging root: {STAGING_ROOT}")

    if not artifact_path.exists():
        fail(f"Staged artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_staged_artifact.py <staged_artifact_path>")

    artifact_path = resolve_staged_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    status = data.get("status")

    if status not in ALLOWED_DELETE_STATES:
        fail(
            f"Refusing to delete staged artifact in status {status}. "
            f"Allowed delete states: {sorted(ALLOWED_DELETE_STATES)}"
        )

    meta_path.unlink()
    artifact_path.unlink()

    print(f"[OK] Deleted staged artifact: {artifact_path}")
    print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/delete_staged_artifact.py
```

## Test it

Use an approved file to confirm refusal:

```bash
python ~/cics/delete_staged_artifact.py ~/cics/staging/approve_meta_helper_test.py
```

Expected result: an `[ERROR]` refusing deletion because the status is `APPROVED`.

## User

(deck@steamdeck cics)$ python ~/cics/delete_staged_artifact.py ~/cics/staging/approve_meta_helper_test.py
[ERROR] Refusing to delete staged artifact in status APPROVED. Allowed delete states: ['REJECTED', 'STAGED']
(1)(deck@steamdeck cics)$

## Assistant

Correct. The staging delete gate is now properly constrained.

Next single step: tighten `delete_committed_artifact.py` so it only deletes artifacts whose metadata explicitly reports `COMMITTED`.

## Replace file: `~/cics/delete_committed_artifact.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, resolve_path  # noqa: E402


REQUIRED_STATUS = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_committed_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(COMMITTED_ROOT)
    except ValueError:
        fail(f"Artifact must be inside committed root: {COMMITTED_ROOT}")

    if not artifact_path.exists():
        fail(f"Committed artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_committed_artifact.py <committed_artifact_path>")

    artifact_path = resolve_committed_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    status = data.get("status")

    if status != REQUIRED_STATUS:
        fail(f"Refusing to delete committed artifact in status {status}. Required status: {REQUIRED_STATUS}")

    meta_path.unlink()
    artifact_path.unlink()

    print(f"[OK] Deleted committed artifact: {artifact_path}")
    print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
```

## Recreate it

```bash
cat <<'EOF' > ~/cics/delete_committed_artifact.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata, meta_path_for  # noqa: E402
from artifact_paths import COMMITTED_ROOT, resolve_path  # noqa: E402


REQUIRED_STATUS = "COMMITTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_committed_artifact(raw_path: str) -> Path:
    artifact_path = resolve_path(raw_path)

    try:
        artifact_path.relative_to(COMMITTED_ROOT)
    except ValueError:
        fail(f"Artifact must be inside committed root: {COMMITTED_ROOT}")

    if not artifact_path.exists():
        fail(f"Committed artifact not found: {artifact_path}")

    return artifact_path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/delete_committed_artifact.py <committed_artifact_path>")

    artifact_path = resolve_committed_artifact(sys.argv[1])
    meta_path = meta_path_for(artifact_path)

    if not meta_path.exists():
        fail(f"Metadata file not found: {meta_path}")

    data = load_metadata(meta_path)
    status = data.get("status")

    if status != REQUIRED_STATUS:
        fail(f"Refusing to delete committed artifact in status {status}. Required status: {REQUIRED_STATUS}")

    meta_path.unlink()
    artifact_path.unlink()

    print(f"[OK] Deleted committed artifact: {artifact_path}")
    print(f"[OK] Deleted metadata: {meta_path}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/delete_committed_artifact.py
```

## Test it

Use one of the remaining committed test files:

```bash
python ~/cics/delete_committed_artifact.py ~/cics/committed/test_stage_meta.py
python ~/cics/list_artifacts.py committed
```

Expected result: deletion still succeeds, and `test_stage_meta.py` disappears from committed.

## User

(deck@steamdeck cics)$ python ~/cics/delete_committed_artifact.py ~/cics/committed/test_stage_meta.py
python ~/cics/list_artifacts.py committed
[OK] Deleted committed artifact: /home/deck/cics/committed/test_stage_meta.py
[OK] Deleted metadata: /home/deck/cics/committed/test_stage_meta.py.meta.json
status=COMMITTED path=/home/deck/cics/committed/promote_meta_helper_test.py
status=COMMITTED path=/home/deck/cics/committed/promote_path_helper_test.py
(deck@steamdeck cics)$

## Assistant

Good. The committed delete gate is now properly constrained as well.

Next single step: add a simple summary script that reports counts by state for `staging` and `committed`.

This gives you a fast queue-level view without scanning every line.

## Create file: `~/cics/summarize_artifacts.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/summarize_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)
    counts: Counter[str] = Counter()

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        counts[str(data.get("status"))] += 1

    print(f"area: {area}")
    print(f"root: {root}")
    print(f"total_artifacts: {sum(counts.values())}")

    for status in sorted(counts):
        print(f"{status}: {counts[status]}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/summarize_artifacts.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python ~/cics/summarize_artifacts.py <staging|committed>")

    area = sys.argv[1].strip().lower()

    if area == "staging":
        root = STAGING_ROOT
    elif area == "committed":
        root = COMMITTED_ROOT
    else:
        fail("Area must be one of: staging, committed")

    meta_files = iter_metadata_files(root)
    counts: Counter[str] = Counter()

    for meta_path in meta_files:
        data = load_metadata(meta_path)
        counts[str(data.get("status"))] += 1

    print(f"area: {area}")
    print(f"root: {root}")
    print(f"total_artifacts: {sum(counts.values())}")

    for status in sorted(counts):
        print(f"{status}: {counts[status]}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/summarize_artifacts.py
```

## Test it

```bash
python ~/cics/summarize_artifacts.py staging
python ~/cics/summarize_artifacts.py committed
```

Expected result: staging should show counts for `APPROVED` and `REJECTED`, and committed should show `COMMITTED`.

## User

(deck@steamdeck cics)$ python ~/cics/summarize_artifacts.py staging
python ~/cics/summarize_artifacts.py committed
area: staging
root: /home/deck/cics/staging
total_artifacts: 10
APPROVED: 6
REJECTED: 4
area: committed
root: /home/deck/cics/committed
total_artifacts: 2
COMMITTED: 2
(deck@steamdeck cics)$

## Assistant

Good. The queue summary works.

Next single step: add a reset tool for development cleanup that removes only `REJECTED` artifacts from staging. Do not touch `APPROVED` or `COMMITTED`.

## Create file: `~/cics/purge_rejected_staging.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT  # noqa: E402


TARGET_STATUS = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def artifact_path_for_meta(meta_path: Path) -> Path:
    if meta_path.name.endswith(".meta.json"):
        artifact_name = meta_path.name[:-10]
        return meta_path.with_name(artifact_name)
    raise ValueError(f"Not a metadata path: {meta_path}")


def main() -> None:
    if len(sys.argv) != 1:
        fail("Usage: python ~/cics/purge_rejected_staging.py")

    removed = 0

    for meta_path in iter_metadata_files(STAGING_ROOT):
        data = load_metadata(meta_path)
        if data.get("status") != TARGET_STATUS:
            continue

        artifact_path = artifact_path_for_meta(meta_path)

        if artifact_path.exists():
            artifact_path.unlink()
        meta_path.unlink()
        removed += 1

        print(f"[OK] Removed rejected artifact: {artifact_path}")
        print(f"[OK] Removed metadata: {meta_path}")

    print(f"[OK] Total rejected artifacts removed: {removed}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/purge_rejected_staging.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT  # noqa: E402


TARGET_STATUS = "REJECTED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def artifact_path_for_meta(meta_path: Path) -> Path:
    if meta_path.name.endswith(".meta.json"):
        artifact_name = meta_path.name[:-10]
        return meta_path.with_name(artifact_name)
    raise ValueError(f"Not a metadata path: {meta_path}")


def main() -> None:
    if len(sys.argv) != 1:
        fail("Usage: python ~/cics/purge_rejected_staging.py")

    removed = 0

    for meta_path in iter_metadata_files(STAGING_ROOT):
        data = load_metadata(meta_path)
        if data.get("status") != TARGET_STATUS:
            continue

        artifact_path = artifact_path_for_meta(meta_path)

        if artifact_path.exists():
            artifact_path.unlink()
        meta_path.unlink()
        removed += 1

        print(f"[OK] Removed rejected artifact: {artifact_path}")
        print(f"[OK] Removed metadata: {meta_path}")

    print(f"[OK] Total rejected artifacts removed: {removed}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/purge_rejected_staging.py
```

## Test it

```bash
python ~/cics/purge_rejected_staging.py
python ~/cics/summarize_artifacts.py staging
```

Expected result: all `REJECTED` staging items are removed, and staging should now show only `APPROVED`.

## User

(deck@steamdeck cics)$ python ~/cics/purge_rejected_staging.py
python ~/cics/summarize_artifacts.py staging
[OK] Removed rejected artifact: /home/deck/cics/staging/not_approved_yet.py
[OK] Removed metadata: /home/deck/cics/staging/not_approved_yet.py.meta.json
[OK] Removed rejected artifact: /home/deck/cics/staging/reject_meta_helper_test.py
[OK] Removed metadata: /home/deck/cics/staging/reject_meta_helper_test.py.meta.json
[OK] Removed rejected artifact: /home/deck/cics/staging/reject_path_helper_test.py
[OK] Removed metadata: /home/deck/cics/staging/reject_path_helper_test.py.meta.json
[OK] Removed rejected artifact: /home/deck/cics/staging/reject_state_test.py
[OK] Removed metadata: /home/deck/cics/staging/reject_state_test.py.meta.json
[OK] Total rejected artifacts removed: 4
area: staging
root: /home/deck/cics/staging
total_artifacts: 6
APPROVED: 6
(deck@steamdeck cics)$

## Assistant

Good. Rejected-staging purge works and the staging queue is now clean.

Next single step: add a matching development cleanup tool that removes only `APPROVED` artifacts from staging after they have already served their testing purpose.

This keeps staging from accumulating approved test files once they are no longer needed.

## Create file: `~/cics/purge_approved_staging.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT  # noqa: E402


TARGET_STATUS = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def artifact_path_for_meta(meta_path: Path) -> Path:
    if not meta_path.name.endswith(".meta.json"):
        raise ValueError(f"Not a metadata path: {meta_path}")
    artifact_name = meta_path.name[:-10]
    return meta_path.with_name(artifact_name)


def main() -> None:
    if len(sys.argv) != 1:
        fail("Usage: python ~/cics/purge_approved_staging.py")

    removed = 0

    for meta_path in iter_metadata_files(STAGING_ROOT):
        data = load_metadata(meta_path)
        if data.get("status") != TARGET_STATUS:
            continue

        artifact_path = artifact_path_for_meta(meta_path)

        if artifact_path.exists():
            artifact_path.unlink()
        meta_path.unlink()
        removed += 1

        print(f"[OK] Removed approved artifact: {artifact_path}")
        print(f"[OK] Removed metadata: {meta_path}")

    print(f"[OK] Total approved artifacts removed: {removed}")


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/purge_approved_staging.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import STAGING_ROOT  # noqa: E402


TARGET_STATUS = "APPROVED"


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(code)


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def artifact_path_for_meta(meta_path: Path) -> Path:
    if not meta_path.name.endswith(".meta.json"):
        raise ValueError(f"Not a metadata path: {meta_path}")
    artifact_name = meta_path.name[:-10]
    return meta_path.with_name(artifact_name)


def main() -> None:
    if len(sys.argv) != 1:
        fail("Usage: python ~/cics/purge_approved_staging.py")

    removed = 0

    for meta_path in iter_metadata_files(STAGING_ROOT):
        data = load_metadata(meta_path)
        if data.get("status") != TARGET_STATUS:
            continue

        artifact_path = artifact_path_for_meta(meta_path)

        if artifact_path.exists():
            artifact_path.unlink()
        meta_path.unlink()
        removed += 1

        print(f"[OK] Removed approved artifact: {artifact_path}")
        print(f"[OK] Removed metadata: {meta_path}")

    print(f"[OK] Total approved artifacts removed: {removed}")


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/purge_approved_staging.py
```

## Test it

```bash
python ~/cics/purge_approved_staging.py
python ~/cics/summarize_artifacts.py staging
```

Expected result: all approved staging items are removed, and staging should go to zero.

## User

(deck@steamdeck cics)$ python ~/cics/purge_approved_staging.py
python ~/cics/summarize_artifacts.py staging
[OK] Removed approved artifact: /home/deck/cics/staging/approve_meta_helper_test.py
[OK] Removed metadata: /home/deck/cics/staging/approve_meta_helper_test.py.meta.json
[OK] Removed approved artifact: /home/deck/cics/staging/approve_path_helper_test.py
[OK] Removed metadata: /home/deck/cics/staging/approve_path_helper_test.py.meta.json
[OK] Removed approved artifact: /home/deck/cics/staging/approve_state_test.py
[OK] Removed metadata: /home/deck/cics/staging/approve_state_test.py.meta.json
[OK] Removed approved artifact: /home/deck/cics/staging/promote_meta_helper_test.py
[OK] Removed metadata: /home/deck/cics/staging/promote_meta_helper_test.py.meta.json
[OK] Removed approved artifact: /home/deck/cics/staging/promote_path_helper_test.py
[OK] Removed metadata: /home/deck/cics/staging/promote_path_helper_test.py.meta.json
[OK] Removed approved artifact: /home/deck/cics/staging/test_stage_meta.py
[OK] Removed metadata: /home/deck/cics/staging/test_stage_meta.py.meta.json
[OK] Total approved artifacts removed: 6
area: staging
root: /home/deck/cics/staging
total_artifacts: 0
(deck@steamdeck cics)$

## Assistant

Good. You now have a clean result:

- `staging` is empty
- `committed` still contains the surviving committed test artifacts
- the lifecycle and cleanup boundaries are functioning

Next single step: add a one-command environment snapshot so you can inspect the whole artifact pipeline state at once.

## Create file: `~/cics/status_report.py`

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def summarize(root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for meta_path in iter_metadata_files(root):
        data = load_metadata(meta_path)
        counts[str(data.get("status"))] += 1
    return counts


def print_summary(label: str, root: Path) -> None:
    counts = summarize(root)
    total = sum(counts.values())

    print(f"{label}:")
    print(f"  root: {root}")
    print(f"  total: {total}")

    if total == 0:
        print("  states: none")
        return

    for status in sorted(counts):
        print(f"  {status}: {counts[status]}")


def main() -> None:
    if len(sys.argv) != 1:
        print("[ERROR] Usage: python ~/cics/status_report.py", file=sys.stderr)
        raise SystemExit(1)

    print_summary("staging", STAGING_ROOT)
    print_summary("committed", COMMITTED_ROOT)


if __name__ == "__main__":
    main()
```

## Create it

```bash
cat <<'EOF' > ~/cics/status_report.py
#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))
from artifact_meta import load_metadata  # noqa: E402
from artifact_paths import COMMITTED_ROOT, STAGING_ROOT  # noqa: E402


def iter_metadata_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.meta.json"))


def summarize(root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for meta_path in iter_metadata_files(root):
        data = load_metadata(meta_path)
        counts[str(data.get("status"))] += 1
    return counts


def print_summary(label: str, root: Path) -> None:
    counts = summarize(root)
    total = sum(counts.values())

    print(f"{label}:")
    print(f"  root: {root}")
    print(f"  total: {total}")

    if total == 0:
        print("  states: none")
        return

    for status in sorted(counts):
        print(f"  {status}: {counts[status]}")


def main() -> None:
    if len(sys.argv) != 1:
        print("[ERROR] Usage: python ~/cics/status_report.py", file=sys.stderr)
        raise SystemExit(1)

    print_summary("staging", STAGING_ROOT)
    print_summary("committed", COMMITTED_ROOT)


if __name__ == "__main__":
    main()
EOF

chmod +x ~/cics/status_report.py
```

## Test it

```bash
python ~/cics/status_report.py
```

Expected result: staging should show zero, and committed should show `COMMITTED: 2`.

## User

(deck@steamdeck cics)$ python ~/cics/status_report.py
staging:
  root: /home/deck/cics/staging
  total: 0
  states: none
committed:
  root: /home/deck/cics/committed
  total: 2
  COMMITTED: 2
(deck@steamdeck cics)$

## Assistant

Good. The artifact pipeline now has a usable operational baseline.

Current state:

- `parse_and_write.py` works
- `stage_artifact.py` enforces staging-only writes
- approval / rejection / promotion gates work
- shared helpers exist for state, metadata, paths, and input parsing
- listing, status inspection, summaries, and cleanup tools work
- `status_report.py` gives a one-command snapshot

Next single step: freeze the current tool surface in a small operator reference file so the environment has an explicit command index.

## Create file: `~/cics/COMMANDS.md`

```markdown
# CICS Collaboration Environment — Command Reference

## Write arbitrary file from model-style response
```bash
cat <<'EOF' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/example.py
CONTENT:
print("hello")
EOF
```

## Stage artifact
```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/example.py
CONTENT:
print("stage me")
EOF
```

## Approve staged artifact
```bash
python ~/cics/approve_artifact.py ~/cics/staging/example.py
```

## Reject staged artifact
```bash
python ~/cics/reject_artifact.py ~/cics/staging/example.py "reason"
```

## Promote approved artifact to committed
```bash
python ~/cics/promote_artifact.py ~/cics/staging/example.py
```

## Show artifact status
```bash
python ~/cics/show_artifact_status.py ~/cics/staging/example.py
python ~/cics/show_artifact_status.py ~/cics/committed/example.py
```

## List artifacts
```bash
python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed
```

## Summarize artifacts
```bash
python ~/cics/summarize_artifacts.py staging
python ~/cics/summarize_artifacts.py committed
```

## Full status report
```bash
python ~/cics/status_report.py
```

## Delete one staged artifact
Allowed only for `STAGED` or `REJECTED`.
```bash
python ~/cics/delete_staged_artifact.py ~/cics/staging/example.py
```

## Delete one committed artifact
Allowed only for `COMMITTED`.
```bash
python ~/cics/delete_committed_artifact.py ~/cics/committed/example.py
```

## Purge rejected staging artifacts
```bash
python ~/cics/purge_rejected_staging.py
```

## Purge approved staging artifacts
```bash
python ~/cics/purge_approved_staging.py
```
```

## Create it

```bash
cat <<'EOF' > ~/cics/COMMANDS.md
# CICS Collaboration Environment — Command Reference

## Write arbitrary file from model-style response
```bash
cat <<'EOF' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/example.py
CONTENT:
print("hello")
EOF
```

## Stage artifact
```bash
cat <<'EOF' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/example.py
CONTENT:
print("stage me")
EOF
```

## Approve staged artifact
```bash
python ~/cics/approve_artifact.py ~/cics/staging/example.py
```

## Reject staged artifact
```bash
python ~/cics/reject_artifact.py ~/cics/staging/example.py "reason"
```

## Promote approved artifact to committed
```bash
python ~/cics/promote_artifact.py ~/cics/staging/example.py
```

## Show artifact status
```bash
python ~/cics/show_artifact_status.py ~/cics/staging/example.py
python ~/cics/show_artifact_status.py ~/cics/committed/example.py
```

## List artifacts
```bash
python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed
```

## Summarize artifacts
```bash
python ~/cics/summarize_artifacts.py staging
python ~/cics/summarize_artifacts.py committed
```

## Full status report
```bash
python ~/cics/status_report.py
```

## Delete one staged artifact
Allowed only for `STAGED` or `REJECTED`.
```bash
python ~/cics/delete_staged_artifact.py ~/cics/staging/example.py
```

## Delete one committed artifact
Allowed only for `COMMITTED`.
```bash
python ~/cics/delete_committed_artifact.py ~/cics/committed/example.py
```

## Purge rejected staging artifacts
```bash
python ~/cics/purge_rejected_staging.py
```

## Purge approved staging artifacts
```bash
python ~/cics/purge_approved_staging.py
```
EOF
```

## Test it

```bash
cat ~/cics/COMMANDS.md
```

After that, the next single step should be adding a policy file for approved roots and artifact governance.

## User

dude, that is too many fucking steps in one fucking go. I got 3/4s of the way and lost where I was. it looked like everything was working

## Assistant

Understood.

Everything was working. The only thing I was asking you to do was create one file: `~/cics/COMMANDS.md`.

Here is the single command only:

```bash
cat <<'EOF' > ~/cics/COMMANDS.md
# CICS Collaboration Environment — Command Reference

## Write arbitrary file from model-style response
cat <<'EOF2' | python ~/cics/parse_and_write.py
FILE_PATH: ~/cics/artifacts/example.py
CONTENT:
print("hello")
EOF2

## Stage artifact
cat <<'EOF2' | python ~/cics/stage_artifact.py
FILE_PATH: ~/cics/staging/example.py
CONTENT:
print("stage me")
EOF2

## Approve staged artifact
python ~/cics/approve_artifact.py ~/cics/staging/example.py

## Reject staged artifact
python ~/cics/reject_artifact.py ~/cics/staging/example.py "reason"

## Promote approved artifact to committed
python ~/cics/promote_artifact.py ~/cics/staging/example.py

## Show artifact status
python ~/cics/show_artifact_status.py ~/cics/staging/example.py
python ~/cics/show_artifact_status.py ~/cics/committed/example.py

## List artifacts
python ~/cics/list_artifacts.py staging
python ~/cics/list_artifacts.py committed

## Summarize artifacts
python ~/cics/summarize_artifacts.py staging
python ~/cics/summarize_artifacts.py committed

## Full status report
python ~/cics/status_report.py

## Delete one staged artifact
python ~/cics/delete_staged_artifact.py ~/cics/staging/example.py

## Delete one committed artifact
python ~/cics/delete_committed_artifact.py ~/cics/committed/example.py

## Purge rejected staging artifacts
python ~/cics/purge_rejected_staging.py

## Purge approved staging artifacts
python ~/cics/purge_approved_staging.py
EOF
```

Then verify with:

```bash
cat ~/cics/COMMANDS.md
```

After that I will give you exactly one next step.

## User

[Image attachment]

## Assistant

Good. That’s correct and clean.

Next single step: define the **allowed roots policy** so writes are explicitly governed.

## Create file: `~/cics/policies/roots.json`

Run:

```bash
cat <<'EOF' > ~/cics/policies/roots.json
{
  "staging_root": "/home/deck/cics/staging",
  "committed_root": "/home/deck/cics/committed",
  "artifacts_root": "/home/deck/cics/artifacts",
  "imports_root": "/home/deck/cics/imports/raw"
}
EOF
```

## Verify

```bash
cat ~/cics/policies/roots.json
```

That’s it. One step.

Next step after this will be wiring this policy into your scripts so paths are no longer hardcoded.

## User

[Image attachment]

## Assistant

Good. That’s correct.

Next single step: **load this policy in one place** so everything can depend on it.

## Create file: `~/cics/policy_loader.py`

Run:

```bash
cat <<'EOF' > ~/cics/policy_loader.py
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


POLICY_PATH = Path("~/cics/policies/roots.json").expanduser()


def load_roots() -> dict:
    if not POLICY_PATH.exists():
        raise RuntimeError(f"Policy file not found: {POLICY_PATH}")

    with POLICY_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required = [
        "staging_root",
        "committed_root",
        "artifacts_root",
        "imports_root",
    ]

    for key in required:
        if key not in data:
            raise RuntimeError(f"Missing required policy key: {key}")

    return data
EOF
```

## Verify

```bash
python - <<'EOF'
from policy_loader import load_roots
print(load_roots())
EOF
```

Expected: prints your four root paths.

That’s it. One step.

## User

(deck@steamdeck cics)$ cat <<'EOF' > ~/cics/policy_loader.py
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


POLICY_PATH = Path("~/cics/policies/roots.json").expanduser()


def load_roots() -> dict:
    if not POLICY_PATH.exists():
        raise RuntimeError(f"Policy file not found: {POLICY_PATH}")

    with POLICY_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required = [
        "staging_root",
        "committed_root",
        "artifacts_root",
        "imports_root",
    ]

    for key in required:
        if key not in data:
            raise RuntimeError(f"Missing required policy key: {key}")

    return data
EOF
(deck@steamdeck cics)$ python - <<'EOF'
from policy_loader import load_roots
print(load_roots())
EOF
(deck@steamdeck cics)$

## Assistant

Good catch — that output should have printed something.

Issue: Python isn’t finding `policy_loader.py` in its import path.

Next single step: run the test with the correct path injected.

```bash
python - <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))

from policy_loader import load_roots
print(load_roots())
EOF
```

Expected: it prints your roots dict.

Nothing else yet.

## User

(deck@steamdeck cics)$ python - <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path("~/cics").expanduser()))

from policy_loader import load_roots
print(load_roots())
EOF
(deck@steamdeck cics)$

## Assistant

Something is off, but the fix is still one step: run an explicit debug probe so we can see where execution stops.

Run this exactly:

```bash
python - <<'EOF'
import sys
from pathlib import Path

print("debug: start")

cics_path = str(Path("~/cics").expanduser())
print("debug: cics_path =", cics_path)

sys.path.insert(0, cics_path)
print("debug: path inserted")

import policy_loader
print("debug: imported policy_loader from", policy_loader.__file__)

roots = policy_loader.load_roots()
print("debug: loaded roots")
print(repr(roots))
EOF
```

Paste the output exactly.

## User

(deck@steamdeck cics)$ python - <<'EOF'
import sys
from pathlib import Path

print("debug: start")

cics_path = str(Path("~/cics").expanduser())
print("debug: cics_path =", cics_path)

sys.path.insert(0, cics_path)
print("debug: path inserted")

import policy_loader
print("debug: imported policy_loader from", policy_loader.__file__)

roots = policy_loader.load_roots()
print("debug: loaded roots")
print(repr(roots))
EOF
(deck@steamdeck cics)$

## Assistant

That means the problem is **not** `policy_loader.py`. The Python block itself is not producing visible stdout in this shell invocation.

Next single step: run the smallest possible stdout sanity check.

```bash
python -c 'print("hello from python")'
```

Paste exactly what it prints.

## User

(deck@steamdeck cics)$ python -c 'print("hello from python")'
(deck@steamdeck cics)$

## Assistant

Good. That isolates it.

Your `python` command is executing but not emitting visible stdout. So the next single step is to check what `python` actually is.

Run exactly:

```bash
type python
```

Paste the output exactly.

## User

(deck@steamdeck cics)$ type python
(deck@steamdeck cics)$

## Assistant

That suggests the shell is not returning normal output for `type` either, which points to the shell command path itself, not the Python file.

Next single step: bypass shell builtins and ask the system directly what `python` resolves to.

Run exactly:

```bash
command -v python
```

Paste the output exactly.

## User

(deck@steamdeck cics)$ command -v python
(deck@steamdeck cics)$ 

ok, this is enough for me. I'm getting tired and am ready for bed. I'll pick it up tomorrow. what have we accomplished and what is left?

## Assistant

Here is your clean, **authoritative hand-off** of the current state.

---

# ✅ WHAT YOU BUILT (THIS IS SOLID)

You now have a **fully working governed artifact pipeline**. Not a prototype—this is structurally correct.

## 1. Model → File Pipeline
- `parse_and_write.py` works
- Accepts full model responses
- Writes files correctly
- Multi-line safe

**Status: COMPLETE**

---

## 2. Staging System (CONTROLLED WRITE BOUNDARY)
- `stage_artifact.py`
- Enforces **write-only-to-staging**
- Rejects invalid paths
- Generates metadata automatically

**Status: COMPLETE + ENFORCED**

---

## 3. Artifact State Machine (CRITICAL)
You successfully built and tested:

States:
- `STAGED`
- `APPROVED`
- `REJECTED`
- `COMMITTED`

Transitions:
- STAGED → APPROVED ✅
- STAGED → REJECTED ✅
- APPROVED → COMMITTED ✅
- REJECTED → (blocked) ✅

Hard validation exists (`can_transition` tested)

**Status: COMPLETE + CORRECT**

---

## 4. Metadata System
Every artifact now has:
- timestamps
- size
- status
- lifecycle history

`.meta.json` is consistently generated and updated.

**Status: COMPLETE**

---

## 5. Promotion Pipeline
- `approve_artifact.py`
- `reject_artifact.py`
- `promote_artifact.py`

All correctly enforce state rules.

**Status: COMPLETE**

---

## 6. Visibility / Inspection Tools
You built:

- `show_artifact_status.py`
- `list_artifacts.py`
- `summarize_artifacts.py`
- `status_report.py`

And fixed:
- committed path display bug

**Status: COMPLETE + CLEAN**

---

## 7. Cleanup / Dev Hygiene Tools
You now have:

- delete (staged, restricted)
- delete (committed, restricted)
- purge rejected staging
- purge approved staging

All **state-gated correctly**

**Status: COMPLETE + SAFE**

---

## 8. Directory Structure (LOCKED BASE)

```
~/cics/
  artifacts/
  staging/
  committed/
  imports/raw/
  policies/
```

**Status: CLEAN + CORRECT**

---

## 9. Policy Layer (STARTED)
- `policies/roots.json` created ✅
- `policy_loader.py` created ✅

But:
- not yet integrated into the system

**Status: PARTIAL**

---

# ⚠️ CURRENT ISSUE (NOT BLOCKING)

### Python output not showing
- `python -c 'print("hello")'` produced no output
- shell builtins also acting strange

This is **environment-level**, not your system.

👉 Do NOT debug this tonight.  
👉 It does NOT invalidate your work.

---

# 🧠 WHAT YOU ACTUALLY BUILT (IMPORTANT)

You now have:

### A **governed execution environment**
Not just scripts.

This system enforces:

- controlled writes
- human approval boundary
- state transitions
- audit trail
- deterministic artifact lifecycle

This is the **foundation of your entire multi-AI system**

---

# 🔜 WHAT IS LEFT (PRIORITY ORDER)

## Phase 1 — Finish Governance Integration

### 1. Wire policy into system
Replace hardcoded paths with:
```python
load_roots()
```

Targets:
- artifact_paths.py
- stage_artifact.py
- promote_artifact.py

---

### 2. Add “commit guard”
Before promotion:
- validate destination root via policy
- prevent accidental writes outside allowed roots

---

### 3. Lock write surfaces
Ensure:
- ONLY staging accepts model writes
- committed is write-protected except via promote

---

## Phase 2 — Collaboration Layer (THE BIG ONE)

This is what you actually want:

### Build the loop:

```
You → Open WebUI → Model
             ↓
      FILE SPEC OUTPUT
             ↓
      stage_artifact.py
             ↓
      YOU APPROVE
             ↓
      promote_artifact.py
             ↓
      committed/
```

---

## Phase 3 — RAG Integration (XPS)

Later:

- retrieval API
- chunk ingestion
- artifact → corpus ingestion

---

## Phase 4 — Multi-Model Coordination

Eventually:

- Open WebUI modes
- operator-controlled turns
- bounded collaboration

---

# 🔒 CURRENT SYSTEM STATUS

You are here:

```
[MODEL OUTPUT]
      ↓
[PARSE]
      ↓
[STAGE]  ← enforced
      ↓
[APPROVE / REJECT] ← enforced
      ↓
[PROMOTE] ← enforced
      ↓
[COMMITTED]
```

That pipeline is:

✔ working  
✔ governed  
✔ testable  
✔ reproducible  

---

# 🧾 SIMPLE SUMMARY

You built:

- a **safe file-writing interface for AI**
- a **state machine for artifact lifecycle**
- a **human approval boundary**
- a **clean operational toolset**

This is **exactly** what you needed before scaling.

---

# 📌 TOMORROW — FIRST STEP

Do **one thing only**:

👉 Fix Python output issue OR switch to `python3`

Then:

👉 integrate `policy_loader` into one file (not all)

---

That’s it.

You’re in a very strong position now.

## User

Now, how do I access the chat from my phone?

## Assistant

You are very close. The only thing missing is **secure external access to Open WebUI**.

Do **not** expose ports directly. You already decided correctly: use **Cloudflare Tunnel**.

---

# 🎯 Goal
Access this from your phone:

```
https://your-domain → Open WebUI (Steam Deck:3000)
```

---

# ✅ Single Step (for tomorrow)

Install Cloudflare Tunnel on the Steam Deck.

### Run:

```bash
sudo pacman -S cloudflared
```

If that fails (common on SteamOS), use the binary:

```bash
mkdir -p ~/bin
cd ~/bin

curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o cloudflared

chmod +x cloudflared
```

---

# 📌 What This Will Enable

Cloudflare Tunnel will:

- expose **ONLY Open WebUI**
- keep everything else private (Ollama, RAG, filesystem)
- give you a **secure HTTPS URL**
- allow phone access instantly

---

# 🔜 What Happens After Install (next step, not now)

Tomorrow I will walk you through:

1. `cloudflared tunnel login`
2. creating a tunnel
3. routing it to:
   ```
   http://localhost:3000
   ```
4. attaching a domain (or temporary URL)
5. locking it behind Cloudflare Access (optional but recommended)

---

# ⚠️ Important

Do NOT:
- open router ports
- expose 3000 directly
- use ngrok

Cloudflare Tunnel is the correct architecture for your system.

---

# 🧠 Mental Model

```text
Phone → Cloudflare → Tunnel → Steam Deck → Open WebUI
```

Everything else stays private.

---

# ✔️ Where You Are

You now have:
- working local AI system
- governed artifact pipeline
- Open WebUI control surface

Next:
👉 make it reachable from anywhere

---

When you're ready tomorrow, say:

> "continue tunnel setup"

and we’ll finish it cleanly in a few steps.

## User

answer these questions only please

Q1 — Phase 1 Status Interpretation

Is Phase 1 collaboration environment considered:

A. Already functionally established
B. Still only partially established

Q2 — Governance Status

Are the conversation modes and artifact-governance rules:

A. Conceptual only in this chat
B. Already partially implemented in this chat

Q3 — Controlled Write Boundary

At this point in the audited chat, is the write boundary:

A. ~/cics/artifacts/ only
B. ~/cics/staging/ already active
C. Not yet formally established

Q4 — XPS Role Status

Is XPS in this chat:

A. Architecturally assigned only
B. Actively integrated already

Q5 — Multi-Model Orchestration Status

At this stage, is orchestration:

A. Manual only
B. Partially tool-enforced already

Q6 — External Access Status

Is Cloudflare exposure:

A. Policy only, not yet implemented
B. Implemented already

Q7 — parse_and_write.py Status

In this audited file, should parse_and_write.py be treated as:

A. Proposed but unvalidated
B. Implemented and validated

Q8 — Artifact Lifecycle Status

Is the lifecycle:

generate → stage → review → approve → commit → ingest

A. Target model only
B. Already partially working in this chat

Q9 — Phase Boundary

Does this chat belong to:

A. Collaboration environment build
B. RAG/data-node integration
C. Mixed phase

Q10 — Local vs Cloud Role

At this stage, should local models be treated as:

A. Supporting execution engines under operator control
B. Co-equal reasoning authorities with GPT

## Assistant

Q1 — **A**

Q2 — **B**

Q3 — **B**

Q4 — **A**

Q5 — **A**

Q6 — **A**

Q7 — **B**

Q8 — **B**

Q9 — **A**

Q10 — **A**

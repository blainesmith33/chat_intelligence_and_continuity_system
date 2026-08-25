#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Iterable, List, Sequence, Tuple

# ============================================================
# CICS CHAT CORPUS CHUNKER
# ============================================================
# Reads recursively from:
#   /home/deck/mnt/xps_cics/imports/raw
#
# Writes chunk files to:
#   /home/deck/mnt/xps_cics/corpora/chats/chunks/<section>/<language>/
#
# Design goals:
# - deterministic output
# - safe re-runs
# - recursive source traversal
# - section-based output
# - language-aware block routing
# - overlap between chunks for retrieval continuity
# - stable, traceable filenames
# ============================================================

SOURCE_ROOT = Path("/home/kimberly/cics/imports/raw")
OUTPUT_ROOT = Path("/home/kimberly/cics/corpora/chats/chunks")

FILE_GLOB = "*.txt"

ENGLISH_CHUNK_SIZE = 4000
ENGLISH_CHUNK_OVERLAP = 500

CODE_CHUNK_SIZE = 2500
CODE_CHUNK_OVERLAP = 250

NORMALIZE_LINE_ENDINGS = True
STRIP_TRAILING_WHITESPACE = True
COLLAPSE_EXCESSIVE_BLANK_LINES = True

SHORT_HASH_LEN = 10

SECTION_MAP = {
    "CICS": "cics",
    "Aletheia_Forensis": "aletheia_forensis",
    "Imperium_Aletheiae": "imperium_aletheiae",
    "Deterministic_AI_Infrastructure": "deterministic_ai_infrastructure",
    "ExosWoW_Mod_Ecosystem": "exoswow_mod_ecosystem",
    "ExosWoW_Addon_Project": "exoswow_addon_project",
    "Ai_Diagonstician": "ai_diagnostician",
    "ALIP-AI_Infrastructure_Provisioning_Platform": "alip_ai_infrastructure_provisioning_platform",
    "ALIP-AI_Lab_Infrastructure_Program": "alip_ai_lab_infrastructure_program",
    "Non-project_chats": "non_project_chats",
    "UMB_Cross-Project_Governance_Framework": "umb_cross_project_governance_framework",
    "gods_and_men": "gods_and_men",
    "blAine": "blaine",
    "ARCHIVE": "archive",
    "blaineai.me_website": "blaineai_website",
}

LANGUAGES = {"english", "python", "bash", "json", "config", "other"}


def normalize_text(text: str) -> str:
    if NORMALIZE_LINE_ENDINGS:
        text = text.replace("\r\n", "\n").replace("\r", "\n")

    if STRIP_TRAILING_WHITESPACE:
        text = "\n".join(line.rstrip() for line in text.split("\n"))

    if COLLAPSE_EXCESSIVE_BLANK_LINES:
        text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip() + "\n"


def iter_source_files(source_root: Path) -> Iterable[Path]:
    return sorted(p for p in source_root.rglob(FILE_GLOB) if p.is_file())


def make_source_id(source_root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(source_root).as_posix()
    digest = hashlib.sha256(rel.encode("utf-8")).hexdigest()
    return digest[:SHORT_HASH_LEN]


def sanitize_stem(file_path: Path) -> str:
    stem = file_path.stem
    stem = re.sub(r"\s+", "_", stem)
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", stem)
    stem = re.sub(r"_+", "_", stem)
    return stem.strip("_") or "untitled"


def get_section_name(source_root: Path, file_path: Path) -> str:
    rel_parts = file_path.relative_to(source_root).parts
    if not rel_parts:
        raise RuntimeError(f"Unable to derive section from path: {file_path}")

    top = rel_parts[0]
    if top not in SECTION_MAP:
        raise RuntimeError(f"Unmapped source section: {top}")

    return SECTION_MAP[top]


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    if not text.strip():
        return []

    chunks: List[str] = []
    step = chunk_size - overlap
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk + "\n")
        start += step

    return chunks


def detect_fence_language(fence_label: str) -> str:
    label = fence_label.strip().lower()

    if label in {"python", "py"}:
        return "python"
    if label in {"bash", "sh", "shell", "zsh"}:
        return "bash"
    if label == "json":
        return "json"
    if label in {"yaml", "yml", "toml", "ini", "conf", "config"}:
        return "config"
    if label:
        return "other"
    return "other"


def looks_like_json_block(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if (stripped.startswith("{") and stripped.endswith("}")) or (
        stripped.startswith("[") and stripped.endswith("]")
    ):
        return True
    return False


def looks_like_python_block(text: str) -> bool:
    return bool(
        re.search(
            r"(^|\n)\s*(def |class |import |from .* import |if __name__ == ['\"]__main__['\"]:)",
            text,
        )
    )


def looks_like_bash_block(text: str) -> bool:
    return bool(
        re.search(
            r"(^|\n)\s*(\$ |cd |ls\b|find\b|mkdir\b|rm\b|mv\b|cp\b|chmod\b|python\b|pytest\b|ssh\b|sed\b)",
            text,
        )
    )


def looks_like_config_block(text: str) -> bool:
    return bool(
        re.search(
            r"(^|\n)\s*([A-Za-z0-9_.-]+)\s*=\s*\S+",
            text,
        )
    ) or bool(
        re.search(
            r"(^|\n)\s*[A-Za-z0-9_.-]+\s*:\s*\S+",
            text,
        )
    )


def classify_plain_block(text: str) -> str:
    if looks_like_json_block(text):
        return "json"
    if looks_like_python_block(text):
        return "python"
    if looks_like_bash_block(text):
        return "bash"
    if looks_like_config_block(text):
        return "config"
    return "english"


def split_into_blocks(text: str) -> List[Tuple[str, str]]:
    """
    Returns a list of (language, block_text).
    Fenced code blocks are routed by fence label.
    Everything outside fences is classified heuristically.
    """
    blocks: List[Tuple[str, str]] = []

    pattern = re.compile(r"```([A-Za-z0-9_-]*)\n(.*?)```", re.DOTALL)
    pos = 0

    for match in pattern.finditer(text):
        before = text[pos:match.start()]
        if before.strip():
            lang = classify_plain_block(before)
            blocks.append((lang, before.strip() + "\n"))

        fence_lang = detect_fence_language(match.group(1))
        fence_body = match.group(2).strip()
        if fence_body:
            blocks.append((fence_lang, fence_body + "\n"))

        pos = match.end()

    tail = text[pos:]
    if tail.strip():
        lang = classify_plain_block(tail)
        blocks.append((lang, tail.strip() + "\n"))

    return merge_adjacent_same_language_blocks(blocks)


def merge_adjacent_same_language_blocks(
    blocks: Sequence[Tuple[str, str]],
) -> List[Tuple[str, str]]:
    merged: List[Tuple[str, str]] = []

    for lang, text in blocks:
        if lang not in LANGUAGES:
            lang = "other"

        if merged and merged[-1][0] == lang:
            prev_lang, prev_text = merged[-1]
            merged[-1] = (prev_lang, prev_text.rstrip() + "\n\n" + text.lstrip())
        else:
            merged.append((lang, text))

    return merged


def build_chunk_filename(
    source_root: Path,
    file_path: Path,
    language: str,
    chunk_index: int,
) -> str:
    stem = sanitize_stem(file_path)
    source_id = make_source_id(source_root, file_path)
    return f"{stem}__{source_id}__{language}_chunk_{chunk_index:06d}.txt"


def clear_existing_chunks(output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    for old_file in output_root.rglob("*.txt"):
        old_file.unlink()


def chunk_for_language(language: str, text: str) -> List[str]:
    if language == "english":
        return chunk_text(text, ENGLISH_CHUNK_SIZE, ENGLISH_CHUNK_OVERLAP)
    return chunk_text(text, CODE_CHUNK_SIZE, CODE_CHUNK_OVERLAP)


def process_file(source_root: Path, output_root: Path, file_path: Path) -> int:
    raw_text = file_path.read_text(encoding="utf-8")
    text = normalize_text(raw_text)

    if not text.strip():
        return 0

    section = get_section_name(source_root, file_path)
    blocks = split_into_blocks(text)

    per_language_index: DefaultDict[str, int] = defaultdict(int)
    written = 0

    for language, block_text in blocks:
        chunks = chunk_for_language(language, block_text)

        for chunk in chunks:
            chunk_index = per_language_index[language]
            per_language_index[language] += 1

            out_dir = output_root / section / language
            out_dir.mkdir(parents=True, exist_ok=True)

            out_name = build_chunk_filename(
                source_root=source_root,
                file_path=file_path,
                language=language,
                chunk_index=chunk_index,
            )
            out_path = out_dir / out_name
            out_path.write_text(chunk, encoding="utf-8")
            written += 1

    return written


def main() -> None:
    if not SOURCE_ROOT.exists():
        raise SystemExit(f"Source root does not exist: {SOURCE_ROOT}")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    source_files = list(iter_source_files(SOURCE_ROOT))
    if not source_files:
        raise SystemExit(f"No source files found under: {SOURCE_ROOT}")

    print("=== CICS Chat Corpus Chunker ===")
    print(f"Source root          : {SOURCE_ROOT}")
    print(f"Output root          : {OUTPUT_ROOT}")
    print(f"Source files         : {len(source_files)}")
    print(f"English chunk size   : {ENGLISH_CHUNK_SIZE}")
    print(f"English overlap      : {ENGLISH_CHUNK_OVERLAP}")
    print(f"Code chunk size      : {CODE_CHUNK_SIZE}")
    print(f"Code overlap         : {CODE_CHUNK_OVERLAP}")
    print()

    print("Clearing existing chunk files recursively...")
    clear_existing_chunks(OUTPUT_ROOT)

    total_chunks = 0

    for index, file_path in enumerate(source_files, start=1):
        rel = file_path.relative_to(SOURCE_ROOT)
        count = process_file(SOURCE_ROOT, OUTPUT_ROOT, file_path)
        total_chunks += count
        print(f"[{index}/{len(source_files)}] {rel} -> {count} chunks")

    print()
    print("=== COMPLETE ===")
    print(f"Source files processed : {len(source_files)}")
    print(f"Total chunks written   : {total_chunks}")


if __name__ == "__main__":
    main()
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/home/kimberly/cics"
VENV_PY="$PROJECT_ROOT/.venv/bin/python"
EMBED_SCRIPT="$PROJECT_ROOT/scripts/create_embeddings.py"

HIGH_NICE="-3"
LOW_NICE="15"

# Edit this if you launch Arena a different way.
ARENA_CMD='steam -applaunch 2141910'

# You may need to tune this once, depending on how Proton exposes the process.
ARENA_MATCH='MTGA\.exe|MTGA'

find_embedding_pid() {
    pgrep -o -f "^${VENV_PY//\//\\/} ${EMBED_SCRIPT//\//\\/}$" || true
}

echo "[arena] lowering embedding priority if running"
pid="$(find_embedding_pid)"
if [[ -n "$pid" ]]; then
    sudo renice -n "$LOW_NICE" -p "$pid" >/dev/null
    echo "[arena] embedding job set to low priority (nice $LOW_NICE), pid=$pid"
else
    echo "[arena] embedding job not running; continuing anyway"
fi

echo "[arena] launching MTG Arena"
bash -lc "$ARENA_CMD" >/dev/null 2>&1 &

echo "[arena] waiting for Arena process to appear"
for _ in $(seq 1 60); do
    if pgrep -f "$ARENA_MATCH" >/dev/null; then
        echo "[arena] Arena detected"
        break
    fi
    sleep 2
done

echo "[arena] monitoring until Arena exits"
while pgrep -f "$ARENA_MATCH" >/dev/null; do
    sleep 5
done

echo "[arena] Arena closed; restoring embedding priority"
pid="$(find_embedding_pid)"
if [[ -n "$pid" ]]; then
    sudo renice -n "$HIGH_NICE" -p "$pid" >/dev/null
    echo "[arena] embedding job restored to high priority (nice $HIGH_NICE), pid=$pid"
else
    echo "[arena] embedding job is not running; nothing to restore"
fi
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/home/kimberly/cics"
VENV_PY="$PROJECT_ROOT/.venv/bin/python"
EMBED_SCRIPT="$PROJECT_ROOT/scripts/create_embeddings.py"
CHECKPOINT_FILE="$PROJECT_ROOT/runtime/embedding_checkpoint.json"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/create_embeddings.log"

# Safer than -5 on this machine.
HIGH_NICE="-3"

TOTAL_CHUNKS=294376

find_embedding_pid() {
    pgrep -o -f "^${VENV_PY//\//\\/} ${EMBED_SCRIPT//\//\\/}$" || true
}

mkdir -p "$LOG_DIR"

pid="$(find_embedding_pid)"

if [[ -z "$pid" ]]; then
    echo "[guard] embedding job not running; starting it now"
    cd "$PROJECT_ROOT"
    nohup "$VENV_PY" "$EMBED_SCRIPT" >> "$LOG_FILE" 2>&1 &
    sleep 3
    pid="$(find_embedding_pid)"
    if [[ -z "$pid" ]]; then
        echo "[guard] ERROR: embedding job did not start"
        exit 1
    fi
    echo "[guard] started embedding job pid=$pid"
else
    echo "[guard] embedding job already running pid=$pid"
fi

sudo renice -n "$HIGH_NICE" -p "$pid" >/dev/null
echo "[guard] embedding job set to high priority (nice $HIGH_NICE), pid=$pid"
echo

prev_index=""
prev_time=""

while true; do
    clear

    pid="$(find_embedding_pid)"
    if [[ -z "$pid" ]]; then
        echo "[guard] embedding job is not running"
        exit 1
    fi

    if [[ ! -f "$CHECKPOINT_FILE" ]]; then
        echo "[guard] waiting for checkpoint file: $CHECKPOINT_FILE"
        sleep 5
        continue
    fi

    current_index="$(jq -r '.next_index // 0' "$CHECKPOINT_FILE")"
    now="$(date +%s)"
    current_nice="$(ps -o ni= -p "$pid" | tr -d ' ')"

    processed="$current_index"
    remaining=$((TOTAL_CHUNKS - processed))
    (( remaining < 0 )) && remaining=0

    rate="warming_up"
    eta_hours="warming_up"

    if [[ -n "$prev_index" && -n "$prev_time" ]]; then
        delta_index=$((current_index - prev_index))
        delta_time=$((now - prev_time))

        if (( delta_time > 0 && delta_index >= 0 )); then
            rate_value="$(awk "BEGIN { printf \"%.4f\", $delta_index / $delta_time }")"

            if awk "BEGIN { exit !($rate_value > 0) }"; then
                eta_value="$(awk "BEGIN { printf \"%.1f\", $remaining / $rate_value / 3600 }")"
                rate="$rate_value"
                eta_hours="$eta_value"
            fi
        fi
    fi

    percent="$(awk "BEGIN { printf \"%.2f\", ($processed / $TOTAL_CHUNKS) * 100 }")"

    echo "Embedding Guard"
    echo "==============="
    echo "pid:              $pid"
    echo "nice:             $current_nice"
    echo "processed:        $processed / $TOTAL_CHUNKS"
    echo "remaining:        $remaining"
    echo "percent:          $percent%"
    echo "rate:             $rate chunks/sec"
    echo "eta_hours:        $eta_hours"
    echo "checkpoint_file:  $CHECKPOINT_FILE"
    echo "log_file:         $LOG_FILE"
    echo
    echo "Refreshing every 30 seconds. Press Ctrl+C to close this monitor."
    echo "The embedding job will keep running."

    prev_index="$current_index"
    prev_time="$now"

    sleep 30
done
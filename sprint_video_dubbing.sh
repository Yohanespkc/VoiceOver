#!/usr/bin/env bash
# ==============================================================================
# VoiceOver Studio SO — Video Dubbing Sprint Quick Runner
# ==============================================================================
# Usage:
#   ./sprint_video_dubbing.sh --url "https://www.youtube.com/watch?v=..." --duration 36 --voice so_marcia
#   ./sprint_video_dubbing.sh --video "path/to/video.mp4" --duration 60 --voice so_marcia
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"

if [ ! -f "$PYTHON_EXEC" ]; then
    echo "⚠️ Python venv tidak ditemukan di $PYTHON_EXEC. Menggunakan python3 sistem..."
    PYTHON_EXEC="python3"
fi

"$PYTHON_EXEC" "$SCRIPT_DIR/video_dubbing_sprint.py" "$@"

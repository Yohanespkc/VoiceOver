#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "======================================================="
echo "🎙️  Menjalankan VoiceOver Studio (Karakter & Asset Asli)"
echo "======================================================="

export PYTORCH_ENABLE_MPS_FALLBACK=1

# Check virtual environments (prioritize local VoiceOver .venv)
PYTHON_BIN=""
if [ -f "./.venv/bin/python" ]; then
  PYTHON_BIN="./.venv/bin/python"
elif [ -f "/Users/yohanessurya/Documents/Development/xtts-v2/.venv/bin/python" ]; then
  PYTHON_BIN="/Users/yohanessurya/Documents/Development/xtts-v2/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

echo "Menggunakan Python: $PYTHON_BIN"
echo "Membuka server di: http://127.0.0.1:8765"
echo "Tekan Ctrl+C untuk menghentikan server."

$PYTHON_BIN -m uvicorn server:app --host 127.0.0.1 --port 8765 --reload

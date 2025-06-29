#!/usr/bin/env bash
set -euo pipefail

# Run AI-OPS unit tests using a local Ollama instance.
# This script mirrors the CI setup in .github/workflows/unit-test.yml.

# Install python dependencies
pip install -q -r requirements-api.txt -r requirements-dev.txt
python -m spacy download en_core_web_md -q

# Environment
export ENDPOINT="${ENDPOINT:-http://127.0.0.1:11434}"
export OLLAMA_ENDPOINT="$ENDPOINT"
export PYTHONPATH="$PYTHONPATH:$(pwd)"
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1

echo "Using ENDPOINT=$ENDPOINT"

docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant &
qdrant_pid=$!

ollama serve &
ollama_pid=$!

trap 'kill $qdrant_pid $ollama_pid' EXIT

# wait for Ollama
for i in {1..10}; do
    if curl -s -f -o /dev/null "$ENDPOINT/v1/models"; then
        echo "[+] Ollama is running"
        break
    fi
    echo "[-] Waiting for Ollama to start ..."
    sleep 5
done

ollama pull nomic-embed-text
ollama pull mistral

pytest -q

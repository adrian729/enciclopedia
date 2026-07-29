#!/usr/bin/env bash
set -euo pipefail

if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Install Node.js first (e.g. brew install node)." >&2
  exit 1
fi

if ! command -v docsify >/dev/null 2>&1; then
  echo "Installing docsify-cli via npm..."
  npm install -g docsify-cli
fi

echo "Done. Run: docsify serve docs"

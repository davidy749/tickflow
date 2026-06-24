#!/usr/bin/env bash
# Tag and push a release. Usage: scripts/release.sh 0.3.0
set -euo pipefail

version="${1:?usage: release.sh <version>}"

if ! grep -q "__version__ = \"${version}\"" src/tickflow/__init__.py; then
    echo "error: __version__ in src/tickflow/__init__.py is not ${version}" >&2
    echo "bump it (and pyproject.toml) before tagging." >&2
    exit 1
fi

git tag -a "v${version}" -m "tickflow ${version}"
git push origin "v${version}"
echo "pushed tag v${version} — the release workflow will build and publish."

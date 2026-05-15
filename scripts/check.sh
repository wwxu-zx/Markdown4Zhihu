#!/bin/sh

set -eu

TMP_PYCACHE_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_PYCACHE_DIR"' EXIT HUP INT TERM

sh -n scripts/publish.sh
PYTHONPYCACHEPREFIX="$TMP_PYCACHE_DIR" python -m py_compile zhihu-publisher.py tests/test_zhihu_publisher.py
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_zhihu_publisher
git diff --check

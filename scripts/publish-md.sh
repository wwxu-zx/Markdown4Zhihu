#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
CURRENT_DIR=$(pwd)

require_command() {
    command_name=$1
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "Required command not found: $command_name" >&2
        echo "Please install $command_name and try again." >&2
        exit 1
    fi
}

show_usage() {
    cat <<EOF
Usage:
  sh scripts/publish-md.sh <markdown-file> [zhihu-publisher args...]

Examples:
  sh scripts/publish-md.sh article.md
  sh scripts/publish-md.sh Resource/Article/Article.md --compress
  sh scripts/publish-md.sh "/tmp/notes/An Article.md" --git-mode=push

What it does:
  1. Resolve the markdown file path
  2. Call zhihu-publisher.py with --input="<markdown-file>"
EOF
}

absolute_file_path() {
    target_path=$1
    target_dir=$(CDPATH= cd -- "$(dirname -- "$target_path")" && pwd)
    target_name=$(basename -- "$target_path")
    printf '%s/%s\n' "$target_dir" "$target_name"
}

resolve_markdown_path() {
    input_value=$1

    if [ -f "$input_value" ]; then
        absolute_file_path "$input_value"
        return 0
    fi

    if [ -f "$CURRENT_DIR/$input_value" ]; then
        absolute_file_path "$CURRENT_DIR/$input_value"
        return 0
    fi

    if [ -f "$REPO_ROOT/$input_value" ]; then
        absolute_file_path "$REPO_ROOT/$input_value"
        return 0
    fi

    return 1
}

if [ "$#" -lt 1 ]; then
    show_usage >&2
    exit 1
fi

case "$1" in
    -h|--help)
        show_usage
        exit 0
        ;;
esac

MARKDOWN_INPUT=$1
shift

MARKDOWN_PATH=$(resolve_markdown_path "$MARKDOWN_INPUT") || {
    echo "Markdown file not found for input: $MARKDOWN_INPUT" >&2
    echo >&2
    show_usage >&2
    exit 1
}

require_command python

echo "Markdown input : $MARKDOWN_PATH"
echo "Running        : python zhihu-publisher.py --input=\"$MARKDOWN_PATH\" $*"

cd "$REPO_ROOT"
python zhihu-publisher.py --input="$MARKDOWN_PATH" "$@"

#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
CURRENT_DIR=$(pwd)
RESOURCE_DIR="$REPO_ROOT/Resource"

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
  sh scripts/publish.sh <article-name-or-zip> [zhihu-publisher args...]

Examples:
  sh scripts/publish.sh AlexNet
  sh scripts/publish.sh Resource/AlexNet.zip
  sh scripts/publish.sh "Reading Research Papers and Career Advice from Andrew Ng" --compress
  sh scripts/publish.sh AlexNet --git-mode=push

What it does:
  1. Find the zip package, defaulting to Resource/<article>.zip
  2. Rebuild the same-name folder from the zip package
  3. Publish the extracted markdown file with zhihu-publisher.py
EOF

    if [ -d "$RESOURCE_DIR" ]; then
        AVAILABLE=$(find "$RESOURCE_DIR" -maxdepth 1 -type f -name "*.zip" -exec basename {} .zip \; | sort)
        if [ -n "$AVAILABLE" ]; then
            echo
            echo "Available packages in Resource/:"
            OLD_IFS=$IFS
            IFS='
'
            for item in $AVAILABLE; do
                echo "  - $item"
            done
            IFS=$OLD_IFS
        fi
    fi
}

resolve_zip_path() {
    input_value=$1

    if [ -f "$input_value" ]; then
        printf '%s\n' "$input_value"
        return 0
    fi

    if [ -f "$CURRENT_DIR/$input_value" ]; then
        printf '%s\n' "$CURRENT_DIR/$input_value"
        return 0
    fi

    if [ -f "$REPO_ROOT/$input_value" ]; then
        printf '%s\n' "$REPO_ROOT/$input_value"
        return 0
    fi

    case "$input_value" in
        *.zip)
            if [ -f "$CURRENT_DIR/Resource/$input_value" ]; then
                printf '%s\n' "$CURRENT_DIR/Resource/$input_value"
                return 0
            fi
            if [ -f "$RESOURCE_DIR/$input_value" ]; then
                printf '%s\n' "$RESOURCE_DIR/$input_value"
                return 0
            fi
            ;;
        *)
            if [ -f "$CURRENT_DIR/Resource/$input_value.zip" ]; then
                printf '%s\n' "$CURRENT_DIR/Resource/$input_value.zip"
                return 0
            fi
            if [ -f "$RESOURCE_DIR/$input_value.zip" ]; then
                printf '%s\n' "$RESOURCE_DIR/$input_value.zip"
                return 0
            fi
            ;;
    esac

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

ZIP_INPUT=$1
shift

ZIP_PATH=$(resolve_zip_path "$ZIP_INPUT") || {
    echo "Zip file not found for input: $ZIP_INPUT" >&2
    echo >&2
    show_usage >&2
    exit 1
}

ZIP_NAME=$(basename "$ZIP_PATH")
ZIP_STEM=${ZIP_NAME%.zip}

if [ "$ZIP_NAME" = "$ZIP_STEM" ]; then
    echo "Expected a .zip file, got: $ZIP_PATH" >&2
    exit 1
fi

if [ -z "$ZIP_STEM" ]; then
    echo "Invalid zip file name: $ZIP_NAME" >&2
    exit 1
fi

ZIP_DIR=$(CDPATH= cd -- "$(dirname "$ZIP_PATH")" && pwd)
ZIP_PATH="$ZIP_DIR/$ZIP_NAME"
EXTRACT_DIR="$ZIP_DIR/$ZIP_STEM"
MD_PATH="$EXTRACT_DIR/$ZIP_STEM.md"

require_command unzip
require_command python

if [ "$EXTRACT_DIR" = "$ZIP_DIR" ] || [ "$EXTRACT_DIR" = "/" ]; then
    echo "Refusing to rebuild unsafe extraction path: $EXTRACT_DIR" >&2
    exit 1
fi

if [ -e "$EXTRACT_DIR" ] && [ ! -d "$EXTRACT_DIR" ]; then
    echo "Extraction path exists and is not a directory: $EXTRACT_DIR" >&2
    exit 1
fi

rm -rf "$EXTRACT_DIR"
mkdir -p "$EXTRACT_DIR"
unzip -oq "$ZIP_PATH" -d "$EXTRACT_DIR"

if [ ! -f "$MD_PATH" ]; then
    echo "Expected markdown file not found: $MD_PATH" >&2
    exit 1
fi

echo "Zip package    : $ZIP_PATH"
echo "Rebuilt folder : $EXTRACT_DIR"
echo "Markdown input : $MD_PATH"
echo "Running        : python zhihu-publisher.py --input=\"$MD_PATH\" $*"

cd "$REPO_ROOT"
python zhihu-publisher.py --input="$MD_PATH" "$@"

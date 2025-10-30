#!/bin/bash
set -euo pipefail

# Script to convert PNG frame sequences to animated WebP using img2webp
# Handles large numbers of frames by using argument file approach

usage() {
    cat << EOF
Usage: $0 <input_pattern> <output_file>

Examples:
  $0 "~/screenshots/frame_*.png" output.webp
  $0 "/path/to/frames/*.png" animation.webp
  $0 "./frame_*.png" result.webp

The script will:
  - Find all matching PNG files
  - Sort them naturally (frame_1, frame_2, ... frame_10, frame_11, ...)
  - Create lossless animated WebP at 10fps with maximum compression
  - Optimize for screenshot content with temporal compression (kmin=10, kmax=100)

Requirements:
  - img2webp must be installed (from webp/libwebp-tools package)
EOF
    exit 1
}

# Check arguments
if [ $# -ne 2 ]; then
    echo "Error: Wrong number of arguments"
    echo
    usage
fi

INPUT_PATTERN="$1"
OUTPUT_FILE="$2"

# Check if img2webp is available
if ! command -v img2webp &> /dev/null; then
    echo "Error: img2webp not found. Please install it:"
    echo "  Ubuntu/Debian: sudo apt install webp"
    echo "  Fedora: sudo dnf install libwebp-tools"
    echo "  Arch: sudo pacman -S libwebp"
    exit 1
fi

# Expand tilde and get directory and pattern
INPUT_PATTERN="${INPUT_PATTERN/#\~/$HOME}"
DIRECTORY="$(dirname "$INPUT_PATTERN")"
PATTERN="$(basename "$INPUT_PATTERN")"

# Check if directory exists
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: Directory does not exist: $DIRECTORY"
    exit 1
fi

# Create temporary argument file
TEMP_ARGS=$(mktemp /tmp/img2webp_args.XXXXXX.txt)
trap "rm -f '$TEMP_ARGS'" EXIT

echo "Finding frames matching: $INPUT_PATTERN"

# Find all matching files and sort them naturally
FRAME_COUNT=$(find "$DIRECTORY" -maxdepth 1 -name "$PATTERN" -type f | wc -l)

if [ "$FRAME_COUNT" -eq 0 ]; then
    echo "Error: No frames found matching pattern: $INPUT_PATTERN"
    exit 1
fi

echo "Found $FRAME_COUNT frames"

# Create argument file with optimal settings
cat > "$TEMP_ARGS" <<EOF
-lossless
-m 6
-d 100
-kmin 10
-kmax 100
-exact
-loop 0
-v
-o
$OUTPUT_FILE
EOF

# Append sorted frame list (using natural sort for proper ordering)
find "$DIRECTORY" -maxdepth 1 -name "$PATTERN" -type f | sort -V >> "$TEMP_ARGS"

echo "Creating animated WebP with settings:"
echo "  - Lossless compression with maximum effort (-m 6)"
echo "  - 10 fps (100ms per frame)"
echo "  - Temporal optimization for screenshots (kmin=10, kmax=100)"
echo "  - Exact color preservation in transparent areas"
echo "  - Infinite loop"
echo ""
echo "This may take a while for large frame counts..."
echo ""

# Run img2webp with argument file
if img2webp "$TEMP_ARGS"; then
    echo ""
    echo "Success! Created: $OUTPUT_FILE"

    # Show file size
    if [ -f "$OUTPUT_FILE" ]; then
        SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        echo "File size: $SIZE"
    fi
else
    echo ""
    echo "Error: img2webp failed"
    exit 1
fi

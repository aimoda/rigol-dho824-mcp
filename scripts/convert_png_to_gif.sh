#!/bin/bash
set -euo pipefail

# Script to convert PNG frame sequences to animated GIF using ffmpeg
# Uses 2-pass approach with custom palette generation for optimal quality

usage() {
    cat << EOF
Usage: $0 <input_pattern> <output_file>

Examples:
  $0 "~/screenshots/frame_*.png" output.gif
  $0 "/path/to/frames/*.png" animation.gif
  $0 "./frame_*.png" result.gif

The script will:
  - Find all matching PNG files
  - Sort them naturally (frame_1, frame_2, ... frame_10, frame_11, ...)
  - Generate optimal color palette (pass 1)
  - Create high-quality animated GIF at 10fps (pass 2)
  - Optimize with gifsicle for smaller file size (if available)

Quality settings:
  - Custom palette generation optimized for frame differences
  - Bayer dithering (scale=5) for clean, low-noise output
  - Differential encoding for efficiency
  - Infinite loop

Requirements:
  - ffmpeg must be installed
  - gifsicle (optional, for optimization)
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

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg not found. Please install it:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Fedora: sudo dnf install ffmpeg"
    echo "  Arch: sudo pacman -S ffmpeg"
    echo "  macOS: brew install ffmpeg"
    exit 1
fi

# Check if gifsicle is available (optional)
GIFSICLE_AVAILABLE=false
if command -v gifsicle &> /dev/null; then
    GIFSICLE_AVAILABLE=true
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

echo "Finding frames matching: $INPUT_PATTERN"

# Find all matching files and sort them naturally
FRAME_COUNT=$(find "$DIRECTORY" -maxdepth 1 -name "$PATTERN" -type f | wc -l)

if [ "$FRAME_COUNT" -eq 0 ]; then
    echo "Error: No frames found matching pattern: $INPUT_PATTERN"
    exit 1
fi

echo "Found $FRAME_COUNT frames"

# Create temporary files
TEMP_FILE_LIST=$(mktemp /tmp/gif_frames.XXXXXX.txt)
TEMP_PALETTE=$(mktemp /tmp/gif_palette.XXXXXX.png)
TEMP_GIF=$(mktemp /tmp/gif_output.XXXXXX.gif)
trap "rm -f '$TEMP_FILE_LIST' '$TEMP_PALETTE' '$TEMP_GIF'" EXIT

# Create sorted file list
find "$DIRECTORY" -maxdepth 1 -name "$PATTERN" -type f | sort -V > "$TEMP_FILE_LIST"

# Create ffmpeg concat file format with duration for each frame
# For 10fps, each frame should display for 0.1 seconds (100ms)
TEMP_CONCAT=$(mktemp /tmp/gif_concat.XXXXXX.txt)
trap "rm -f '$TEMP_FILE_LIST' '$TEMP_PALETTE' '$TEMP_GIF' '$TEMP_CONCAT'" EXIT

# Build concat file with duration for each frame (10fps = 0.1s per frame)
FRAME_DURATION="0.1"
LAST_FRAME=""

while IFS= read -r frame; do
    if [ -n "$LAST_FRAME" ]; then
        # Write previous frame with duration
        echo "file '$LAST_FRAME'" >> "$TEMP_CONCAT"
        echo "duration $FRAME_DURATION" >> "$TEMP_CONCAT"
    fi
    LAST_FRAME="$frame"
done < "$TEMP_FILE_LIST"

# Write last frame twice (required by concat demuxer for proper timing)
if [ -n "$LAST_FRAME" ]; then
    echo "file '$LAST_FRAME'" >> "$TEMP_CONCAT"
    echo "file '$LAST_FRAME'" >> "$TEMP_CONCAT"
fi

echo ""
echo "Pass 1/2: Generating optimal color palette..."
echo "  - Analyzing frame differences for optimal colors"
echo "  - Maximum 256 colors (GIF limit)"
echo ""

# Pass 1: Generate palette optimized for screenshot content
if ! ffmpeg -f concat -safe 0 -i "$TEMP_CONCAT" \
    -vf "palettegen=stats_mode=diff:max_colors=256" \
    -y "$TEMP_PALETTE" -loglevel warning -stats; then
    echo ""
    echo "Error: Palette generation failed"
    exit 1
fi

echo ""
echo "Pass 2/2: Creating animated GIF..."
echo "  - 10 fps frame rate"
echo "  - Bayer dithering (scale=5) for clean output"
echo "  - Differential encoding for smaller size"
echo "  - Infinite loop"
echo ""

# Pass 2: Create GIF using custom palette
if ! ffmpeg -f concat -safe 0 -i "$TEMP_CONCAT" \
    -i "$TEMP_PALETTE" \
    -lavfi "paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
    -loop 0 \
    -y "$TEMP_GIF" -loglevel warning -stats; then
    echo ""
    echo "Error: GIF creation failed"
    exit 1
fi

# Optimize with gifsicle if available
if [ "$GIFSICLE_AVAILABLE" = true ]; then
    echo ""
    echo "Optimizing with gifsicle..."
    echo "  - Level 3 optimization (lossless)"
    echo ""

    if gifsicle -O3 -o "$OUTPUT_FILE" "$TEMP_GIF" 2>&1; then
        echo ""
        echo "Success! Created optimized GIF: $OUTPUT_FILE"
    else
        echo ""
        echo "Warning: gifsicle optimization failed, using unoptimized version"
        cp "$TEMP_GIF" "$OUTPUT_FILE"
        echo "Success! Created GIF: $OUTPUT_FILE"
    fi
else
    cp "$TEMP_GIF" "$OUTPUT_FILE"
    echo ""
    echo "Success! Created GIF: $OUTPUT_FILE"
    echo ""
    echo "Tip: Install gifsicle for automatic optimization:"
    echo "  Ubuntu/Debian: sudo apt install gifsicle"
    echo "  Fedora: sudo dnf install gifsicle"
    echo "  Arch: sudo pacman -S gifsicle"
    echo "  macOS: brew install gifsicle"
fi

# Show file size
if [ -f "$OUTPUT_FILE" ]; then
    echo ""
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "File size: $SIZE"
fi

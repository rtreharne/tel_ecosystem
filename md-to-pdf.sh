#!/bin/bash

# Script to convert README.md to PDF.
# Preferred tools: pandoc or Python with weasyprint.

set -e

# Configuration
INPUT_FILE="README.md"
OUTPUT_FILE="README.pdf"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found"
    exit 1
fi

# Try pandoc first
if command -v pandoc >/dev/null 2>&1; then
    echo "Using pandoc to convert $INPUT_FILE to $OUTPUT_FILE..."
    pandoc "$INPUT_FILE" -o "$OUTPUT_FILE" \
      --from markdown \
      --to pdf \
      --standalone \
      --pdf-engine=xelatex
    echo "✓ PDF generated: $OUTPUT_FILE"
    exit 0
fi

# Fallback to Python script
if command -v python3 >/dev/null 2>&1; then
    echo "Using Python fallback converter..."
    python3 "$(dirname "$0")/md-to-pdf.py" "$INPUT_FILE" "$OUTPUT_FILE"
    exit $?
fi

echo "Error: No supported PDF conversion tool found."
echo "Install pandoc or ensure python3 is available."
exit 1

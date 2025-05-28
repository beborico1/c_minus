#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <assembly_file>"
    exit 1
fi

ASSEMBLY_FILE="$1"
MAX_LINES=1000
TIMEOUT=10

if [ ! -f "$ASSEMBLY_FILE" ]; then
    echo "Error: File '$ASSEMBLY_FILE' not found"
    exit 1
fi

echo "Running SPIM with safety limits:"
echo "  - Max output lines: $MAX_LINES"
echo "  - Timeout: ${TIMEOUT}s (using gtimeout if available)"
echo "  - File: $ASSEMBLY_FILE"
echo "----------------------------------------"

# Check if gtimeout is available (from coreutils on macOS)
if command -v gtimeout &> /dev/null; then
    gtimeout $TIMEOUT spim -file "$ASSEMBLY_FILE" 2>&1 | head -n $MAX_LINES
    EXIT_STATUS=${PIPESTATUS[0]}
    if [ $EXIT_STATUS -eq 124 ]; then
        echo ""
        echo "----------------------------------------"
        echo "ERROR: Program killed due to timeout (${TIMEOUT}s exceeded)"
        echo "Possible infinite loop detected!"
    elif [ $EXIT_STATUS -ne 0 ]; then
        echo ""
        echo "----------------------------------------"
        echo "ERROR: SPIM exited with status $EXIT_STATUS"
    fi
else
    # Fallback: just use head to limit output
    echo "WARNING: gtimeout not found. Install with: brew install coreutils"
    echo "Running without timeout protection (output limit only)..."
    echo ""
    spim -file "$ASSEMBLY_FILE" 2>&1 | head -n $MAX_LINES
    echo ""
    echo "----------------------------------------"
    echo "NOTE: Output limited to $MAX_LINES lines"
    echo "If program appears stuck, use Ctrl+C to stop"
fi
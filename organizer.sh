#!/bin/bash
# organizer.sh - Archives grades.csv with a timestamp and logs the action.

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"
LOG_FILE="organizer.log"

# 1. Archive Directory: create it if it doesn't exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "Archive directory not found. Creating '$ARCHIVE_DIR'..."
    mkdir -p "$ARCHIVE_DIR"
else
    echo "Archive directory '$ARCHIVE_DIR' already exists."
fi

# 2. Timestamp Generation (format: YYYYMMDD-HHMMSS)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Guard: nothing to archive
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' does not exist in the current directory."
    exit 1
fi

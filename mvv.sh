#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_venv_path> <destination_venv_path>"
    exit 1
fi

SRC="$1"
DEST="$2"

# If destination ends with /, extract venv name from source and append it
if [[ "$DEST" == */ ]]; then
    VENV_NAME=$(basename "$SRC")
    DEST="$DEST$VENV_NAME"
fi

# Validate source virtual environment exists
if [ ! -d "$SRC" ]; then
    echo "Error: Source virtual environment '$SRC' does not exist"
    exit 1
fi

# Create destination directory if it doesn't exist
mkdir -p "$(dirname "$DEST")" || exit 1

# Activate source virtual environment and freeze packages
source "$SRC/bin/activate" || exit 1
uv pip freeze > .internal-files || exit 1
deactivate

# Create new virtual environment at destination
uv venv "$DEST" || exit 1

# Activate destination virtual environment and install packages
source "$DEST/bin/activate" || exit 1
uv pip install -r .internal-files || exit 1
deactivate

# Clean up the requirements file
rm .internal-files || exit 1

echo "Virtual environment moved successfully from '$SRC' to '$DEST'!"
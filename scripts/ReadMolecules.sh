#!/bin/bash

# Get the current working directory and Blender path from arguments
WORK_DIR="$(dirname "$(realpath "$0")")"
BLENDER_PATH="$1"

# Check if Blender path is provided
if [ -z "$BLENDER_PATH" ]; then
  echo "Error: Blender path not provided."
  echo "Usage: ./ReadMolecules.sh <BlenderPath>"
  exit 1
fi

# Print debug information
echo "Information received."
echo "Moving to Blender path: $BLENDER_PATH"

# Navigate to the Blender directory
cd "$BLENDER_PATH" || { echo "Error: Failed to navigate to Blender path."; exit 1; }

# Execute the Blender command
echo "Executing Receive_Parameters script from path."
"$BLENDER_PATH/blender" "$WORK_DIR/ReadMolecules00.blend" --background --python "$WORK_DIR/Main_Body.py"
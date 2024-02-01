#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Path to the config file
CONFIG_FILE="$SCRIPT_DIR/config/config.ini"

# Read parameters from the config.ini file
OUTPUT_FOLDER=$(awk -F " = " '/OutputFinalFolder/ {print $2}' "$CONFIG_FILE")
OUTPUT_TEX_FILE=$(awk -F " = " '/OutputTeXFile/ {print $2}' "$CONFIG_FILE")
OUTPUT_SPEECH_FILE=$(awk -F " = " '/OutputSpeechFile/ {print $2}' "$CONFIG_FILE")

# Ensure OUTPUT_FOLDER is evaluated for variables such as $HOME
eval OUTPUT_FOLDER=$OUTPUT_FOLDER

# cd into the script directory, if haven't done that already
cd "$SCRIPT_DIR"

# Run the script
source ./env/bin/activate
python ./src/main.py

# Move the files to the output folder
mv "./workdir/$OUTPUT_TEX_FILE" "$OUTPUT_FOLDER"
mv "./workdir/$OUTPUT_SPEECH_FILE" "$OUTPUT_FOLDER"

# Compile the document
cd "$OUTPUT_FOLDER" || { echo "Output folder doesn't exist! Exiting..."; exit 1; }
pdflatex -interaction=nonstopmode "$OUTPUT_TEX_FILE"

# Cleanup the folder - only leave .tex, .pdf, and .mp3 files
for file in *; do
    if [[ ! $file =~ \.tex$ ]] && [[ ! $file =~ \.pdf$ ]] && [[ ! $file =~ \.mp3$ ]]; then
        rm "$file"
    fi
done


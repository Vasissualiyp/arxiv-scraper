#!/bin/bash

OUTPUT_FOLDER="$HOME/research/notes/arxiv_scraper/"

# Get the directory where the script is located 
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# cd into that directory, if haven't done that already
cd "$SCRIPT_DIR"

# Run the script
source ./env/bin/activate
python ./src/main.py

mv ./workdir/related_papers.tex "$OUTPUT_FOLDER"

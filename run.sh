#!/bin/bash

#OUTPUT_FOLDER="$HOME/research/notes/papers/arxiv_scraper/"
OUTPUT_FOLDER="./output/"

# Get the directory where the script is located 
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# cd into that directory, if haven't done that already
cd "$SCRIPT_DIR"

# Run the script
source ./env/bin/activate
python ./src/main.py

mv ./workdir/related_papers.tex "$OUTPUT_FOLDER"

# Compile the document
cd "$OUTPUT_FOLDER" || exit 1
pdflatex "related_papers.tex"
# Cleanup the folder - only leave .tex and .pdf files
for file in *; do
    if [[ ! $file =~ \.tex$ ]] && [[ ! $file =~ \.pdf$ ]]; then
        rm "$file"
    fi
done



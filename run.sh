#!/bin/bash

# Prevent script from running on the weekend
[ "$(date +%u)" -gt 5 ] && exit

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
OUTPUT_LOGFILE="./output.log"

# Path to the config file
CONFIG_FILE="$SCRIPT_DIR/config/config.ini"

# Read parameters from the config.ini file
OUTPUT_FOLDER=$(awk -F " = " '/OutputFinalFolder/ {print $2}' "$CONFIG_FILE")
OUTPUT_TEX_FILE=$(awk -F " = " '/OutputTeXFile/ {print $2}' "$CONFIG_FILE")
OUTPUT_SPEECH_FILE=$(awk -F " = " '/OutputSpeechFile/ {print $2}' "$CONFIG_FILE")
SEPARATE_PAPERS_FOLDER=$(awk -F " = " '/SeparatePapersFolder/ {print $2}' "$CONFIG_FILE")
SEPARATE_PAPERS_FOLDER="workdir/$SEPARATE_PAPERS_FOLDER"
OUTPUT_VIDEO_FILE=$(awk -F " = " '/OutputVideoFile/ {print $2}' "$CONFIG_FILE")

echo "OUTPUT_FOLDER: $OUTPUT_FOLDER"
echo "OUTPUT_TEX_FILE: $OUTPUT_TEX_FILE"
echo "OUTPUT_SPEECH_FILE: $OUTPUT_SPEECH_FILE"
echo "SEPARATE_PAPERS_FOLDER: $SEPARATE_PAPERS_FOLDER"
echo "OUTPUT_VIDEO_FILE: $OUTPUT_VIDEO_FILE"

# Ensure OUTPUT_FOLDER is evaluated for variables such as $HOME
eval OUTPUT_FOLDER=$OUTPUT_FOLDER

# cd into the script directory, if haven't done that already
cd "$SCRIPT_DIR"
echo "Now in $SCRIPT_DIR" &> $OUTPUT_LOGFILE

# Clean up the previous tex, mp3 and mp4 files
rm -f "./$SEPARATE_PAPERS_FOLDER/*" 
echo " Removed all the files from ./$SEPARATE_PAPERS_FOLDER" &>> $OUTPUT_LOGFILE

# Run the script
source ./env/bin/activate
echo "Running the main python script..." &>> $OUTPUT_LOGFILE
python ./src/main.py &>> $OUTPUT_LOGFILE
echo "Finished running the main python script. Now, compiling the papers..." &>> $OUTPUT_LOGFILE

# This script will create the video for YouTube
./src/compile_all_papers.sh "$SEPARATE_PAPERS_FOLDER" "$OUTPUT_VIDEO_FILE" &>> $OUTPUT_LOGFILE

cd "$SCRIPT_DIR"

python ./src/upload_yt_video.py &>> $OUTPUT_LOGFILE

# Move the files to the output folder
#cp "./workdir/$OUTPUT_TEX_FILE" "$OUTPUT_FOLDER"
#cp "./workdir/$OUTPUT_SPEECH_FILE" "$OUTPUT_FOLDER"
#cp "./workdir/$SEPARATE_PAPERS_FOLDER/$OUTPUT_VIDEO_FILE" "$OUTPUT_FOLDER"

# Compile the document
cd "$OUTPUT_FOLDER" || { echo "Output folder doesn't exist! Exiting..."; exit 1; }
#pdflatex -interaction=nonstopmode "$OUTPUT_TEX_FILE"

# Cleanup the folder - only leave .tex, .pdf, .mp4 and .mp3 files
for file in *; do
    if [[ ! $file =~ \.tex$ ]] && [[ ! $file =~ \.pdf$ ]] && [[ ! $file =~ \.mp3$ ]] && [[ ! $file =~ \.mp4$ ]]; then
        rm "$file"
    fi
done


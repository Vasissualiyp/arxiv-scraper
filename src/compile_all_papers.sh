#!/bin/bash

# Directory containing your .tex files
DIRECTORY="./workdir/separate_papers/"

# Change to the directory
cd "$DIRECTORY"
#
## Convert .tex to .pdf for all files in directory
#
## Iterate over all *_read.tex files in the directory
#for texfile in *_read.tex; do
#    echo "Compiling $texfile..."
#    pdflatex -interaction=nonstopmode "$texfile" > /dev/null
#
#    # Check if pdflatex succeeded
#    if [ $? -eq 0 ]; then
#        echo "$texfile compiled successfully."
#    else
#        echo "Failed to compile $texfile."
#    fi
#done
#
#echo "All files compiled."
#
## Iterate over all PDF files in the directory
#for pdffile in *.pdf; do
#    # Extract base name without the extension
#    base_name="${pdffile%.pdf}"
#
#    echo "Converting $pdffile to PNG..."
#    pdftoppm -png -r 300 "$pdffile" "${base_name}"
#done
#
## Convert .pdf to .png for all files in directory
#
#echo "Conversion pdf -> png completed."
#
## Now, create mp4 files
#
## Iterate over all .mp3 files in the current directory
#for audio_file in *.mp3; do
#    # Extract the base name without the file extension
#    base_name="${audio_file%.*}"
#    
#    # Define the corresponding image file name
#    image_file="${base_name}_read-1.png"
#    
#    # Define the output video file name
#    output_file="${base_name}.mp4"
#    
#    # Check if the image file exists
#    if [ -f "$image_file" ]; then
#        echo "Processing: $base_name"
#        
#        # Use ffmpeg to create video file from the image and audio files
#        ffmpeg -loop 1 -framerate 1 -i "$image_file" -i "$audio_file" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "$output_file"
#        
#        echo "Created video: $output_file"
#    else
#        echo "Image file not found for $audio_file"
#    fi
#done

# Create a temporary file list for ffmpeg
file_list=$(mktemp /tmp/ffmpeg_list.XXXXXX.txt)

# List all .mp4 files, sort them numerically, and add file 'entry' format for ffmpeg
for f in $(ls *.mp4 | sort -V); do
    echo "file '$PWD/$f'" >> "$file_list"
done

# Define the output file name
output_file="combined_video.mp4"

# Use ffmpeg to concatenate all videos using the generated file list
ffmpeg -f concat -safe 0 -i "$file_list" -c copy "$output_file"

# Remove the temporary file list
rm "$file_list"

echo "All videos have been combined into $output_file"

#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# This is optional directory where the final tex file will be located. You can change the location of the final file in the run.sh script
read -p "Do you want to save the outputs (compiled tex files) in the output folder? (y/n): " create_output_dir
if [[ "$create_output_dir" == "y" ]]; then
    mkdir output 
		echo "The output will be saved in ${SCRIPT_DIR}/output/"
else
		echo "You will have to manually change the folder where the output tex file is saved in run.sh"
fi

# Create python environment
if [ -d "$ENV_FOLDER" ]; then
	echo "Skipping creation of the environment..."
else
  python -m venv env
fi

# Path to the activate script
ACTIVATE_SCRIPT="./env/bin/activate"

#---------OPENAI API KEY----------

# Check if OPENAI_API_KEY is already set in the activate script
if grep -q "export OPENAI_API_KEY=" "$ACTIVATE_SCRIPT"; then
    echo "OpenAI API Key is already set in the activate script."
else
    # Prompt the user for the OpenAI API key
    read -p "Enter your OpenAI API Key: " openai_key

    # Append the export command to the end of the activate script
    echo "export OPENAI_API_KEY=$openai_key" >> "$ACTIVATE_SCRIPT"

    echo "API key added to the activate script."
fi

#---------DEPENDENCIES-----------

# Activate python environment
source ./env/bin/activate

echo "Installing dependencies..."

pip install -r requirements.txt

#--------CRONTAB SCHEDULING-------

# Ask user if they want to schedule run.sh with cron
read -p "Do you want to schedule run.sh to run daily? (y/n): " schedule_cron

if [[ "$schedule_cron" == "y" ]]; then
    # Prompt user for the time to run the script daily
    read -p "Enter the time to run the script daily (HH:MM format, 24-hour clock): " cron_time

    # Format the cron_time into cron format
    hour=$(echo $cron_time | cut -d':' -f1)
    minute=$(echo $cron_time | cut -d':' -f2)
    cron_entry="$minute $hour * * * /bin/bash $(pwd)/run.sh"

    # Add the cron job
    (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -

    echo "Scheduled run.sh to run daily at $cron_time."
else
    echo "Skipping scheduling."
fi

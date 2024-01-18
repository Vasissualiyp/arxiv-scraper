#!/bin/bash

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

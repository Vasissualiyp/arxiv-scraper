#!/bin/bash

# Create python environment
if [ -d "$ENV_FOLDER" ]; then
	echo "Skipping creation of the environment..."
else
  python -m venv env
fi

# Path to the activate script
ACTIVATE_SCRIPT="./env/bin/activate"

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

# Activate python environment
source ./env/bin/activate

echo "Installing dependencies..."

pip install -r requirements.txt
